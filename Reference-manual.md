This page lists functions and methods available in Meson scripts. For more in-depth documentation on how to use them, refer to the [manual](Manual).

## Functions

### add_global_arguments

Adds the positional arguments to the compiler command line for the language specified in <tt>language</tt> keyword argument. Note that there is no way to remove an argument set in this way. If you have an argument that is only used in a subset of targets, you have to specify it in per-target flags.

The arguments are used in all compiler invocations with the exception of compile tests, becausmes you might need to run a compile test with and without the argument in question. For this reason only the arguments explicitly specified are used during compile tests.

### add_languages

Add support for new programming languages. Equivalent to having them in the `project` declaration. This function is usually used to add languages that are only used on some platforms like this:

    project('foobar', 'c')
    if compiling_for_osx
      add_languages('objc')
    endif

Takes one keyword argument, `required`. It defaults to `true`, which means that if any of the languages specified is not found, Meson will halt. Returns true if all languages specified were found and false otherwise.

### benchmark

Creates a benchmark item that will be run when the benchmark target is run. The behaviour of this function is identical to `test` with the exception that there is no `is_parallel` keyword, because benchmarks are never run in parallel.

### build_target

Creates a build target whose type can be set dynamically with the `target_type` keyword argument. This declaration:

    executable(<arguments and keyword arguments>)

is equivalent to this:

    build_target(<arguments and keyword arguments>, target_type : 'executable')


### configuration_data

Creates an empty configuration object. You should add your configuration with its method calls and finally use it in a call to <tt>configure_file</tt>.

### configure_file ###

Takes a configuration file template and values and produces a file as specified in [the configuration file documentation](Configuration). The keyword arguments are the following:

- <tt>input</tt> the input file name
- <tt>output</tt> the output file name
- <tt>configuration</tt> the configuration data object as returned by <tt>configuration_data</tt>
- <tt>command</tt> if specified Meson does not create the file itself but rather runs the specified command, which allows you to do fully custom file generation
- <tt>install_dir</tt> the subdirectory to install the generated file to (e.g. <tt>share/myproject</tt>), if empty the file is not installed

### custom_target ###

Create a custom top level build target. The only positional argument is the name of this target and the keyword arguments are the following.

- <tt>input</tt> list of source files
- <tt>output</tt> list of output files
- <tt>command</tt> command to run to create outputs from inputs (note: always specify commands in array form <tt>['commandname', '-arg1', '-arg2']</tt> rather than as a string <tt>'commandname -arg1 -arg2'</tt> as the latter will *not* work)
- <tt>install</tt> when true, this target is installed during the install step
- <tt>install_dir</tt> directory to install to
- <tt>build_always</tt> if <tt>true</tt> this target is always considered out of date and is rebuilt every time, useful for things such as build timestamps or revision control tags
- <tt>depends</tt> specifies that this target depends on the specified target(s), even though it does not take any of them as a command line argument. This is meant for cases where you have a tool that e.g. does globbing internally. Usually you should just put the generated sources as inputs and Meson will set up all dependencies automatically.

### declare_dependency

This function creates a dependency object that behaves like the return value of `dependency` but is internal to the current build. The main use case for this is in subprojects. This allows a subproject to easily specify how it should be used. This makes it interchangeable with the same dependency that is provided externally by the system. This function has three keyword arguments.

  - `include_directories`, the directories to add to header search path
  - `link_with`, libraries to link against
  - `sources`, sources to add to targets (or generated header files that should be built before sources including them are built)
  - `dependencies`, other dependencies needed to use this dependency


### dependency

Finds an external dependency with the given name with pkg-config if possible and with fallback detection logic otherwise. Dependency supports the following keyword arguments.

- `modules` specifies submodules to use for dependencies such as Qt5 or Boost.
- `required`, when set to false, Meson will proceed with the build even if the dependency is not found
- `version`, specifies the required version, a string containing a comparison operator followed by the version string, examples include `>1.0.0`, `<=2.3.5` or `3.1.4` for exact matching
- `native` if set to `true`, causes Meson to find the dependency on the build machine system rather than the host system (i.e. where the cross compiled binary will run on), usually only needed if you build a tool to be used during compilation.
- `fallback` specifies a subproject fallback to use in case the dependency is not found in the system. The value is an array `['subproj_name', 'subproj_dep']` where the first value is the name of the subproject and the second is the variable name in that subproject that contains the value of `declare_dependency`.
- `static` tells the dependency provider to try to get static libraries instead of dynamic ones (note that this is not supported by all dependency backends)

### error

Print the argument string and halts the build process.

### executable ###

Creates a new executable. The first argument specifies its name and the remaining positional arguments define the source files to use.

Executable supports the following keyword arguments.

- <tt>link_with</tt>, one or more shared or static libraries (built by this project) that this target should be linked with
- <tt>&lt;languagename&gt;_pch</tt> precompiled header file to use for the given language
- <tt>&lt;languagename&gt;_args</tt> compiler flags to use for the given language
- <tt>link_args</tt> flags to use during linking
- <tt>link_depends</tt> an extra file that the link step depends on such as a symbol visibility map
- <tt>include_directories</tt> one or more objects created with the <tt>include_directories</tt> function
- <tt>dependencies</tt> one or more objects created with <tt>dependency</tt> or <tt>find_library</tt>
- <tt>gui_app</tt> when set to true flags this target as a GUI application on platforms where this makes a difference (e.g. Windows)
- <tt>extra_files</tt> are not used for the build itself but are shown as source files in IDEs that group files by targets (such as Visual Studio)
- <tt>install</tt>, when set to true, this executable should be installed
- <tt>install_rpath</tt> a string to set the target's rpath to after install (but *not* before that)
- <tt>install_dir</tt> override install directory for this file
- <tt>objects</tt> list of prebuilt object files (usually for third party products you don't have source to) that should be linked in this target, **never** use this for object files that you build yourself.

### find_program ###

Tries to locate the command listed in the positional argument. It can either be a command or a script in the source directory. Meson will also autodetect scripts with a shebang line and run them with the executable specified in it both on Windows (because the command invocator will reject the command otherwise) and unixes (if the script file does not have the executable bit set).

If the program is not found, Meson will abort. You can tell it not to by setting the keyword argument <tt>required</tt> to false.

### find_library ###

Tries to find the library specified in the positional argument. The result object can be used just like the return value of <tt>dependency</tt>. If the keyword argument <tt>required</tt> is false, Meson will proceed even if the library is not found. By default the library is searched for in the system specific library directory (e.g. <tt>/usr/lib</tt>). This can be overridden with the <tt>dirs</tt> keyword argument, which can be either a string or a list of strings.

### files ###

This command takes the strings given to it in arguments and returns corresponding File objects that you can use as sources for build targets. The difference is that file objects remember the subdirectory they were defined in and can be used anywhere in the source tree. As an example suppose you have source file <tt>foo.cpp</tt> in subdirectory <tt>bar1</tt> and you would like to use it in a build target that is defined in <tt>bar2</tt>. To make this happen you first create the object in <tt>bar1</tt> like this:

    foofile = files('foo.cpp')

Then you can use it in <tt>bar2</tt> like this:

    executable('myprog', 'myprog.cpp', foofile, ...)

Meson will then do the right thing.

### generator ###

This function creates a generator object that can be used to run custom compilation commands. The only positional argument is the executable to use. It can either be a self-built executable or one returned by find_program. Keyword arguments are the following:

- <tt>arguments</tt> list the command line arguments passed to the command
- <tt>output</tt> a template string defining how an output file name is generated from a source file name

### get_option

Obtains the value of the [project build option](Build options) specified in the positional argument.

### get_variable

This function can be used to dynamically obtain a variable. `res = get_variable(varname, fallback)` takes the value of `varname` (which must be a string) and stores the variable of that name into `res`. If the variable does not exist, the variable `fallback` is stored to `res`instead. If a fallback is not specified, then attempting to read a non-existing variable will cause a fatal error.

### gettext

Sets up gettext localisation so that translations are built and placed into their proper locations during install. Takes one positional argument which is the name of the gettext module. The list of languages that are to be generated are specified with the <tt>languages</tt> keyword argument.

### import

Imports the given extension module. Returns an opaque object that can be used to call the methods of the module. Here's an example for a hypothetical `testmod` module.

    tmod = import('testmod')
    tmod.do_something()

### include_directories ###

Returns an opaque object which contains the directories given in positional arguments. The result can then be used as a keyword argument when building executables or libraries. Both the source directory and the corresponding build directory are added. Note that this function call itself does not add the directories into the search path, since there is no global search path. You can use the the returned object in any subdirectory you want, Meson will make the paths work automatically. This function has one keyword argument `is_system` which, if set, flags the specified directories as system directories. This means that they will be used with the `-isystem` compiler argument rather than `-I` on compilers that support this flag (in practice everything except Visual Studio).

### install_data ###

Installs files listed in positional and <tt>sources</tt> keyword arguments into the directory specified by the <tt>install_dir</tt> argument during install phase.

### install_headers ###

Installs the specified headers into system's header directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument. If you just want to specify a subdirectory on top of the default source dir, then use the <tt>subdir</tt> argument. As an example if this has the value <tt>myproj</tt> then the headers would be installed to <tt>/prefix/include/myproj</tt>.

### install_man ###

Installs the man files specified into system's man directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument.

### install_subdir ###

Installs the entire given subdirectory tree to the location specified by the keyword argument <tt>install_dir</tt>. Note that due to implementation issues this command deletes the entire target dir before copying the files, so you should never use <tt>install_subdir</tt> to install into two overlapping directories (such as <tt>foo</tt> and <tt>foo/bar</tt>) because if you do the behaviour is undefined.

### is_subproject

Returns true if the current project is being built as a subproject of some other project and false otherwise.

### is_variable

`is_variable(varname)` returns true if a variable of the given name exists and false otherwise.

### jar

Build a jar from the specified Java source files. Keyword arguments are the same as executable's, with the addition of <tt>main_class</tt> which specifies the main class to execute when running the jar with <tt>java -jar file.jar</tt>.

### library

Builds a library that is either static or shared depending on the value of `default_library` user option. You should use this instead of `shared_library` or `static_library` most of the time. This allows you to toggle your entire project (including subprojects) from shared to static with only one option.

### message

This function prints its argument to stdout.

### project ###

The first argument to this function must be a string defining the name of this project. It must be followed by one or more programming languages that the project uses. Supported values for languages are `c`, `cpp` (for `C++`), `objc`, `objcpp`, `fortran`, `java`, `cs` (for `C#`) and `vala`.

The project name can be any string you want, it's not used for anything except descriptive purposes. However since it is written to e.g. the dependency manifest is usually makes sense to have it be the same as the project tarball or pkg-config name. So for example you would probably want to use the name _libfoobar_ instead of _The Foobar Library_.

You can specify a keyword argument `version`, which is a free form string describing the version of this project. You can access the value in your Meson build files with `meson.project_version()`.

Keyword argument 'subproject_dir` specifies the top level directory name that holds Meson subprojects. This is only meant as a compatibility option for existing code bases that house their embedded source code in a custom directory. All new projects should not set this but instead use the default value. It should be noted that this keyword argument is ignored inside subprojects. There can be only one subproject dir and it is set in the top level Meson file. 

The argument `meson_version` takes a string describing which Meson version the project requires. Usually something like `>0.28.0`. Similarly you can specify the license(s) the code is under with the `license` keyword argument. Usually this would be something like `license : 'GPL2+'`, but the code has multiple licenses you can specify them as an array like this: `license : ['proprietary', 'GPL3']`. Note that the text is informal and is only written to the dependency manifest. Meson does not do any license validation, you are responsible for verifying that you abide by all licensing terms.

You can specify default values for project options with the `default_options` keyword, which takes an array of strings. The strings are in the form `key=value` and have the same format as options to `mesonconf`. For example to set the default project type you would set this: `default_options : ['buildtype=debugoptimized']`. Note that these settings are only used when running Meson for the first time. They are also ignored in subprojects, only ones in the top level project are used.

### run_command ###

Runs the command specified in positional arguments. Returns an opaque object containing the result of the invocation.

### run_target ###

This function creates a new top level target that runs the command specified by positional arguments. The script is run from an unspecified directory, and Meson will set three environment variables <tt>MESON_SOURCE_ROOT</tt>, <tt>MESON_BUILD_ROOT</tt> and <tt>MESON_SUBDIR</tt> that specify the source directory, build directory and subdirectory the target was defined in, respectively.

### set_variable ###

Assigns a value to the given variable name. Calling <tt>set_variable('foo', bar)</tt> is equivalent to <tt>foo = bar</tt>.

### shared_library ###

Builds a shared library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt> with the following extra keyword arguments.

- `version` a string specifying the version of this shared library, such as *1.1.0*
- `soversion` a string specifying the soversion of this shared library, such as 0 
- `vs_module_defs` a string pointing to a file that contains Visual Studio symbol export definitions

### static_library ###

Builds a static library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt>

### subdir ###

Recurses into the specified subdirectory and executes the <tt>meson.build</tt> file in it. Once that is done, it returns and execution continues on the line following this <tt>subdir</tt> command.

### subproject

Takes the project specified in the positional argument and brings that in the current build specification. Subprojects must always be placed inside the `subprojects` directory at the top source directory. So for example a subproject called `foo` must be located in `${MESON_SOURCE_ROOT}/subprojects/foo`. You can specify the `version` keyword argument that works just like the one in `dependency`. It specifies what version the subproject should be, as an example `>=1.0.1`.

### test

Defines an unit test. Takes two positional arguments, the first is the name of this test and the second is the executable to run. Keyword arguments are the following.

- `args` arguments to pass to the executable
- `env` environment variables to set, such as `['NAME1=value1', 'NAME2=value2']`
- `is_parallel` when false, specifies that no other test must be running at the same time as this test
- `should_fail` when true the test is considered passed if the executable returns a non-zero return value (i.e. reports an error)
- `valgrind_args` if the test is run under Valgrind, pass these arguments to Valgrind (and not to the executable itself)
- `timeout` the amount of seconds the test is allowed to run, a test that exceeds its time limit is always considered failed, defaults to 30 seconds
- `workdir` absolute path that will be used as the working directory for the test

### vcs_tag ###

This command detects revision control commit information and places it in a specified file. This file is guaranteed to be up to date on every build. Keywords are similar to <tt>custom_command</tt> and all of them are mandatory.

- <tt>input</tt> file to modify (e.g. <tt>version.c.in</tt>)
- <tt>output</tt> file to write the results to (e.g. <tt>version.c</tt>)
- <tt>fallback</tt> version number to use when no revision control information is present, such as when building from a release tarball

Meson will read the contents of <tt>input</tt>, replace the string <tt>@VCS_TAG@</tt> with the detected revision number and write the result to <tt>output</tt>. This method returns an opaque object that you should put in your main program. If you desire more specific behaviour than what this command provides, you should use <tt>custom_command</tt>.

## Object methods ##

Meson has several different object types that have methods users can call. This section describes them.

### meson object ###

The <tt>meson</tt> object allows you to introspect various properties of the system. This object is always mapped in the <tt>meson</tt> variable. It has the following methods.

- <tt>get_compiler</tt> returns an object describing a compiler, takes one positional argument which is the language to use, and one keyword argument, <tt>native</tt> which when set to true makes Meson return the compiler for the build machine (the "native" compiler) and when false it returns the host compiler (the "cross" compiler)

- <tt>is_cross_build</tt> returns true if the current build is a cross build and false otherwise

- <tt>is_unity</tt> returns true when doing a unity build

- <tt>has_exe_wrapper</tt> returns true when doing a cross build if there is a wrapper command that can be used to execute cross built binaries (for example when cross compiling from Linux to Windows, one can use <tt>wine</tt> as the wrapper)

- <tt>add_install_script</tt> causes the script given as an argument to be run during the install step, this script will have the environment variables <tt>MESON_SOURCE_ROOT</tt>, <tt>MESON_BUILD_ROOT</tt> and <tt>MESON_INSTALL_PREFIX</tt> set

- `add_postconf_script` will run the executable given as an argument after all project files have been generated. This script will have the environment variables `MESON_SOURCE_ROOT` and `MESON_BUILD_ROOT` set. All additional arguments are passed as parameters.

- <tt>current_source_dir</tt> returns a string to the current source directory

- <tt>current_build_dir</tt> returns a string to the current build directory

- `source_root` returns a string with the absolute path to the source root directory

- `build_root` returns a string with the absolute path to the build root directory

- `project_version` returns the version string specified in `project` function call

### build target object

A build target is either an executable, shared or static library.

- <tt>extract_objects</tt> returns an opaque object representing the generated object files of arguments, usually used to take single object files and linking them to unit tests or compiling some source files with custom flags

- `extract_all_objects` is same as above but returns all object files generated by this target

- `private_dir_include` returns a opaque object that works like `include_directories` but points to the private directory of this target, usually only needed if an another target needs to access some generated internal headers of this target

### compiler object ###

This object represents a compiler for a given language and allows you to query its properties. It has the following methods.

- `get_id` returns a string identifying the compiler (e.g. *gcc*)
- `version` returns the compiler's version number as a string
- `compiles` returns true if the code fragment given in the positional argument compiles
- `sizeof` returns the size of the given type (e.g. *int*) or -1 if the type is unknown, to add includes set them in the `prefix` keyword argument
- `has_header` returns true if the specified header can be included
- `has_type` returns true if the specified token is a type
- `run` attempts to compile and execute the given code fragment, returns a run result object
- `has_function` returns true if the given function can be called
- `has_member` takes two arguments, type name and member name and returns true if the type has the specified member
- `alignment` returns the alignment of the type specified in the positional argument
- `has_header_symbol` allows one to detect whether a particular symbol (function, variable, #define, type definition, etc) is declared in the specified header.

The prefix keyword argument can be used to add #defines, #includes, etc that are required for the symbol to be declared (eg: #define _GNU_SOURCE is often required for some symbols to be exposed on Linux).

The args keyword argument can be used to pass a list of compiler arguments that are required to find the header or symbol. For example, you might need to pass the include path -Isome/path/to/header if the header is not in the default include path. Note that if you have a single prefix with all your dependencies, you might find it easier to append to the environment variables `C_INCLUDE_PATH` with gcc/clang and `INCLUDE` with msvc to expand the default include path.

### run result object ###

This object encapsulates the result of trying to compile and run a sample piece of code.

- `compiled` if true, the compilation succeeded, if false it did not and the other methods return unspecified data
- `returncode` the return code of executing the compiled binary
- `stdout` the standard out produced when the binary was run
- `stderr` the standard error produced when the binary was run

### configuration data object ###

This object encapsulates configuration values to be used for generating configuration files. It has two methods, <tt>set</tt> and <tt>set10</tt> which are fully documented on [the configuration wiki page](Configuration).

### dependency object ###

Contains an external dependency. This object has only one method, <tt>found</tt>, which returns whether the dependency was found.

### external program object ###

Contains an external (i.e. not built as part of this project) program. This object has the following methods:

- `found` which returns whether the executable was found
- `path` which returns a string pointing to the executable

### external library object ###

Contains an external (i.e. not built as part of this project) library. This object has only one method, <tt>found</tt>, which returns whether the library was found.

### generator object ###

This object contains a generator that is used to transform files from one type to another by an executable (e.g. idl files into source code and headers).

- <tt>process</tt> takes a list of files, causes them to be processed and returns an object containing the result which can then, for example, be passed into a build target definition. The keyword argument `extra_args`, if specified, will be used to replace an entry `@EXTRA_ARGS@` in the argument list.
