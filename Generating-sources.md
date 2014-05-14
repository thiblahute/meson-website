Sometimes source files need to be preprocessed before they are passed to the actual compiler. As an example you might want build an IDL compiler and then run some files through that to generate actual source files. In Meson this is done with the following lines of code.

First we build the executable.

    mycomp = executable('mycompiler', 'compiler.c')

Then we define a *generator*, which defines how to transform input files into output files.

    gen = generator(mycomp,
     outputs  : '@BASENAME@.c',
     arguments : ['@INPUT@', '@OUTPUT@'])

The first argument is the executable file to run. The next file specifies a name generation rule. It specifies how to build the output file name for a given input name. <tt>@BASENAME@</tt> is a placeholder for the input file name without preceding path or suffix (if any). So if the input file name were <tt>some/path/filename.idl</tt>, then the output name would be <tt>filename.c</tt>. You can also use <tt>@PLAINNAME@</tt>, which preserves the suffix which would result in a file called <tt>filename.idl.c</tt>. The last line specifies the command line arguments to pass to the executable. <tt>@INPUT@</tt> and <tt>@OUTPUT@</tt> are placeholders for the input and output files, respectively, and will be automatically filled in by Meson.

With this rule specified we can generate source files and add them to a target.

    gen_src = gen.process('input1.idl', 'input2.idl')
    executable('program', 'main.c', gen_src)

Generators can generate more than one output file.

    gen2 = generator(someprog,
     outputs : ['@BASENAME@.c', '@BASENAME@.h'],
     arguments : ['--out_dir=@BUILD_DIR@', '@INPUT@']

In this case you can not use the <tt>@OUTPUT@</tt> variable, as it would be ambiguous.

---

[Back to index](Manual).