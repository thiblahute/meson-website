# Generating sources

Sometimes source files need to be preprocessed before they are passed to the actual compiler. As an example you might want build an IDL compiler and then run some files through that to generate actual source files. In Meson this is done with the following lines of code.

First we build the executable.

```meson
mycomp = executable('mycompiler', 'compiler.c')
```

Then we define a *generator*, which defines how to transform input files into output files.

```meson
gen = generator(mycomp,
                output  : '@BASENAME@.c',
                arguments : ['@INPUT@', '@OUTPUT@'])
```

The first argument is the executable file to run. The next file specifies a name generation rule. It specifies how to build the output file name for a given input name. `@BASENAME@` is a placeholder for the input file name without preceding path or suffix (if any). So if the input file name were `some/path/filename.idl`, then the output name would be `filename.c`. You can also use `@PLAINNAME@`, which preserves the suffix which would result in a file called `filename.idl.c`. The last line specifies the command line arguments to pass to the executable. `@INPUT@` and `@OUTPUT@` are placeholders for the input and output files, respectively, and will be automatically filled in by Meson. If your rule produces multiple output files and you need to pass them to the command line, append the location to the output holder like this: `@OUTPUT0@`, `@OUTPUT1@` and so on.

With this rule specified we can generate source files and add them to a target.

```meson
gen_src = gen.process('input1.idl', 'input2.idl')
executable('program', 'main.c', gen_src)
```

Generators can generate more than one output file.

```meson
gen2 = generator(someprog,
                 outputs : ['@BASENAME@.c', '@BASENAME@.h'],
                 arguments : ['--out_dir=@BUILD_DIR@', '@INPUT@']
```

In this case you can not use the plain `@OUTPUT@` variable, as it would be ambiguous. This program only needs to know the output directory, it will generate the file names by itself.
