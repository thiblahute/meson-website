This module provides helper tools for build operations needed when building Gnome/GLib programs.

**Note**: the compilation commands here might not work properly when you change the source files. This is a bug in the respective compilers which do not expose the required dependency information. This has been reported upstream in [this bug](https://bugzilla.gnome.org/show_bug.cgi?id=745754). Until this is fixed you need to be careful when changing your source files.

## compile_resources

This function compiles resources specified in an XML file into code that can be embedded inside the main binary. Similar a build target it takes two positional arguments. The first one is the name of the resource and the second is the xml file containing the resource definitions. If the name is `foobar`, Meson will generate a header file called `foobar.h`, which you can then include in your sources. There are two keyword arguments.

* `source_dir`: a subdirectory where the resource compiler should look up the files, relative to the location of the xml file
* `c_name`: passed to the resource compiler as an argument after `--c-name`
* `extra_args`: extra command line arguments to pass to the resource compiler

This function returns an array of two elements which are the c target and the header target.

## generate_gir

Generates GObject introspection data. Takes one positional argument, the build target you want to build gir data for. There are several keyword arguments. Many of these map directly to the `g-ir-scanner` tool so see its documentation for more information.

* `sources`: the list of sources to be scanned for gir data
* `nsversion`: namespace version
* `namespace`: the namespace for this gir object which determines output files
* `symbol_prefix`: the symbol prefix for the gir object, e.g. `gtk`
* `identifier_prefix`: the identifier prefix for the gir object, e.g. `Gtk`
* `export_packages`: extra packages the gir file exports
* `includes`: list of gir names to be included, can also be a GirTarget
* `dependencies`: extra dependencies for building the gir and typelib
* `link_with`: list of libraries to link with
* `include_directories`: extra include paths to look for gir files
* `install`: if true, install the generated files
* `install_dir_gir`: (*Added 0.35.0*) which directory to install the gir file into
* `install_dir_typelib`: (*Added 0.35.0*) which directory to install the typelib file into
* `dependencies`: deps to use during introspection scanning
* `extra_args`: command line arguments to pass to gir compiler

This function returns an array of two elements which are the gir target and the typelib target.

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
