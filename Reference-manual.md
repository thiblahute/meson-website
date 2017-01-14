This page lists functions and methods available in Meson scripts. For more in-depth documentation on how to use them, refer to the [manual](Manual).

## Functions

The following functions are available in build files. Click on each to see the description and usage. The objects returned by them are [list afterwards](#returned-objects).

 * [add_global_arguments](#add_global_arguments)
 * [add_global_link_arguments](#add_global_link_arguments)
 * [add_languages](#add_languages)
 * [add_project_arguments](#add_project_arguments)
 * [add_project_link_arguments](#add_project_link_arguments)
 * [benchmark](#benchmark)
 * [build_target](#build_target)
 * [configuration_data](#configuration_data)
 * [configure_file](#configure_file)
 * [custom_target](#custom_target)
 * [declare_dependency](#declare_dependency)
 * [dependency](#dependency)
 * [error](#errormessage)
 * [environment](#environment)
 * [executable](#executable)
 * [find_program](#find_program)
 * [find_library](#find_library)
 * [files](#files)
 * [generator](#generator)
 * [get_option](#get_option)
 * [get_variable](#get_variable)
 * [import](#import)
 * [include_directories](#include_directories)
 * [install_data](#install_data)
 * [install_headers](#install_headers)
 * [install_man](#install_man)
 * [install_subdir](#install_subdir)
 * [is_subproject](#is_subproject)
 * [is_variable](#is_variable)
 * [jar](#jar)
 * [join_paths](#join_paths)
 * [library](#library)
 * [message](#message)
 * [project](#project)
 * [run_command](#run_command)
 * [run_target](#run_target)
 * [set_variable](#set_variable)
 * [shared_library](#shared_library)
 * [static_library](#static_library)
 * [subdir](#subdir)
 * [subproject](#subproject)
 * [test](#test)
 * [vcs_tag](#vcs_tag)

## Built-in objects

These are built-in objects that are always available.

 * [meson](#meson-object)
 * [build_machine](#build_machine-object)
 * [host_machine](#host_machine-object)
 * [target_machine](#target_machine-object)
 * [String](#string-object)
 * [Number](#number-object)
 * [Boolean](#boolean-object)
 * [Array](#array-object)

## Returned objects

These are objects returned by the [functions listed above](#functions).

 * [build target object](#build-target-object)
 * [compiler object](#compiler-object)
 * [run result object](#run-result-object)
 * [configuration data object](#configuration-data-object)
 * [dependency object](#dependency-object)
 * [external program object](#external-program-object)
 * [environment object](#environment-object)
 * [external library object](#external-library-object)
 * [generator object](#generator-object)

### add_global_arguments

    void add_global_arguments(arg1, arg2, ...)

Adds the positional arguments to the compiler command line for the language specified in `language` keyword argument. Note that there is no way to remove an argument set in this way. If you have an argument that is only used in a subset of targets, you have to specify it in per-target flags.

The arguments are used in all compiler invocations with the exception of compile tests, because you might need to run a compile test with and without the argument in question. For this reason only the arguments explicitly specified are used during compile tests.

Note that usually you should use `add_project_arguments` instead, because that works even when you project is used as a subproject.

### add_global_link_arguments

    void add_global_link_arguments(*arg1*, *arg2*, ...)

Like `add_global_arguments` but the arguments are passed to the linker.

### add_languages

    add_languages(*langs*)

Add support for new programming languages. Equivalent to having them in the `project` declaration. This function is usually used to add languages that are only used on some platforms like this:

    project('foobar', 'c')
    if compiling_for_osx
      add_languages('objc')
    endif

Takes one keyword argument, `required`. It defaults to `true`, which means that if any of the languages specified is not found, Meson will halt. Returns true if all languages specified were found and false otherwise.

### add_project_arguments

    void add_project_arguments(arg1, arg2, ...)

This function behaves in the same way as `add_global_arguments` except that the arguments are only used for the current project, they won't be used in any other subproject.

### add_project_link_arguments

    void add_project_link_arguments(*arg1*, *arg2*, ...)

Like `add_project_arguments` but the arguments are passed to the linker.

### benchmark

    void benchmark(name, executable, ...)

Creates a benchmark item that will be run when the benchmark target is run. The behaviour of this function is identical to `test` with the exception that there is no `is_parallel` keyword, because benchmarks are never run in parallel.

### build_target

Creates a build target whose type can be set dynamically with the `target_type` keyword argument. This declaration:

    executable(<arguments and keyword arguments>)

is equivalent to this:

    build_target(<arguments and keyword arguments>, target_type : 'executable')

The object returned by `build_target` and all convenience wrappers for `build_target` such as [`executable`](#executable) and [`library`](#library) has methods that are documented in the [object methods section](#build-target-object) below.

### configuration_data

    configuration_data_object = configuration_data()

Creates an empty configuration object. You should add your configuration with [its method calls](#configuration-data-object) and finally use it in a call to `configure_file`.

### configure_file

    generated_file = configure_file(...)

Takes a configuration file template and values and produces a file as specified in [the configuration file documentation](Configuration). The keyword arguments are the following:

- `input` the input file name. If it's not specified, all the variables in the `configuration` object (see below) are written to the `output` file.
- `output` the output file name. The permissions of the input file (if it is specified) are copied to the output file.
- `configuration` the configuration data object as returned by `configuration_data`
- `command` if specified Meson does not create the file itself but rather runs the specified command, which allows you to do fully custom file generation
- `install_dir` the subdirectory to install the generated file to (e.g. `share/myproject`), if omitted the file is not installed

### custom_target

    ctarget custom_target(*name*, ...)

Create a custom top level build target. The only positional argument is the name of this target and the keyword arguments are the following.

- `input` list of source files
- `output` list of output files
- `command` command to run to create outputs from inputs (note: always specify commands in array form `['commandname', '-arg1', '-arg2']` rather than as a string `'commandname -arg1 -arg2'` as the latter will *not* work)
- `install` when true, this target is installed during the install step
- `install_dir` directory to install to
- `build_always` if `true` this target is always considered out of date and is rebuilt every time, useful for things such as build timestamps or revision control tags
- `capture`, there are some compilers that can't be told to write their output to a file but instead write it to standard output. When this argument is set to true, Meson captures `stdout` and writes it to the target file. Note that your command argument list may not contain `@OUTPUT@` when capture mode is active.
- `depends` specifies that this target depends on the specified target(s), even though it does not take any of them as a command line argument. This is meant for cases where you have a tool that e.g. does globbing internally. Usually you should just put the generated sources as inputs and Meson will set up all dependencies automatically.
- `depend_files` files ([`string`](#string-object), [`files()`](#files), or [`configure_file()`](#configure_file)) that this target depends on but are not listed in the `command` kwarg. Useful for adding regen dependencies.
- `depfile` is a dependency file that the command can write listing all the additional files this target depends on, for example a C compiler would list all the header files it included, and a change in any one of these files triggers a recompilation

The list of strings passed to the `command` kwarg accept the following special string substitutions:

- `@INPUT@` the full path to the input passed to `input` (if only one was specified)
- `@OUTPUT@` the full path to the output passed to `output` (if only one was specified)
- `@INPUT0@` `@INPUT1@` `...` the full path to the input with the specified array index in `input`
- `@OUTPUT0@` `@OUTPUT1@` `...` the full path to the output with the specified array index in `output`
- `@OUTDIR@` the full path to the directory where the output(s) must be written
- `@DEPFILE@` the full path to the dependency file passed to `depfile`

### declare_dependency

    dependency_object declare_dependency(...)

This function creates a dependency object that behaves like the return value of `dependency` but is internal to the current build. The main use case for this is in subprojects. This allows a subproject to easily specify how it should be used. This makes it interchangeable with the same dependency that is provided externally by the system. This function has three keyword arguments.

  - `include_directories`, the directories to add to header search path
  - `link_with`, libraries to link against
  - `sources`, sources to add to targets (or generated header files that should be built before sources including them are built)
  - `dependencies`, other dependencies needed to use this dependency
  - `compile_args`, compile arguments to use
  - `link_args`, link arguments to use
  - `version`, the version of this depency, such as `1.2.3`

### dependency

    dependency_object dependency(*dependency_name*, ...)

Finds an external dependency with the given name with pkg-config if possible and with fallback detection logic otherwise. Dependency supports the following keyword arguments.

- `modules` specifies submodules to use for dependencies such as Qt5 or Boost.
- `required`, when set to false, Meson will proceed with the build even if the dependency is not found
- `version`, specifies the required version, a string containing a comparison operator followed by the version string, examples include `>1.0.0`, `<=2.3.5` or `3.1.4` for exact matching. (*Added 0.37.0*) You can also specify multiple restrictions by passing a list to this kwarg, such as: `['>=3.14.0', '<=4.1.0']`.
- `native` if set to `true`, causes Meson to find the dependency on the build machine system rather than the host system (i.e. where the cross compiled binary will run on), usually only needed if you build a tool to be used during compilation.
- `fallback` specifies a subproject fallback to use in case the dependency is not found in the system. The value is an array `['subproj_name', 'subproj_dep']` where the first value is the name of the subproject and the second is the variable name in that subproject that contains the value of `declare_dependency`.
- `static` tells the dependency provider to try to get static libraries instead of dynamic ones (note that this is not supported by all dependency backends)

The returned object also has methods that are documented in the [object methods section](#dependency-object) below.

### error

    void error(message)

Print the argument string and halts the build process.

### environment

    environment_object environment()

Returns an empty [environment variable object](#environment-object).

### executable

    exe executable(*exe_name*, *sources*, ...)

Creates a new executable. The first argument specifies its name and the remaining positional arguments define the source files to use.

Executable supports the following keyword arguments. These keyword arguments are also used for [shared and static libraries](#library).

- `link_with`, one or more shared or static libraries (built by this project) that this target should be linked with
- `<languagename>_pch` precompiled header file to use for the given language
- `<languagename>_args` compiler flags to use for the given language; eg: `cpp_args` for C++
- `link_args` flags to use during linking. You can use unix-style flags here for all platforms.
- `link_depends` an extra file that the link step depends on such as a symbol visibility map
- `include_directories` one or more objects created with the `include_directories` function
- `dependencies` one or more objects created with [`dependency`](#dependency) or [`find_library`](#compiler-object) (for external deps) or [`declare_dependency`](#declare_dependency) (for deps built by the project)
- `gui_app` when set to true flags this target as a GUI application on platforms where this makes a difference (e.g. Windows)
- `extra_files` are not used for the build itself but are shown as source files in IDEs that group files by targets (such as Visual Studio)
- `install`, when set to true, this executable should be installed
- `install_rpath` a string to set the target's rpath to after install (but *not* before that)
- `install_dir` override install directory for this file. The value is relative to the `prefix` specified. F.ex, if you want to install plugins into a subdir, you'd use something like this: `install_dir : get_option('libdir') + '/projectname-1.0'`.
- `objects` list of prebuilt object files (usually for third party products you don't have source to) that should be linked in this target, **never** use this for object files that you build yourself.
- `name_suffix` the string that will be used as the extension for the target by overriding the default. By default on Windows this is `exe` and on other platforms it is omitted.

The list of `sources`, `objects`, and `dependencies` is always flattened, which means you can freely nest and add lists while creating the final list. As a corollary, the best way to handle a 'disabled dependency' is by assigning an empty list `[]` to it and passing it like any other dependency to the `dependencies:` kwarg.

The returned object also has methods that are documented in the [object methods section](#build-target-object) below.

### find_program

    program find_program(program_name1, program_name2, ...)

Tries to locate the command listed in the positional argument. It can either be a command or a script in the source directory. Meson will also autodetect scripts with a shebang line and run them with the executable specified in it both on Windows (because the command invocator will reject the command otherwise) and unixes (if the script file does not have the executable bit set).

This function takes many arguments and is meant to be used for cases where the program may have many alternative names, such as `foo` and `foo.py`. The function will check for the arguments one by one and the first one that is found is returned. Meson versions earlier than 0.37.0 only accept one argument.

If the program is not found, Meson will abort. You can tell it not to by setting the keyword argument `required` to false.

The returned object also has methods that are documented in the [object methods section](#external-program-object) below.

### find_library

This function is deprecated and in the 0.31.0 release it was moved to [the compiler object](#compiler-object) as obtained from `meson.get_compiler(lang)`.

### files

    file_array files(list_of_filenames)

This command takes the strings given to it in arguments and returns corresponding File objects that you can use as sources for build targets. The difference is that file objects remember the subdirectory they were defined in and can be used anywhere in the source tree. As an example suppose you have source file `foo.cpp` in subdirectory `bar1` and you would like to use it in a build target that is defined in `bar2`. To make this happen you first create the object in `bar1` like this:

    foofile = files('foo.cpp')

Then you can use it in `bar2` like this:

    executable('myprog', 'myprog.cpp', foofile, ...)

Meson will then do the right thing.

### generator

    generator_object gen(*executable*, ...)

This function creates a generator object that can be used to run custom compilation commands. The only positional argument is the executable to use. It can either be a self-built executable or one returned by find_program. Keyword arguments are the following:

- `arguments` a list of template strings that will be the command line arguments passed to the executable
- `output` a template string (or list of template strings) defining how an output file name is (or multiple output names are) generated from a single source file name
- `depfile` is a template string pointing to a dependency file that a generator can write listing all the additional files this target depends on, for example a C compiler would list all the header files it included, and a change in any one of these files triggers a recompilation

The returned object also has methods that are documented in the [object methods section](#generator-object) below.

The template strings passed to all the above kwargs accept the following special substitutions:

- `@PLAINNAME@`: the complete input file name, e.g: `foo.c` becomes `foo.c` (unchanged)
- `@BASENAME@`: the base of the input filename, e.g.: `foo.c.y` becomes `foo.c` (extension is removed)

Each string passed to the `outputs` kwarg *must* be constructed using one or both of these two substitutions.

In addition to the above substitutions, the `arguments` kwarg also accepts the following:

- `@OUTPUT@`: the full path to the output file
- `@INPUT@`: the full path to the input file
- `@SOURCE_DIR@`: the full path to the root of the source tree 
- `@BUILD_DIR@`: the full path to the root of the build dir where the output will be placed

NOTE: Generators should only be used for outputs that will ***only*** be used as inputs for a [build target](#build_target) or a [custom target](#custom_target). When you use the processed output of a generator in multiple targets, the generator will be run multiple times to create outputs for each target. Each output will be created in a target-private directory `@BUILD_DIR@`.

If you want to generate files for general purposes such as for generating headers to be used by several sources, or data that will be installed, and so on, use a [`custom_target`](#custom_target) instead.

### get_option

    value get_option(option_name)

Obtains the value of the [project build option](Build options) specified in the positional argument.

### get_variable

    value get_variable(variable_name, fallback)

This function can be used to dynamically obtain a variable. `res = get_variable(varname, fallback)` takes the value of `varname` (which must be a string) and stores the variable of that name into `res`. If the variable does not exist, the variable `fallback` is stored to `res`instead. If a fallback is not specified, then attempting to read a non-existing variable will cause a fatal error.

### import

    module_object import(module_name)

Imports the given extension module. Returns an opaque object that can be used to call the methods of the module. Here's an example for a hypothetical `testmod` module.

    tmod = import('testmod')
    tmod.do_something()

### include_directories

    include_object include_directories(directory_names, ...)

Returns an opaque object which contains the directories given in positional arguments. The result can then be used as a keyword argument when building executables or libraries. Both the source directory and the corresponding build directory are added. Note that this function call itself does not add the directories into the search path, since there is no global search path. You can use the the returned object in any subdirectory you want, Meson will make the paths work automatically. This function has one keyword argument `is_system` which, if set, flags the specified directories as system directories. This means that they will be used with the `-isystem` compiler argument rather than `-I` on compilers that support this flag (in practice everything except Visual Studio).

### install_data

    void install_data(list_of_files, ...)

Installs files listed in positional and `sources` keyword arguments into the directory specified by the `install_dir` argument during install phase.

### install_headers

    void install_headers(list_of_headers, ...)

Installs the specified header files into the system header directory (usually `/{prefix}/include`) during the install step. This directory can be overridden by specifying it with the `install_dir` keyword argument. If you just want to install into a subdirectory of the system header directory, then use the `subdir` argument. As an example if this has the value `myproj` then the headers would be installed to `/{prefix}/include/myproj`.

For example, this will install `common.h` and `kola.h` into `/{prefix}/include`:

```
install_headers('common.h', 'proj/kola.h')
```

This will install `common.h` and `kola.h` into `/{prefix}/include/myproj`:

```
install_headers('common.h', 'proj/kola.h', subdir : 'myproj')
```

This will install `common.h` and `kola.h` into `/{prefix}/cust/myproj`:

```
install_headers('common.h', 'proj/kola.h', install_dir : 'cust', subdir : 'myproj')
```

### install_man

    void install_man(list_of_manpages, ...)

Installs the man files specified into system's man directory during the install step. This directory can be overridden by specifying it with the `install_dir` keyword argument.

### install_subdir

    void install_subdir(subdir_name)

Installs the entire given subdirectory tree to the location specified by the keyword argument `install_dir`. Note that due to implementation issues this command deletes the entire target dir before copying the files, so you should never use `install_subdir` to install into two overlapping directories (such as `foo` and `foo/bar`) because if you do the behaviour is undefined.

### is_subproject

    bool is_subproject()

Returns true if the current project is being built as a subproject of some other project and false otherwise.

### is_variable

    bool is_variable(varname)

Returns true if a variable of the given name exists and false otherwise.

### jar

   jar_object jar(name, list_of_sources, ...)

Build a jar from the specified Java source files. Keyword arguments are the same as executable's, with the addition of `main_class` which specifies the main class to execute when running the jar with `java -jar file.jar`.

### join_paths

   string join_paths([strings to join])

Joins the given strings into a file system path segment. For example `join_paths('foo', 'bar')` results in `foo/bar`. If any one of the individual segments is an absolute path, all segments before it are dropped. That means that `join_paths('foo', '/bar')` returns `/bar`.

*Added 0.36.0*

### library

    buildtarget library(library_name, list_of_sources, ...)

Builds a library that is either static or shared depending on the value of `default_library` user option. You should use this instead of [`shared_library`](#shared_library) or [`static_library`](#static_library) most of the time. This allows you to toggle your entire project (including subprojects) from shared to static with only one option.

The keyword arguments for this are the same as for [`executable`](#executable) with the following addition:

- `name_prefix` the string that will be used as the suffix for the target by overriding the default (only used for libraries). By default this is `lib` on all platforms and compilers except with MSVC where it is omitted.

`static_library` and `shared_library` also accept this keyword argument.

### message

    void message(text)

This function prints its argument to stdout.

### project

    void project(project_name, list_of_languages, ...)

The first argument to this function must be a string defining the name of this project. It must be followed by one or more programming languages that the project uses. Supported values for languages are `c`, `cpp` (for `C++`), `objc`, `objcpp`, `fortran`, `java`, `cs` (for `C#`) and `vala`.

The project name can be any string you want, it's not used for anything except descriptive purposes. However since it is written to e.g. the dependency manifest is usually makes sense to have it be the same as the project tarball or pkg-config name. So for example you would probably want to use the name _libfoobar_ instead of _The Foobar Library_.

You can specify a keyword argument `version`, which is a free form string describing the version of this project. You can access the value in your Meson build files with `meson.project_version()`.

Keyword argument `subproject_dir` specifies the top level directory name that holds Meson subprojects. This is only meant as a compatibility option for existing code bases that house their embedded source code in a custom directory. All new projects should not set this but instead use the default value. It should be noted that this keyword argument is ignored inside subprojects. There can be only one subproject dir and it is set in the top level Meson file. 

The argument `meson_version` takes a string describing which Meson version the project requires. Usually something like `>0.28.0`. Similarly you can specify the license(s) the code is under with the `license` keyword argument. Usually this would be something like `license : 'GPL2+'`, but if the code has multiple licenses you can specify them as an array like this: `license : ['proprietary', 'GPL3']`. Note that the text is informal and is only written to the dependency manifest. Meson does not do any license validation, you are responsible for verifying that you abide by all licensing terms.

You can specify default values for project options with the `default_options` keyword, which takes an array of strings. The strings are in the form `key=value` and have the same format as options to `mesonconf`. For example to set the default project type you would set this: `default_options : ['buildtype=debugoptimized']`. Note that these settings are only used when running Meson for the first time. They are also ignored in subprojects, only ones in the top level project are used.

### run_command

    runresult run_command(command, list_of_args)

Runs the command specified in positional arguments. Returns [an opaque object](#run-result-object) containing the result of the invocation. The script is run from an *unspecified* directory, and Meson will set three environment variables `MESON_SOURCE_ROOT`, `MESON_BUILD_ROOT` and `MESON_SUBDIR` that specify the source directory, build directory and subdirectory the target was defined in, respectively.

### run_target

    buildtarget run_target(target_name, ...)

This function creates a new top level target that runs the command specified. The script is run from an *unspecified* directory, and Meson will set three environment variables `MESON_SOURCE_ROOT`, `MESON_BUILD_ROOT` and `MESON_SUBDIR` that specify the source directory, build directory and subdirectory the target was defined in, respectively.

 - `command` is an array of the command to run, each item may be a string or a target
 - `depends` is a list of targets that this target depend on but which are not listed in the command array (because, for example, the script does file globbing internally)

### set_variable

    void set_variable(variable_name, value)

Assigns a value to the given variable name. Calling `set_variable('foo', bar)` is equivalent to `foo = bar`.

### shared_library

    buildtarget shared_library(library_name, list_of_sources, ...)

Builds a shared library with the given sources. Positional and keyword arguments are the same as for [`library`](#library) with the following extra keyword arguments.

- `version` a string specifying the version of this shared library, such as `1.1.0`. On Linux and OS X, this is used to set the shared library version in the filename, such as `libfoo.so.1.1.0` and `libfoo.1.1.0.dylib`. If this is not specified, `soversion` is used instead (see below).
- `soversion` a string specifying the soversion of this shared library, such as `0`. On Linux and Windows this is used to set the soversion (or equivalent) in the filename. For example, if `soversion` is `4`, a Windows DLL will be called `foo-4.dll` and one of the aliases of the Linux shared library would be `libfoo.so.4`. If this is not specified, the first part of `version` is used instead. For example, if `version` is `3.6.0` and `soversion` is not defined, it is set to `3`.
- `vs_module_defs` a string pointing to a file that contains 