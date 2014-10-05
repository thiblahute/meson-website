This page lists functions and methods available in Meson scripts. For more in-depth documentation on how to use them, refer to the [manual](Manual).

## Functions ##

### custom_target ###

Create a custom top level build target. The only positional argument is the name of this target and the keyword arguments are the following.

- <tt>input</tt> list of source files
- <tt>output</tt> list of output files
- <tt>command</tt> command to run to create outputs from inputs (note: always specify commands in array form <tt>['commandname', '-arg1', '-arg2']</tt> rather than as a string <tt>'commandname -arg1 -arg2'</tt> as the latter will *not* work)
- <tt>install</tt> when true, this target is installed during the install step
- <tt>install_dir</tt> directory to install to

### dependency ###

Finds an external dependency with the given name with pkg-config if possible and with fallback detection logic otherwise. Dependency supports one keyword argument, <tt>modules</tt>, which specifies submodules to use for dependencies such as Qt5 or Boost.

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

### generator ###

This function creates a generator object that can be used to run custom compilation commands. The only positional argument is the executable to use. It can either be a self-built executable or one returned by find_program. Keyword arguments are the following:

- <tt>arguments</tt> list the command line arguments passed to the command
- <tt>output</tt> a template string defining how an output file name is generated from a source file name

### headers ###

Installs the specified headers into system's header directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument.

### jar ###

Build a jar from the specified Java source files. Keyword arguments are the same as executable's, with the addition of <tt>main_class</tt> which specifies the main class to execute when running the jar with <tt>java -jar file.jar</tt>.

### man ###

Installs the man files specified into system's man directory during the install step. This directory can be overridden by specifying it with the <tt>install_dir</tt> keyword argument.

### message ###

This function prints its argument to stdout.

### project ###

The first argument to this function must be a string defining the name of this project. It must be followed by one or more programming languages that the project uses. Supported values for languages are <tt>c</tt>, <tt>cpp</tt> (for <tt>C++</tt>), <tt>objc</tt>, <tt>objcpp</tt>, <tt>fortran</tt>, <tt>java</tt>, <tt>cs</tt> (for <tt>C#</tt>) and <tt>vala</tt>.

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
