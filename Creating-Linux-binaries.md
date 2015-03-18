Creating Linux binaries that can be downloaded and run on any distro (like .dmg packages for OSX or .exe installers for Windows) has traditionally been difficult. This is even more tricky if you want to use modern compilers and features, which is especially desired in game development. There is still no simple turn-key solution for this problem but after a bit of setup it can be relatively straightforward.

## Installing system and GCC

First you need to do a fresh operating system install. You can use spare hardware, VirtualBox, cloud or whatever you want. Note that the distro you install must be *at least as old* as the oldest release you wish to support. Debian stable is usually a good choice, though immediately after its release you might want to use Debian oldstable or the previous Ubuntu LTS. The oldest supported version of CentOS is also a good choice.

Once you have installed the system, you need to install build-dependencies for GCC. In Debian-based distros this can be done with the following commands:

    apt-get build-dep g++
    apt-get install pkg-config libgmp-dev libmpfr-dev libmpc-dev

Then create a <tt>src</tt> subdirectory in your home directory. Copypaste the following into <tt>install_gcc.sh</tt> and execute it.

    #!/bin/sh

    wget ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/gcc-4.9.2/gcc-4.9.2.tar.bz2
    tar xf gcc-4.9.2.tar.bz2

    mkdir objdir
    cd objdir
    ../gcc-4.9.2/configure --disable-bootstrap --prefix=${HOME}/devroot \
                           --disable-multilib --enable-languages=c,c++
    make -j 4
    make install-strip
    ln -s gcc ${HOME}/devroot/bin/cc

Then finally add the following lines to your <tt>.bashrc</tt>.

    export LD_LIBRARY_PATH=${HOME}/devroot/lib
    export PATH=${HOME}/devroot/bin:$PATH
    export PKG_CONFIG_PATH=${HOME}/devroot/lib/pkgconfig

Log out and back in and now your build environment is ready to use.

## Adding dependencies

For dependencies you want to embed and statically link everything you can (especially C++ dependencies). Meson's [Wrap package manager might be of use here](https://groups.google.com/forum/#!topic/mesonbuild/DliVv-mjOTk). This is equivalent to what you would do on Windows, OSX, Android etc. Sometimes static linking is not possible. In these cases you need to copy the .so files inside your package. Let's use SDL2 as an example. First we download and install it as usual giving it our custom install prefix (that is, <tt>./configure --prefix=${HOME}/devroot</tt>)

## Building and installing

Building happens in much the same way as normally. There are just two things to note. First, you must tell GCC to link the C++ standard library statically. If you don't then your app is guaranteed to break as different distros have binary-incompatible C++ libraries. The second thing is that you need to point your install prefix to some empty staging area. Here's the meson command to do that:

    LDFLAGS=-static-libstdc++ meson --prefix=/tmp/myapp <other args>

The aim is to put the executable in <tt>/tmp/myapp/bin</tt> and shared libraries to <tt>/tmp/myapp/lib</tt>. The next thing you need is the embedder. It takes your dependencies (in this case only <tt>libSDL2-2.0.so.0</tt> and copies them in the lib directory. Depending on your use case you can either copy the files by hand or write a script that parses the output of <tt>ldd binary_file</tt>. Be sure not to copy system libraries (<tt>libc</tt>, <tt>libpthread</tt>, <tt>libm</tt> etc). For an example, see the [sample project](https://github.com/jpakkane/meson/tree/master/manual%20tests/3%20standalone%20binaries).

Make the script run during install with this:

     meson.set_install_script('linux_bundler.sh')

## Final steps

If you try to run the program now it will most likely fail to start or crashes. The reason for this is that the system does not know that the executable needs libraries from the <tt>lib</tt> directory. The solution for this is a simple wrapper script. Create a script called <tt>myapp.sh</tt> with the following content:

    #!/bin/bash

    cd "${0%/*}"
    export LD_LIBRARY_PATH="`pwd`/lib"
    bin/myapp

Install it with this Meson snippet:

    install_data('myapp.sh', install_dir : '.')

And now you are done. Zip up your <tt>/tmp/myapp</tt> directory and you have a working binary ready for deployment. To run the program, just unzip the file and run <tt>myapp.sh</tt>.
 
---

[Back to index](Manual).