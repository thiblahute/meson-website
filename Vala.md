Compiling Vala applications
==

Meson has experimental support for compiling Vala programs. A skeleton Vala file looks like this.

    project('valaprog', ['vala', 'c'])
    
    glib = dependency('glib-2.0')
    gobject = dependency('gobject-2.0')

    executable('valaprog', 'prog.vala',
               dependencies : [glib, gobject])

You must always specify `glib` and `gobject` as dependencies, because all Vala applications use them.

---

[Back to index](Manual)
