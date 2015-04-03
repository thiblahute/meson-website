There are two different ways of invoking Meson. First, you can run it directly from the source tree with the command <tt>/path/to/source/meson.py</tt>. Meson may also be installed in which case the command is simply <tt>meson</tt>. In this manual we only use the latter format for simplicity.

At the time of writing only a command line version of Meson is available. This means that Meson must be invoked using the terminal. If you wish to use the MSVC compiler, you need to run Meson under "Visual Studio command prompt".

Configuring the source
==

Let us assume that we have a source tree that has a Meson build system. This means that at the topmost directory has a file called <tt>meson.build</tt>. We run the following commands to get the build started.

    cd /path/to/source/root
    mkdir build
    cd build
    meson ..

First we create a directory to hold all files generated during the build. Then we go into it and invoke Meson, giving it the location of the source root. Meson then loads the build configuration file and writes the corresponding build backend in the build directory. By default Meson generates a *debug build*, which turns on basic warnings and debug information and disables compiler optimizations. 

You can specify a different type of build with the <tt>--buildtype</tt> command line argument. It can have one of the following values.

value | meaning
------|--------
<tt>plain</tt> | no extra build flags are used, even for compiler warnings, useful for distro packagers and other cases where you need to specify all arguments by yourself
<tt>debug</tt> | debug info is generated but the result is not optimized, this is the default
<tt>debugoptimized</tt> | debug info is generated and the code is optimized (on most compilers this means <tt>-g -O2</tt>)
<tt>release</tt> | full optimization, no debug info

The build directory is mandatory. The reason for this is that it simplifies the build process immensely. Meson will not under any circumstances write files inside the source directory (if it does, it is a bug and should be fixed). This means that the user does not need to add a bunch of files to their revision control's ignore list. It also means that you can create arbitrarily many build directories for any given source tree. If we wanted to test building the source code with the Clang compiler instead of the system default, we could just type the following commands.

    cd /path/to/source/root
    mkdir buildclang
    cd buildclang
    CC=clang CXX=clang++ meson ..

This separation is even more powerful if your code has multiple configuration options (such as multiple data backends). You can create a separate subdirectory for each of them. You can also have build directories for optimized builds, code coverage, static analysis and so on. They are all neatly separated and use the same source tree. Changing between different configurations is just a question of changing to the corresponding directory.

Unless otherwise mentioned, all following command line invocations are meant to be run in the build directory.

By default Meson will use the Ninja backend to build your project. If you wish to use any of the other backends, you need to pass the corresponding argument during configuration time. As an example, here is how you would use Meson to generate a Visual studio solution.

    meson <source dir> <build dir> --backend=vs2010

You can then open the generated solution with Visual Studio an compile it in the usual way. A list of backends can be obtained with <tt>meson --help</tt>.

Building the source
==

If you are not using an IDE, Meson uses the [Ninja build system](http://martine.github.com/ninja/) to actually build the code. To start the build, simply type the following command.

    ninja

The main usability difference between Ninja and Make is that Ninja will automatically detect the number of CPUs in your computer and parallelize itself accordingly. You can override the amount of parallel processes used with the command line argument <tt>-j &lt;num processes&gt;</tt>.

It should be noted that after the initial configure step <tt>ninja</tt> is the only command you ever need to type to compile. No matter how you alter your source tree (short of moving it to a completely new location), Meson will detect the changes and regenerate itself accordingly. This is especially handy if you have multiple build directories. Often one of them is used for development (the "debug" build) and others only every now and then (such as a "static analysis" build). Any configuration can be built just by <tt>cd</tt>'ing to the corresponding directory and running Ninja.

Running tests
==

Meson provides native support for running tests. The command to do that is simple.

    ninja test

Meson does not force the use of any particular testing framework. You are free to use GTest, Boost Test, Check or even custom executables.

Installing
==

Installing the built software is just as simple.

    ninja install

By default Meson installs to <tt>/usr/local</tt>. This can be changed by passing the command line argument <tt>--prefix /your/prefix</tt> to Meson during configure time. Meson also supports the <tt>DESTDIR</tt> variable used in e.g. building packages. It is used like this:

    DESTDIR=/path/to/staging ninja install

Command line help
==

Meson comes with extensive command line help. It can be accessed with the following command.

    meson --help

---

[Back to index](Manual)