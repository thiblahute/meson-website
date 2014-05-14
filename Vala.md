Compiling Vala applications
==

Meson has experimental support for compiling Vala programs. A skeleton Vala file looks like this.

    project('valaprog', 'vala')
    
    glib = dependency('glib-2.0')
    gobject = dependency('gobject-2.0')

    executable('valaprog', 'prog.vala',
               deps : [glib, gobject])

You must always specify <tt>glib</tt> and <tt>gobject</tt> as dependencies, because all Vala applications use them.

---

[Back to index](Manual)
