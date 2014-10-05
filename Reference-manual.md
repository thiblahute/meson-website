This page lists functions and methods available in Meson scripts. For more in-depth documentation on how to use them, refer to the [manual](Manual).

## Functions ##

### add_global_arguments ###

Adds the positional arguments to the compiler command line for the language specified in <tt>language</tt> keyword argument. Note that there is no way to remove an argument set in this way. If you have an argument that is only used in a subset of targets, you have to specify it in per-target flags.

The arguments are used in all compiler invocations with the exception of compile tests, because you might need to run a compile test with and without the argument in question. For this reason only the arguments explicitly specified are used during compile tests.

### configuration_data ###

Creates an empty configuration object. You should add your configuration with its method calls and finally use it in a call to <tt>configure_file</tt>.

### configure_file ###

Takes a configuration file template and values and produces a file as specified in [the configuration file documentation](Configuration). The keyword arguments are the following:

-<tt>input</tt> the input file name
-<tt>output</tt> the output file name
-<tt>configuration</tt> the configuration data object as returned by <tt>configuration_data</tt>
-<tt>command</tt> if specified Meson does not create the file itself but rather runs the specified command, which allows you to do fully custom file generation

### custom_target ###

Create a custom top level build target. The only positional argument is the name of this target and the keyword arguments are the following.

- <tt>input</tt> list of source files
- <tt>output</tt> list of output files
- <tt>command</tt> command to run to create outputs from inputs (note: always specify commands in array form <tt>['commandname', '-arg1', '-arg2']</tt> rather than as a string <tt>'commandname -arg1 -arg2'</tt> as the latter will *not* work)
- <tt>install</tt> when true, this target is installed during the install step
- <tt>install_dir</tt> directory to install to

### data ###

Installs files listed in positional and <tt>sources</tt> keyword arguments into the directory specified by the <tt>install_dir</tt> argument during install phase.

### dependency ###

Finds an external dependency with the given name with pkg-config if possible and with fallback detection logic otherwise. Dependency supports two keyword arguments.

- <tt>modules</tt> specifies submodules to use for dependencies such as Qt5 or Boost.
- <tt>required</tt>, when set to false, Meson will proceed with the build even if the dependency is not found

### error ###

Print the argument string and halts the build process.

### executable ###

Creates a new executable. The first argument specifies its name and the remaining positional arguments define the source files to use.

Executable supports the following keyword arguments.

- <tt>link_with</tt>, one or more shared or static libraries (built by this project) that this target should be linked with
- <tt>&lt;languagename&gt;_pch</tt> precompiled header fire to use for the given language
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

### headers ###

Installs the specified headers into system's header directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument.

### include_directories ###

Returns an opaque object which contains the directories given in positional arguments. The result can then be used as a keyword argument when building executables or libraries. Both the source directory and the corresponding build directory are added. Note that this function call itself does not add the directories into the search path, since there is no global search path. You can use the the returned object in any subdirectory you want, Meson will make the paths work automatically.

### jar ###

Build a jar from the specified Java source files. Keyword arguments are the same as executable's, with the addition of <tt>main_class</tt> which specifies the main class to execute when running the jar with <tt>java -jar file.jar</tt>.

### man ###

Installs the man files specified into system's man directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument.

### message ###

This function prints its argument to stdout.

### project ###

The first argument to this function must be a string defining the name of this project. It must be followed by one or more programming languages that the project uses. Supported values for languages are <tt>c</tt>, <tt>cpp</tt> (for <tt>C++</tt>), <tt>objc</tt>, <tt>objcpp</tt>, <tt>fortran</tt>, <tt>java</tt>, <tt>cs</tt> (for <tt>C#</tt>) and <tt>vala</tt>.

### run_command ###

Runs the command specified in positional arguments. Returns an opaque object containing the result of the invocation.

### run_target ###

This function creates a new top level target that runs the command specified by positional arguments. The script is run from an unspecified directory, and Meson will set three environment variables <tt>MESON_SOURCE_ROOT</tt>, <tt>MESON_BUILD_ROOT</tt> and <tt>MESON_SUBDIR</tt> that specify the source directory, build directory and subdirectory the target was defined in, respectively.

### shared_library ###

Builds a shared library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt> with the following extra keyword arguments.

- <tt>version</tt> a string specifying the version of this shared library, such as *1.1.0*
- <tt>soversion</tt> a string specifying the soversion of this shared library, such as 0 

### static_library ###

Builds a static library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt>

### subdir ###

Recurses into the specified subdirectory and executes the <tt>meson.build</tt> file in it. Once that is done, it returns and execution continues on the line following this <tt>subdir</tt> command.

### test ###

Defines an unit test. Takes two positional arguments, the first is the name of this test and the second is the executable to run. Keyword arguments are the following.

- <tt>args</tt> arguments to pass to the executable
- <tt>env</tt> environment variables to set, such as <tt>['NAME1=value1', 'NAME2=value2']</tt>
- <tt>is_parallel</tt> when false, specifies that no other test must be running at the same time as this test
- <tt>valgrind_args</tt> if the test is run under Valgrind, pass these arguments to Valgrind (and not to the executable itself)
