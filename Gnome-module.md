This module provides helper tools for build operations needed when building Gnome/GLib programs.

**Note**: the compilation commands here do not work properly when you change the source files. This is a bug in the respective compilers which do not expose the required dependency information. This has been reported upstream in [this bug](https://bugzilla.gnome.org/show_bug.cgi?id=745754). Until this is fixed you need to be careful when changing your source files.

## compile_resources

This function compiles resources specified in an XML file into code that can be embedded inside the main binary. Similar a build target it takes two positional arguments. The first one is the name of the resource and the second is the xml file containing the resource definitions. If the name is <tt>foobar</tt>, Meson will generate a header file called <tt>foobar.h</tt>, which you can then include in your sources. There are two keyword arguments.

* <tt>source_dir</tt>: a subdirectory where the resource compiler should look up the files, relative to the location of the xml file
* <tt>c_name</tt>: passed to the resource compiler as an argument after <tt>--c-name</tt>

Returns an opaque object that you should pass into your build target.

## generate_gir

Generates GObject introspection data. Takes one positional argument, the build target you want to build gir data for. There are several keyword arguments.

* `sources`: the list of sources to be scanned for gir data
* `nsversion`: namespace version
* `namespace`: the namespace for this gir object
* `install`: if true, install the generated gir file
* `install_dir`: which subdirectory to install the gir file into
* `dependencies`: deps to use during introspection scanning

This function returns nothing.

## compile_schemas

When called, this method will compile the gschemas in the current directory.

## gdbus_codegen

Compiles the given XML schema into gdbus source code. Takes two positional arguments, the first one specifies the name of the source files and the second specifies the XML file name. There are two keyword arguments, <tt>interface_prefix</tt> and <tt>namespace</tt> which map to corresponding features of the compiler.

Return value is an opaque object containing the source files. Add it to a top level target's source list.

---

Back to [module reference](Module reference).
