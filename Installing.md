By default Meson will not install anything. Build targets can be installed by tagging them as installable in the definition.

    project('install', 'c')
    shared_library('mylib', 'libfile.c', install : true)

There is usually no need to specify install paths or the like. Meson will automatically install it to the standards-conforming location. In this particular case the executable is installed to the <tt>bin</tt> subdirectory of the install prefix. However if you wish to override the install dir, you can do that with the <tt>install_dir</tt> argument.

    executable('prog', 'prog.c', install : true, install_dir : 'my/special/dir')

Other install commands are the following.

    install_headers('header.h', subdir : 'projname') # -> include/projname/header.h
    install_man('foo.1') # -> share/man/man1/foo.1.gz
    install_data('datafile.cat', install_dir : 'share/progname') # -> share/progname/datafile.dat

Sometimes you want to copy an entire subtree directly. For this use case there is the <tt>install_subdir</tt> command, which can be used like this.

    install_subdir('mydir', install_dir : 'include') # mydir subtree -> include/mydir

Most of the time you want to install files relative to the install prefix. Sometimes you need to go outside of the prefix (such as writing files to <tt>/etc</tt> instead of <tt>/usr/etc</tt>. This can be accomplished by giving an absolute install path.

    install_data('foobar', sources : 'foo.dat', install_dir : '/etc') # -> /etc/foo.dat

## Custom install behaviour ##

Sometimes you need to do more than just install basic targets. Meson makes this easy by allowing you to specify a custom script to execute at install time. As an example, here is a script that generates an empty file in a custom directory.

    #!/bin/sh

    mkdir "${DESTDIR}/${MESON_INSTALL_PREFIX}/mydir"
    touch "${DESTDIR}/${MESON_INSTALL_PREFIX}/mydir/file.dat"

As you can see, Meson sets up some environment variables to help you write your script (<tt>DESTDIR</tt> is not set by Meson, it is inherited from the outside environment). In addition to the install prefix, Meson also sets the variables <tt>MESON_SOURCE_ROOT</tt> and <tt>MESON_BUILD_ROOT</tt>.

Telling Meson to run this script at install time is a one-liner.

    meson.set_install_script('myscript.sh')

The argument is the name of the script file relative to the current subdirectory.

## DESTDIR support ##

Sometimes you need to install to a different directory than the install prefix. This is most common when building rpm or deb packages. This is done with the <tt>DESTDIR</tt> environment variable and it is used just like with other build systems:

    DESTDIR=/path/to/staging/area ninja install

---

[Back to index](Manual).