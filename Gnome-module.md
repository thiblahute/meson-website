This module provides helper tools for build operations needed when building Gnome/GLib programs.

**Note**: the compilation commands here do not work properly when you change the source files. This is a bug in the respective compilers which do not expose the required dependency information. This has been reported upstream in [this bug](https://bugzilla.gnome.org/show_bug.cgi?id=745754). Until this is fixed you need to be careful when changing your source files.

## compile_resources

This function compiles resources specified in an XML file into code that can be embedded inside the main binary. Similar a build target it takes two positional arguments. The first one is the name of the resource and the second is the xml file containing the resource definitions. If the name is <tt>foobar</tt>, Meson will generate a header file called <tt>foobar.h</tt>, which you can then include in your sources. There are two keyword arguments.

* <tt>source_dir</tt>: a subdirectory where the resource compiler should look up the files, relative to the location of the xml file
* <tt>c_name</tt>: passed to the resource compiler as an argument after <tt>--c-name</tt>

Returns an opaque object that you should pass into your build target.

## generate_gir

Generates GObject introspection data. Takes one positional argument, the build target you want to build gir data for. There are several keyword arguments.

* <tt>sources</tt>: the list of sources to be scanned for gir data
* <tt>nsversion</tt>: namespace version
* <tt>namespace</tt>: the namespace for this gir object
* <tt>install</tt>: if true, install the generated gir file
* <tt>install_dir</tt>: which subdirectory to install the gir file into

This function returns nothing.


---

Back to [module reference](Module reference).
