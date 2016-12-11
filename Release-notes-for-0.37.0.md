**0.37.0 is not released yet, these are preliminary**

# New features

## Mesontest

Mesontest is a new testing tool that allows you to run your tests in many different ways. As an example you can run tests multiple times:

    mesontest --repeat=1000 a_test

or with an arbitrary wrapper executable:

    mesontest --wrap='valgrind --tool=helgrind' a_test

or under gdb, 1000 times in a row. This is handy for tests that fail spuriously, as when the crash happens you are given the full GDB command line:

    mesontest --repeat=1000 --gdb a_test

## Mesonrewriter

Mesonrewrite is an experimental tool to manipulate your build definitions programmatically. It is not installed by default yet but those interested can run it from the source repository.

As an example, here is how you would add a source file to a build target:

    mesonrewriter add --target=program --filename=new_source.c

## Shared modules

The new `shared_module` function allows the creation of shared modules, that is, extension modules such as plugins that are meant to be used solely with `dlopen` rather than linking them to targets.

## Gnome module

- Detect required programs and print useful errors if missing

### gtkdoc

- Allow passing a list of directories to `src_dir` kwarg
- Add `namespace` kwarg
- Add `mode` kwarg
- Fix `gtkdoc-scangobj` finding local libraries

### compile_resources

- Add `gresource_bundle` kwarg to output `.gresource` files
- Add `export` and `install_header` kwargs
- Use depfile support available in GLib >= 2.52.0

## i18n module

- Add `merge_file()` function for creating translated files
- Add `preset` kwarg to included common gettext flags
- Read languages from `LINGUAS` file

## LLVM IR compilation

Meson has long had support for compiling assembler (GAS) files. In this release we add support for compiling LLVM IR files in a similar way when building with the Clang compiler. Just add it to the list of files when creating a `library` or `executable` target like any other source file. No special handling is required:

```
executable('some-exe', 'main.c', 'asm-file.S', 'ir-file.ll')
```

As always, you can also mix LLVM IR files with C++, C, and Assembly (GAS) sources.

## Other stuff

Add your highlights here.
