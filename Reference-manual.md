This page lists functions and methods available in Meson scripts. For more in-depth documentation on how to use them, refer to the [manual](Manual).

## Functions ##

### add_global_arguments ###

Adds the positional arguments to the compiler command line for the language specified in <tt>language</tt> keyword argument. Note that there is no way to remove an argument set in this way. If you have an argument that is only used in a subset of targets, you have to specify it in per-target flags.

The arguments are used in all compiler invocations with the exception of compile tests, because you might need to run a compile test with and without the argument in question. For this reason only the arguments explicitly specified are used during compile tests.

### configuration_data ###

Creates an empty configuration object. You should add your configuration with its method calls and finally use it in a call to <tt>configure_file</tt>.

### configure_file ###

Takes a configuration file template and values and produces a file as specified in [the configuration file documentation](Configuration). The keyword arguments are the following:

- <tt>input</tt> the input file name
- <tt>output</tt> the output file name
- <tt>configuration</tt> the configuration data object as returned by <tt>configuration_data</tt>
- <tt>command</tt> if specified Meson does not create the file itself but rather runs the specified command, which allows you to do fully custom file generation

### custom_target ###

Create a custom top level build target. The only positional argument is the name of this target and the keyword arguments are the following.

- <tt>input</tt> list of source files
- <tt>output</tt> list of output files
- <tt>command</tt> command to run to create outputs from inputs (note: always specify commands in array form <tt>['commandname', '-arg1', '-arg2']</tt> rather than as a string <tt>'commandname -arg1 -arg2'</tt> as the latter will *not* work)
- <tt>install</tt> when true, this target is installed during the install step
- <tt>install_dir</tt> directory to install to
- <tt>build_always</tt> if <tt>true</tt> this target is always considered out of date and is rebuilt every time, useful for things such as build timestamps or revision control tags

### dependency ###

Finds an external dependency with the given name with pkg-config if possible and with fallback detection logic otherwise. Dependency supports two keyword arguments.

- <tt>modules</tt> specifies submodules to use for dependencies such as Qt5 or Boost.
- <tt>required</tt>, when set to false, Meson will proceed with the build even if the dependency is not found
- <tt>version</tt>, specifies the required version, a string containing a comparison operator followed by the version string, examples include <tt>&gt;1.0.0</tt>, <tt>&lt;=2.3.5</tt> or <tt>3.1.4</tt> for exact matching

### error ###

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

### find_program ###

Tries to locate the command listed in the positional argument. It can either be a command or a script in the source directory. Meson will also autodetect scripts with a shebang line and run them with the executable specified in it both on Windows (because the command invocator will reject the command otherwise) and unixes (if the script file does not have the executable bit set).

If the program is not found, Meson will abort. You can tell it not to by setting the keyword argument <tt>required</tt> to false.

### find_library ###

Tries to find the library specified in the positional argument. The result object can be used just like the return value of <tt>dependency</tt>. If the keyword argument <tt>required</tt> is false, Meson will proceed even if the library is not found.

### generator ###

This function creates a generator object that can be used to run custom compilation commands. The only positional argument is the executable to use. It can either be a self-built executable or one returned by find_program. Keyword arguments are the following:

- <tt>arguments</tt> list the command line arguments passed to the command
- <tt>output</tt> a template string defining how an output file name is generated from a source file name

### get_option ###

Obtains the value of the (project build option)[Build options] specified in the positional argument.

### gettext ###

Sets up gettext localisation so that translations are built and placed into their proper locations during install. Takes one positional argument which is the name of the gettext module. The list of languages that are to be generated are specified with the <tt>languages</tt> keyword argument.

### include_directories ###

Returns an opaque object which contains the directories given in positional arguments. The result can then be used as a keyword argument when building executables or libraries. Both the source directory and the corresponding build directory are added. Note that this function call itself does not add the directories into the search path, since there is no global search path. You can use the the returned object in any subdirectory you want, Meson will make the paths work automatically.

### install_data ###

Installs files listed in positional and <tt>sources</tt> keyword arguments into the directory specified by the <tt>install_dir</tt> argument during install phase.

### install_headers ###

Installs the specified headers into system's header directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument. If you just want to specify a subdirectory on top of the default source dir, then use the <tt>subdir</tt> argument. As an example if this has the value <tt>myproj</tt> then the headers would be installed to <tt>/prefix/include/myproj</tt>.

### install_man ###

Installs the man files specified into system's man directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument.

### install_subdir ###

Installs the entire given subdirectory tree to the location specified by the keyword argument <tt>install_dir</tt>. Note that due to implementation issues this command deletes the entire target dir before copying the files, so you should never use <tt>install_subdir</tt> to install into two overlapping directories (such as <tt>foo</tt> and <tt>foo/bar</tt>) because if you do the behaviour is undefined.

### is_subproject ###

Returns true if the current project is being built as a subproject of some other project and false otherwise.

### jar ###

Build a jar from the specified Java source files. Keyword arguments are the same as executable's, with the addition of <tt>main_class</tt> which specifies the main class to execute when running the jar with <tt>java -jar file.jar</tt>.

### message ###

This function prints its argument to stdout.

### pkgconfig_gen ###

A helper function to generate simple pkg-config files. For more complex pkg-config generation you should look into <tt>configure_file</tt>. The generated file's properties are specified with the following keyword arguments.

- <tt>libraries</tt>, a list of built libraries (usually results of shared_library) that the user needs to link against
- <tt>version</tt>, a string describing the version of this library
- <tt>name</tt>, the name of this library
- <tt>filebase</tt>, the base name to use for the pkg-config file, as an example the value of <tt>libfoo</tt> would produce a pkg-config file called <tt>libfoo.pc</tt>
- <tt>subdirs</tt> which subdirs of <tt>include</tt> should be added to the header search path, for example if you install headers into <tt>${PREFIX}/include/foobar-1</tt>, the correct value for this argument would be <tt>foobar-1</tt>

### project ###

The first argument to this function must be a string defining the name of this project. It must be followed by one or more programming languages that the project uses. Supported values for languages are <tt>c</tt>, <tt>cpp</tt> (for <tt>C++</tt>), <tt>objc</tt>, <tt>objcpp</tt>, <tt>fortran</tt>, <tt>java</tt>, <tt>cs</tt> (for <tt>C#</tt>) and <tt>vala</tt>.

### run_command ###

Runs the command specified in positional arguments. Returns an opaque object containing the result of the invocation.

### run_target ###

This function creates a new top level target that runs the command specified by positional arguments. The script is run from an unspecified directory, and Meson will set three environment variables <tt>MESON_SOURCE_ROOT</tt>, <tt>MESON_BUILD_ROOT</tt> and <tt>MESON_SUBDIR</tt> that specify the source directory, build directory and subdirectory the target was defined in, respectively.

### set_variable ###

Assigns a value to the given variable name. Calling <tt>set_variable('foo', bar)</tt> is equivalent to <tt>foo = bar</tt>.

### shared_library ###

Builds a shared library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt> with the following extra keyword arguments.

- <tt>version</tt> a string specifying the version of this shared library, such as *1.1.0*
- <tt>soversion</tt> a string specifying the soversion of this shared library, such as 0 

### static_library ###

Builds a static library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt>

### subdir ###

Recurses into the specified subdirectory and executes the <tt>meson.build</tt> file in it. Once that is done, it returns and execution continues on the line following this <tt>subdir</tt> command.

### subproject ###

Takes the project specified in the positional argument and brings that in the current build specification. Subprojects must always be placed inside the <tt>subprojects</tt> directory at the top source directory. So for example a subproject called <tt>foo</tt> must be located in <tt>${MESON_SOURCE_ROOT}/subprojects/foo</tt>.

### test ###

Defines an unit test. Takes two positional arguments, the first is the name of this test and the second is the executable to run. Keyword arguments are the following.

- <tt>args</tt> arguments to pass to the executable
- <tt>env</tt> environment variables to set, such as <tt>['NAME1=value1', 'NAME2=value2']</tt>
- <tt>is_parallel</tt> when false, specifies that no other test must be running at the same time as this test
- <tt>valgrind_args</tt> if the test is run under Valgrind, pass these arguments to Valgrind (and not to the executable itself)

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

- <tt>current_source_dir</tt> returns a string to the current source directory

- <tt>current_build_dir</tt> returns a string to the current build directory

- <tt>set_install_script</tt> causes the script given as an argument to be run during the install step, this script will have the environment variables <tt>MESON_SOURCE_ROOT</tt>, <tt>MESON_BUILD_ROOT</tt> and <tt>MESON_INSTALL_PREFIX</tt> set

### compiler object ###

This object represents a compiler for a given language and allows you to query its properties. It has the following methods.

- <tt>get_id</tt> returns a string identifying the compiler (e.g. *gcc*)
- <tt>version</tt> returns the compiler's version number as a string
- <tt>compiles</tt> returns true if the code fragment given in the positional argument compiles
- <tt>sizeof</tt> returns the size of the given type (e.g. *int*), to add includes set them in the <tt>prefix</tt> keyword argument
- <tt>has_header</tt> returns true if the specified header can be included
- <tt>run</tt> attempts to compile and execute the given code fragment, returns a run result object
- <tt>has_function</tt> returns true if the given function can be called
- <tt>has_member</tt> takes two arguments, type name and member name and returns true if the type has the specified member
- <tt>alignment</tt> returns the alignment of the type specified in the positional argument

### run result object ###

This object encapsulates the result of trying to compile and run a sample piece of code.

- <tt>compiled</tt> if true, the compilation succeeded, if false it did not and the other methods return unspecified data
- <tt>returncode</tt> the return code of executing the compiled binary
- <tt>stdout</tt> the standard out produced when the binary was run
- <tt>stderr</tt> the standard error produced when the binary was run

### configuration data object ###

This object encapsulates configuration values to be used for generating configuration files. It has two methods, <tt>set</tt> and <tt>set10</tt> which are fully documented on [the configuration wiki page](Configuration).

### dependency object ###

Contains an external dependency. This object has only one method, <tt>found</tt>, which returns whether the dependency was found.

### external program object ###

Contains an external (i.e. not built as part of this project) program. This object has only one method, <tt>found</tt>, which returns whether the executable was found.

### external library object ###

Contains an external (i.e. not built as part of this project) library. This object has only one method, <tt>found</tt>, which returns whether the library was found.

### generator object ###

This object contains a generator that is used to transform files from one type to another by an executable (e.g. idl files into source code and headers).

- <tt>process</tt> takes a list of files, causes them to be processed and returns an object containing the result which can then, for example, be passed into a build target definition
