This page lists functions and methods available in Meson scripts. For more in-depth documentation on how to use them, refer to the [manual](Manual).

## Functions ##

### dependency ###

Finds an external dependency with the given name with pkg-config if possible and with fallback detection logic otherwise. Dependency supports one keyword argument, <tt>modules</tt>, which specifies submodules to use for dependencies such as Qt5 or Boost.

### error ###

Print the argument string and halts the build process.

### executable ###

Creates a new executable. The first argument specifies its name and the remaining positional arguments define the source files to use.

Executable supports the following keyword arguments.

- <tt>install</tt>, when set to true, this executable should be installed
- <tt>link_with</tt>, one or more shared or static libraries (built by this project) that this target should be linked with
- <tt>&lt;languagename&gt;_pch</tt> precompiled header fire to use for the given language
- <tt>&lt;languagename&gt;_args</tt> compiler flags to use for the given language
- <tt>link_args</tt> flags to use during linking
- <tt>link_depends</tt> an extra file that the link step depends on such as a symbol visibility map
- <tt>include_directories</tt> one or more objects created with the <tt>include_directories</tt> function
- <tt>dependencies</tt> one or more objects created with <tt>dependency</tt> or <tt>find_library</tt>
- <tt>gui_app</tt> when set to true flags this target as a GUI application on platforms where this makes a difference (e.g. Windows)
- <tt>extra_files</tt> are not used for the build itself but are shown as source files in IDEs that group files by targets (such as Visual Studio)
- <tt>install_rpath</tt> a string to set the target's rpath to after install (but *not* before that)

### jar ###

Build a jar from the specified Java source files. Keyword arguments are the same as executable's, with the addition of <tt>main_class</tt> which specifies the main class to execute when running the jar with <tt>java -jar file.jar</tt>.

### message ###

This function prints its argument to stdout.

### project ###

The first argument to this function must be a string defining the name of this project. It must be followed by one or more programming languages that the project uses. Supported values for languages are <tt>c</tt>, <tt>cpp</tt> (for <tt>C++</tt>), <tt>objc</tt>, <tt>objcpp</tt>, <tt>fortran</tt>, <tt>java</tt>, <tt>cs</tt> (for <tt>C#</tt>) and <tt>vala</tt>.

### shared_library ###

Builds a shared library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt> with the following extra keyword arguments.

- <tt>version</tt> a string specifying the version of this shared library, such as *1.1.0*
- <tt>soversion</tt> a string specifying the soversion of this shared library, such as 0 

### static_library ###

Builds a static library with the given sources. Positional and keyword arguments are the same as for <tt>executable</tt>
