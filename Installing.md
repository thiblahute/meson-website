By default Meson will not install anything. Build targets can be installed by tagging them as installable in the definition.

    project('install', 'c')
    shared_library('mylib', 'libfile.c', install : true)

There is usually no need to specify install paths or the like. Meson will automatically install it to the standards-conforming location. In this particular case the executable is installed to the <tt>bin</tt> subdirectory of the install prefix. However if you wish to override the install dir, you can do that with the <tt>install_dir</tt> argument.

    executable('prog', 'prog.c', install : true, install_dir : 'my/special/dir')

Other install commands are the following.

    headers('header.h', subdir : 'projname') # -> include/projname/header.h
    man('foo.1') # -> share/man/man1/foo.1.gz
    data('progname', sources : 'datafile.cat') # -> share/progname/datafile.dat

---

[Back to index](Manual).