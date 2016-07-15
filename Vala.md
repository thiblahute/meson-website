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

## GObject Introspection

To generate GObject Introspection metadata, the --gir flags has to be set explicitly in vala_args.

    foo_lib = library('foo',
                      dependencies: [glib, gobject],
                      vala_args: ['--gir=Foo-1.0.gir'])

For the typelib, use a custom_target depending on the library:

    g_ir_compiler = find_program('g_ir_compiler')
    custom_target('foo-typelib',
                   command: [g_ir_compiler, '--output', '@OUTPUT@', meson.current_build_dir() + '/foo@sha/Foo-1.0.gir'],
                   output: 'Foo-1.0.typelib',
                   depends: foo_lib,
                   install: true,
                   install_dir: get_option('libdir') + '/girepository-1.0')

---

[Back to index](Manual)
