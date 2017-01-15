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
- `build_by_default` causes, when set to true, to have this target be built by default, that is, when invoking plain `ninja`, the default value is false, available since 0.38.0

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
- `build_by_default` causes, when set to true, to have this target be built by default, that is, when invoking plain `ninja`, the default value is true for all built target types, since 0.38.0

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

Project supports the following keyword arguments.

 - `version`, which is a free form string describing the version of this project. You can access the value in your Meson build files with `meson.project_version()`.

 - `subproject_dir` specifies the top level directory name that holds Meson subprojects. This is only meant as a compatibility option for existing code bases that house their embedded source code in a custom directory. All new projects should not set this but instead use the default value. It should be noted that this keyword argument is ignored inside subprojects. There can be only one subproject dir and it is set in the top level Meson file. 

 - `meson_version` takes a string describing which Meson version the project requires. Usually something like `>0.28.0`. Similarly you can specify the license(s) the code is under with the `license` keyword argument. Usually this would be something like `license : 'GPL2+'`, but if the code has multiple licenses you can specify them as an array like this: `license : ['proprietary', 'GPL3']`. Note that the text is informal and is only written to the dependency manifest. Meson does not do any license validation, you are responsible for verifying that you abide by all licensing terms.

 - `default_options` takes an array of strings. The strings are in the form `key=value` and have the same format as options to `mesonconf`. For example to set the default project type you would set this: `default_options : ['buildtype=debugoptimized']`. Note that these settings are only used when running Meson for the first time. Global options such as `buildtype` can only be specified in the master project, settings in subprojects are ignored. Project specific options are used normally even in subprojects.

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
- `vs_module_defs` a string pointing to a file that contains Visual Studio symbol export definitions.

### static_library

    buildtarget static_library(library_name, list_of_sources, ...)

Builds a static library with the given sources. Positional and keyword arguments are otherwise the same as for [`library`](#library), but it has one argument the others don't have:

 - `pic`, (*Added 0.36.0*) builds the library as positional independent code (so it can be linked into a shared library). This option has no effect on Windows and OS X since it doesn't make sense on Windows and PIC cannot be disabled on OS X.

### subdir

    void subdir(dir_name)

Recurses into the specified subdirectory and executes the `meson.build` file in it. Once that is done, it returns and execution continues on the line following this `subdir` command.

### subproject

    subproject_object subproject(subproject_name, ...)

Takes the project specified in the positional argument and brings that in the current build specification. Subprojects must always be placed inside the `subprojects` directory at the top source directory. So for example a subproject called `foo` must be located in `${MESON_SOURCE_ROOT}/subprojects/foo`. Supports the following keyword arguments:

 - `version` keyword argument that works just like the one in `dependency`. It specifies what version the subproject should be, as an example `>=1.0.1`
 - `default_options`, an array of default option values that override those set in the project's `default_options` invocation (like `default_options` in `project`, they only have effect when Meson is run for the first time, and command line arguments override any default options in build files)

### test

    void test(name, executable, ...)

Defines an unit test. Takes two positional arguments, the first is the name of this test and the second is the executable to run. Keyword arguments are the following.

- `args` arguments to pass to the executable
- `env` environment variables to set, such as `['NAME1=value1', 'NAME2=value2']`
- `is_parallel` when false, specifies that no other test must be running at the same time as this test
- `should_fail` when true the test is considered passed if the executable returns a non-zero return value (i.e. reports an error)
- `valgrind_args` if the test is run under Valgrind, pass these arguments to Valgrind (and not to the executable itself)
- `timeout` the amount of seconds the test is allowed to run, a test that exceeds its time limit is always considered failed, defaults to 30 seconds
- `workdir` absolute path that will be used as the working directory for the test

### vcs_tag

    void vcs_tag(...)

This command detects revision control commit information and places it in a specified file. This file is guaranteed to be up to date on every build. Keywords are similar to `custom_target` and all of them are mandatory.

- `input` file to modify (e.g. `version.c.in`)
- `output` file to write the results to (e.g. `version.c`)
- `fallback` version number to use when no revision control information is present, such as when building from a release tarball

Meson will read the contents of `input`, replace the string `@VCS_TAG@` with the detected revision number and write the result to `output`. This method returns an opaque object that you should put in your main program. If you desire more specific behavior than what this command provides, you should use `custom_target`.

## Object methods

Meson has several different object types that have methods users can call. This section describes them.

### meson object

The `meson` object allows you to introspect various properties of the system. This object is always mapped in the `meson` variable. It has the following methods.

- `get_compiler(language)` returns [an object describing a compiler](#compiler-object), takes one positional argument which is the language to use. It also accepts one keyword argument, `native` which when set to true makes Meson return the compiler for the build machine (the "native" compiler) and when false it returns the host compiler (the "cross" compiler). If `native` is omitted, Meson returns the "cross" compiler if we're currently cross-compiling and the "native" compiler if we're not.

- `is_cross_build()` returns true if the current build is a cross build and false otherwise

- `is_unity()` returns true when doing a unity build

- `has_exe_wrapper()` returns true when doing a cross build if there is a wrapper command that can be used to execute cross built binaries (for example when cross compiling from Linux to Windows, one can use `wine` as the wrapper)

- `add_install_script(script_name, arg1, arg2, ...)` causes the script given as an argument to be run during the install step, this script will have the environment variables `MESON_SOURCE_ROOT`, `MESON_BUILD_ROOT`, `MESON_INSTALL_PREFIX`, and `MESON_INSTALL_DESTDIR_PREFIX` set. All additional arguments are passed as parameters.

 `MESON_INSTALL_PREFIX` has the value of the `prefix` option passed to Meson, and `MESON_INSTALL_DESTDIR_PREFIX` has both the value of `DESTDIR` and `prefix` joined together. This is useful because both are absolute paths, and many path-joining functions such as [`os.path.join` in Python](https://docs.python.org/3/library/os.path.html#os.path.join) special-case absolute paths.

- `add_postconf_script(script_name, arg1, arg2, ...)` will run the executable given as an argument after all project files have been generated. This script will have the environment variables `MESON_SOURCE_ROOT` and `MESON_BUILD_ROOT` set.

- `current_source_dir()` returns a string to the current source directory. Note: use the `files()` function to refer to files in the source directory instead of constructing paths manually with `meson.current_source_dir()`.

- `current_build_dir()` returns a string to the current build directory

- `source_root()` returns a string with the absolute path to the source root directory. Note: use the `files()` function to refer to files in the source directory instead of constructing paths manually with `meson.current_source_dir()`.

- `build_root()` returns a string with the absolute path to the build root directory

- `project_version()` returns the version string specified in `project` function call

- `project_name()` returns the project name specified in the `project` function call

- `version()` return a string with the version of Meson

- `get_cross_property(propname, fallback_value)` returns the given property from a cross file, the optional second argument is returned if not cross compiling or the given property is not found

- `install_dependency_manifest(output_name)` installs a manifest file containing a list of all subprojects, their versions and license files to the file name given as the argument

### build_machine object

Provides information about the build machine — the machine that is doing the actual compilation. See [Cross-compilation](Cross-compilation). It has the following methods:

- `cpu_family()` returns the CPU family name. Guaranteed to return `x86` for 32-bit userland on x86 CPUs, `x86_64` for 64-bit userland on x86 CPUs, `arm` for 32-bit userland on all ARM CPUs, etc.
- `cpu()` returns a more specific CPU name, such as `i686`, `amd64`, etc.
- `system()` returns the operating system name, such as `windows` (all versions of Windows), `linux` (all Linux distros), `darwin` (all versions of OS X), etc.
- `endian()` returns `big` on big-endian systems and `little` on little-endian systems.

If you think the returned values for any of these are incorrect for your system or CPU, please file [a bug report](/mesonbuild/meson/issues/new).

### host_machine object

Provides information about the host machine — the machine on which the compiled binary will run. See [Cross-compilation](Cross-compilation).

It has the same methods as [`build_machine`](#build_machine-object), but note that it simply returns the values defined in the cross-info file.

### target_machine object

Provides information about the target machine — the machine on which the compiled binary's output will run. Hence, this object should only be used while cross-compiling a compiler. See [Cross-compilation](Cross-compilation).

It has the same methods as [`build_machine`](#build_machine-object), but note that it simply returns the values defined in the cross-info file. If `target_machine` values are not defined in the cross-info file, `host_machine` values are returned instead.

### build target object

A build target is either an [executable](#executable), [shared](#shared_library) or [static library](#static_library).

- `extract_objects()` returns an opaque object representing the generated object files of arguments, usually used to take single object files and linking them to unit tests or compiling some source files with custom flags

- `extract_all_objects()` is same as above but returns all object files generated by this target

- `private_dir_include()` returns a opaque object that works like `include_directories` but points to the private directory of this target, usually only needed if an another target needs to access some generated internal headers of this target

- `full path()` returns a full path pointing to the result target file

### compiler object

This object is returned by [`meson.get_compiler(lang)`](#meson-object). It represents a compiler for a given language and allows you to query its properties. It has the following methods:

- `get_id()` returns a string identifying the compiler (e.g. `'gcc'`)
- `version()` returns the compiler's version number as a string
- `find_library(lib_name, ...)` tries to find the library specified in the positional argument. The [result object](#external-library-object) can be used just like the return value of `dependency`. If the keyword argument `required` is false, Meson will proceed even if the library is not found. By default the library is searched for in the system library directory (e.g. /usr/lib). This can be overridden with the `dirs` keyword argument, which can be either a string or a list of strings.
- `sizeof(typename, ...)` returns the size of the given type (e.g. `'int'`) or -1 if the type is unknown, to add includes set them in the `prefix` keyword argument, you can specify external dependencies to use with `dependencies` keyword argument
- `alignment(typename)` returns the alignment of the type specified in the positional argument, you can specify external dependencies to use with `dependencies` keyword argument
- `compiles(code)` returns true if the code fragment given in the positional argument compiles, you can specify external dependencies to use with `dependencies` keyword argument, `code` can be either a string containing source code or a `file` object pointing to the source code
- `links(code)` returns true if the code fragment given in the positional argument compiles and links, you can specify external dependencies to use with `dependencies` keyword argument, `code` can be either a string containing source code or a `file` object pointing to the source code
- `run(code)` attempts to compile and execute the given code fragment, returns a run result object, you can specify external dependencies to use with `dependencies` keyword argument, `code` can be either a string containing source code or a `file` object pointing to the source code
- `has_header` returns true if the specified header can be included, you can specify external dependencies to use with `dependencies` keyword argument and extra code to put above the header test with the `prefix` keyword
- `has_type(typename)` returns true if the specified token is a type, you can specify external dependencies to use with `dependencies` keyword argument
- `has_function(funcname)` returns true if the given function is provided by the standard library or a library passed in with the `args` keyword, you can specify external dependencies to use with `dependencies` keyword argument
- `has_member(typename, membername)` takes two arguments, type name and member name and returns true if the type has the specified member, you can specify external dependencies to use with `dependencies` keyword argument
- `has_members(typename, membername1, membername2, ...)` takes at least two arguments, type name and one or more member names, returns true if the type has all the specified members, you can specify external dependencies to use with `dependencies` keyword argument
- `has_header_symbol(headername, symbolname)` allows one to detect whether a particular symbol (function, variable, #define, type definition, etc) is declared in the specified header, you can specify external dependencies to use with `dependencies` keyword argument
- `has_argument(argument_name)` returns true if the compiler accepts the specified command line argument, that is, can compile code without erroring out or printing a warning about an unknown flag, you can specify external dependencies to use with `dependencies` keyword argument
- `has_multi_arguments(arg1, arg2, arg3, ...)` is the same as `has_argument` but takes multiple arguments and uses them all in a single compiler invocation, available since 0.37.0
- `first_supported_argument(list_of_strings)`, given a list of strings, returns the first argument that passes the `has_argument` test above or an empty array if none pass
- `symbols_have_underscore_prefix()` returns `true` if the C symbol mangling is one underscore (`_`) prefixed to the symbol, available since 0.37.0

The `prefix` keyword argument can be used to add #defines, #includes, etc that are required for the symbol to be declared (eg: `#define _GNU_SOURCE` is often required for some symbols to be exposed on Linux). Supported by the methods `sizeof`, `has_type`, `has_function`, `has_member`, `has_members`, `has_header_symbol`.

You can pass the `include_directories` keyword argument to specify extra directories for header searches. Available since version 0.38.0.

The `args` keyword argument can be used to pass a list of compiler arguments that are required to find the header or symbol. For example, you might need to pass the include path `-Isome/path/to/header` if a header is not in the default include path. In versions newer than 0.38.0 you should use the `include_directories` keyword described above. You may also want to pass a library name `-lfoo` for `has_function` to check for a function. Supported by all methods except `get_id`, `version`, and `find_library`. 

Note that if you have a single prefix with all your dependencies, you might find it easier to append to the environment variables `C_INCLUDE_PATH` with gcc/clang and `INCLUDE` with msvc to expand the default include path, and `LIBRARY_PATH` with gcc/clang and `LIB` with msvc to expand the default library search path.

However, with GCC, these variables will be ignored when cross-compiling. In that case you need to use a specs file. See: <http://www.mingw.org/wiki/SpecsFileHOWTO>

### run result object

This object encapsulates the result of trying to compile and run a sample piece of code with [`compiler.run()`](#compiler-object). It has the following methods:

- `compiled()` if true, the compilation succeeded, if false it did not and the other methods return unspecified data
- `returncode()` the return code of executing the compiled binary
- `stdout()` the standard out produced when the binary was run
- `stderr()` the standard error produced when the binary was run

### configuration data object

This object is returned by [`configuration_data`](#configuration_data) and encapsulates configuration values to be used for generating configuration files. A more in-depth description can be found in the [the configuration wiki page](Configuration) It has three methods:

 - `set(varname, value)`, sets a variable to a given value
 - `set10(varname, boolean_value)` is the same as above but the value is either `true` or `false` and will be written as 1 or 0, respectively
 - `set_quoted(varname, value)` is same as `set` but quotes the value in double quotes (`"`)
 - `has(varname)`, returns `true` if the specified variable is set
 - `get(varname, default_value)` returns the value of `varname`, if the value has not been set returns `default_value` if it is defined and errors out if not, since 0.38.0

They all take the `description` keyword that will be written in the result file. The replacement assumes a file with C syntax. If your generated file is source code in some other language, you probably don't want to add a description field because it most likely will cause a syntax error.

### dependency object

This object is returned by [`dependency`](#dependency) and contains an external dependency with the following methods:

 - `found()` which returns whether the dependency was found
 - `type_name()` which returns a string describing the type of the dependency, the most common values are `internal` for deps created with `declare_dependencies` and `pkgconfig` for system dependencies obtained with Pkg-config.
 - `version()` is the version number as a string, for example `1.2.8`
 - `get_pkgconfig_variable(varname)` (*Added 0.36.0*) will get the pkg-config variable specified, or, if invoked on a non pkg-config dependency, error out

### external program object

This object is returned by [`find_program`](#find_program) and contains an external (i.e. not built as part of this project) program and has the following methods:

- `found()` which returns whether the executable was found
- `path()` which returns an array pointing to the executable (this is an array as opposed to a string because the program might be `['python', 'foo.py']`, for example)

### environment object

This object is returned by [`environment`](#environment) and stores detailed information about how environment variables should be set during tests. It should be passed as the `env` keyword argument to tests. It has the following methods.

 - `set(varname, value)` sets environment variable in the first argument to the value in the second argument, e.g. `env.set('FOO', 'BAR') sets envvar `FOO` to value `BAR`
 - `append(varname, value)` appends the given value to the old value of the environment variable, e.g. `env.append'('FOO', 'BAR', separator : ';')` produces `BOB;BAR` if `FOO` had the value `BOB` and plain `BAR` if the value was not defined. If the separator is not specified explicitly, the default path separator for the host operating system will be used, i.e. ';' for Windows and ':' for UNIX/POSIX systems.
 - `prepend(varname, value)` is the same as `append` except that it writes to the beginning of the variable

### external library object

This object is returned by [`find_library`](#find_library) and contains an external (i.e. not built as part of this project) library. This object has only one method, `found`, which returns whether the library was found.

### generator object

This object is returned by [`generator`](#generator) and contains a generator that is used to transform files from one type to another by an executable (e.g. `idl` files into source code and headers).

- `process(list_of_files)` takes a list of files, causes them to be processed and returns an object containing the result which can then, for example, be passed into a build target definition. The keyword argument `extra_args`, if specified, will be used to replace an entry `@EXTRA_ARGS@` in the argument list.

### string object

All strings have the following methods. Strings are immutable, all operations return their results as a new string.

 - `strip()` removes whitespace at the beginning and end of the string
 - `format()` formats text, see the [[Syntax manual|Syntax#string-formatting]] for usage info
 - `to_upper()` creates an upper case version of the string
 - `to_lower()` creates a lower case version of the string
 - `underscorify()` creates a string where every non-alphabetical non-number character is replaced with `_`
 - `split(split_character)` splits the string at the specified character (or whitespace if not set) and returns the parts in an array
 - `startswith(string)` returns true if string starts with the string specified as the argument
 - `endswith(string)` returns true if string ends with the string specified as the argument
 - `contains(string)` returns true if string contains the string specified as the argument
 - `to_int` returns the string converted to an integer (error if string is not a number)
 - `join(list_of_strings)` is the opposite of split, for example `'.'.join(['a', 'b', 'c']` yields `'a.b.c'`
 - `version_compare(comparison_string)` does semantic version comparison, if `x = '1.2.3'` then `x.version_compare('>1.0.0')` returns `true`

### Number object

Numbers support these methods:

 - `is_even()` returns true if the number is even
 - `is_odd()` returns true if the number is odd

### boolean object

A boolean object has two simple methods:

 - `to_string()` returns the string `'true'` if the boolean is true or `'false'` otherwise. You can also pass it two strings as positional arguments to specify what to return for true/false. For instance, `bool.to_string('yes', 'no')` will return `yes` if the boolean is true and `no` if it is false.
 - `to_int()` as above, but returns either `1` or `0`

### array object

The following methods are defined for all arrays:

 - `length()`, the size of the array
 - `contains(item)`, returns `true` if the array contains the object given as argument, `false` otherwise
 - `get(index)`, returns the object at the given index, negative indices count from the back of the array, indexing out of bounds is a fatal error
