Using Meson
==

Meson has been designed to be as easy to use as possible. This page outlines the basic use cases. For more advanced cases refer to Meson's command line help which is accessible with the command <tt>meson.py --help</tt>.

Requirements
--

Meson has two main dependencies.

* [Python 3](http://python.org)
* [Ninja](http://martine.github.com/ninja/)

Ninja is only needed if you use the Ninja backend. Meson can also generate native VS and XCode project files.

On Ubuntu these can be easily installed with the following command:

    sudo apt-get install python3 ninja-build

Compiling a Meson project
--

The most common use case of Meson is compiling code on a code base you are working on. The steps to take are very simple.

    cd /path/to/source/root
    mkdir build
    cd build
    meson ..
    ninja
    ninja test

The only thing to note is that you need to create a separate build directory. Meson will not allow you to build source code inside your source tree. All build artifacts are stored in the build directory. This allows you to have multiple build trees with different configurations at the same time. This way generated files are not added into revision control by accident. 

To recompile after code changes, just type <tt>ninja</tt>. The build command is always the same. You can do arbitrary changes to source code and build system files and Meson will detect those and will do the right thing. If you want to build optimized binaries, just use the argument <tt>--buildtype=debugoptimized</tt> when running Meson. It is recommended that you keep one build directory for unoptimized builds and one for optimized ones. To compile any given configuration, just go into the corresponding build directory and run <tt>ninja</tt>.

Meson will automatically add compiler flags to enable debug information and compiler warnings (i.e. <tt>-g</tt> and <tt>-Wall</tt>). This means the user does not have to deal with them and can instead focus on coding.

Using Meson as a distro packager
--

Distro packagers usually want total control on the build flags used. Meson supports this use case natively. The commands needed to build and install Meson projects are the following.

    cd /path/to/source/root
    mkdir build
    cd build
    CFLAGS=... CXXFLAGS=... LDFLAGS=.. meson --prefix /usr --buildtype=plain
    ninja
    ninja test
    DESTDIR=/path/to/staging/root ninja install

The command line switch <tt>--buildtype=plain</tt> tells Meson not to add its own flags to the command line. This gives the packager total control on used flags.

This is very similar to other build systems. The only difference is that the <tt>DESTDIR</tt> variable is passed as an environment variable rather than as an argument to <tt>ninja install</tt>.

As distro builds happen always from scratch, we recommend you to enable [unity builds](Unity builds) whenever possible on your packages because they are faster and produce better code.