# How do I do X in Meson?

This page lists code snippets for common tasks. These are written mostly using the C compiler, but the same approach should work on almost all other compilers.

# Set compiler

When first running Meson, set it in an environment variable.

    CC=mycc meson <options>

# Set default C/C++ language version

    project('myproj', 'c', 'cpp',
            default_options : ['c_std=c11', 'cpp_std=c++11'])

# Set extra compiler and linker flags 

The behaviour is the same as with other build systems, with environment variables during first invocation.

    CFLAGS=-fsomething LDFLAGS=-Wl,--linker-flag meson <options>

# Use an argument only with a specific compiler

First check which arguments to use.

    if meson.get_compiler('c').get_id() == 'clang'
      extra_args = ['-fclang-flag']
    else
      extra_args = []
    endif

Then use it in a target.

    executable(..., c_args : extra_args)

If you want to use the arguments on all targets, then do this.

    if meson.get_compiler('c').get_id() == 'clang'
      add_global_arguments('-fclang-flag', language : 'c')
    endif

# Set a command's output to configuration

    txt = run_command('script', 'argument').stdout().strip()
    cdata = configuration_data()
    cdata.set('SOMETHING', txt)
    configure_file(...)

# Generate a runnable script with `configure_file`

`configure_file` preserves metadata so if your template file has execute permissions, the generated file will have them too.

## Producing a coverage report ##

First initialise the build directory with this command.

    meson <other flags> -Db_coverage=true

Then issue the following commands.

    ninja
    ninja test
    ninja coverage-html (or coverage-xml)

The coverage report can be found in the meson-logs subdirectory.

## Adding some optimization to debug builds ##

By default the debug build does not use any optimizations. This is the desired approach most of the time. However some projects benefit from having some minor optimizations enabled. Gcc even has a specific compiler flag `-Og` for this. To enable its use, just issue the following command.

    mesonconf -Dc_args=-Og

This causes all subsequent builds to use this command line argument.

## Using address sanitizer

Clang comes with a selection of analysis tools such as the [address sanitizer](http://clang.llvm.org/docs/AddressSanitizer.html). Meson has native support for these with the `b_sanitize` option.

    meson <other options> -Db_sanitize=address

After this you just compile your code and run the test suite. Address sanitizer will abort executables which have bugs so they show up as test failures.

## Using Clang static analyzer ##

Install scan-build and configure your project. Then do this:

    ninja scanbuild

## Using profile guided optimization ##

Using profile guided optimization with GCC is a two phase operation. First we set up the project with profile measurements enabled and compile it.

    meson  <Meson options, such as --buildtype=debugoptimized> -Db_pgo=generate
    ninja

Then we need to run the program with some representative input. This step depends on your project.

Once that is done we change the compiler flags to use the generated information and rebuild.

    mesonconf -Db_pgo=use
    ninja

After these steps the resulting binary is fully optimized.

----

[Wiki home](Home)
