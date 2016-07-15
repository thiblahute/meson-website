## Compiling Vala applications

Meson has experimental support for compiling Vala programs. A skeleton Vala file looks like this.

    project('valaprog', ['vala', 'c'])
    
    glib = dependency('glib-2.0')
    gobject = dependency('gobject-2.0')

    executable('valaprog', 'prog.vala',
               dependencies : [glib, gobject])

You must always specify `glib` and `gobject` as dependencies, because all Vala applications use them.

## Using a custom VAPI

When dealing with libraries that are not providing Vala bindings, you can point --vapidir to a directory relative to meson.current_source_dir containing the binding and include a --pkg flag.

    glib = dependency('glib-2.0')
    gobject = dependency('gobject-2.0')
    foo = dependency('foo')
    
    executable('app',
               dependencies: [glib, gobject, foo]
               vala_args: ['--pkg=foo', '--vapidir=' + meson.current_source_dir()])

---

[Back to index](Manual)
