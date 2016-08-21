This module provides helper tools for build operations needed when building Gnome/GLib programs.

**Note**: the compilation commands here might not work properly when you change the source files. This is a bug in the respective compilers which do not expose the required dependency information. This has been reported upstream in [this bug](https://bugzilla.gnome.org/show_bug.cgi?id=745754). Until this is fixed you need to be careful when changing your source files.

## compile_resources

This function compiles resources specified in an XML file into code that can be embedded inside the main binary. Similar a build target it takes two positional arguments. The first one is the name of the resource and the second is the xml file containing the resource definitions. If the name is `foobar`, Meson will generate a header file called `foobar.h`, which you can then include in your sources. There are two keyword arguments.

* `source_dir`: a subdirectory where the resource compiler should look up the files, relative to the location of the xml file
* `c_name`: passed to the resource compiler as an argument after `--c-name`
* `extra_args`: extra command line arguments to pass to the resource compiler

Returns an opaque object that you should pass into your build target.

## generate_gir

Generates GObject introspection data. Takes one positional argument, the build target you want to build gir data for. There are several keyword arguments.

* `sources`: the list of sources to be scanned for gir data
* `nsversion`: namespace version
* `namespace`: the namespace for this gir object
* `install`: if true, install the generated gir file
* `install_dir`: which subdirectory to install the gir file into
* `dependencies`: deps to use during introspection scanning
* `extra_args`: command line arguments to pass to gir compiler

This function returns nothing.

## compile_schemas

When called, this method will compile the gschemas in the current directory.

## gdbus_codegen

Compiles the given XML schema into gdbus source code. Takes two positional arguments, the first one specifies the name of the source files and the second specifies the XML file name. There are two keyword arguments, `interface_prefix` and `namespace` which map to corresponding features of the compiler.

Return value is an opaque object containing the source files. Add it to a top level target's source list.

## gtkdoc

Compiles and installs gtkdoc documentation. Takes two positional arguments. The first one is the name for this target and the second is the directory containing sources. Keyword arguments are `main_sgml`which specifies the main sgml (or xml) file, `install` which, if true, installs the generated docs and `scan_args` and `html_args` for extra arguments to pass to `gtkdoc-scan` and `gtkdoc-mkhtml`, respectively.

## gtkdoc_html_dir

Takes as argument a module name and returns the path where that module's HTML files will be installed. Usually used with `install_data` to install extra files, such as images, to the output directory.

---

Back to [module reference](Module reference).
