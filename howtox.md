# How do I do X in Meson?

This page lists code snippets for common tasks. These are written mostly using the C compiler, but the same approach should work on almost all other compilers.

# Set compiler

When first running Meson, set it in an environment variable.

    CC=mycc meson <options>

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

----

[Wiki home](Home)
