This module provides helper tools for build operations needed when building Gnome/GLib programs.

## compile_resources

This function compiles resources specified in an XML file into code that can be embedded inside the main binary. Similar a build target it takes two positional arguments. The first one is the name of the resource and the second is the xml file containing the resource definitions. If the name is <tt>foobar</tt> then Meson will generate a header file called <tt>foobar.h</tt>, which you can then include in your sources. There are two keyword arguments.

* <tt>source_dir</tt>: a subdirectory where the resource compiler should look up the files, relative to the location of the xml file
* <tt>c_name</tt>: passed to the resource compiler as an argument after <tt>--c-name</tt>

Returns an opaque object that you should pass into your build target.

---

Back to [module reference](Module reference).
