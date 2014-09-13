# An in-depth tutorial of Meson #

In this tutorial we set up a project with multiple targets, unit tests and dependencies between targets. Our main product is a shared library called *foo* that is written in <tt>C++11</tt>. We are going to ignore the contents of the source files, as they are not really important from a build definition point of view. The library makes use of the <tt>GLib</tt> library so we need to detect and link it properly. We also make the resulting library installable.

The source tree contains three subdirectories <tt>src</tt>, <tt>include</tt> and <tt>test</tt> that contain, respectively, the source code, headers and unit tests of our project.

To start things up, here is the top level <tt>meson.build</tt> file.

    project('c++ foolib', 'cpp')
    add_global_arguments('-std=c++11', language : 'cpp')
    glib_dep = dependency('glib-2.0')

    inc = include_directories('include')
    subdir('include')
    subdir('src')
    subdir('test')

    pkgconfig_gen(libraries : foolib,
                  version : '1.0',
                  name : 'libfoobar',
                  filebase : 'foobar',
                  description : 'A Library to a barnicator for your foos.')

First we define the project's name and the programmin languages it uses (in this case only <tt>C++</tt>). Then we find GLib, which is an *external dependency*. The <tt>dependency</tt> function tells Meson to find the library (by default using <tt>pkg-config</tt>). If the library is not found, Meson will raise an error and stop processing the build definition.

Then we add a global compiler argument <tt>-std=c++11</tt>. This flag is used for *all* C++ source file compilations. It is not possible to unset it for some targets. The reason for this is that it is hard to keep track of what compiler flags are in use if global settings change per target.

Since <tt>include</tt> directory contains the header files, we need a way to tell compilations to add that directory to the compiler command line. This is done with the <tt>include_directories</tt> command that takes a directory and returns an object representing this directory. It is stored in variable <tt>inc</tt> which makes it accessible later on.

After this are three <tt>subdir</tt> commands. These instruct Meson to go to the specified subdirectory, open the <tt>meson.build</tt> file that's in there and execute it. The last line is a stanza to generate a <tt>pkg-config</tt> file. We'll skip that for now and come back to it at the end.

The first subdirectory we go into is <tt>include</tt>. In it we have a a header file for the library that we want to install. This requires one line.

    headers('foolib.h')

This installs the given header file to the system's header directory. This is by default <tt>/[install prefix]/include</tt>, but it can be changed with a command line argument.

The Meson definition of <tt>src</tt> subdir is simple.

    foolib = shared_library('foo', 'source1.cpp', 'source2.cpp',
                            include_directories : inc,
                            dependencies : glib_dep,
                            install : true)

Here we just tell Meson to build the library with the given sources. We also tell it to use the include directories we stored to variable <tt>inc</tt> earlier. Since this library uses GLib, we tell Meson to add all necessary compiler and linker flags with the <tt>dependencies</tt> keyword argument. Its value is <tt>glib_dep</tt> which we set at the top level <tt>meson.build</tt> file. The <tt>install</tt> argument tells Meson to install the result. As with the headers, the shared library is installed to the system's default location (usually <tt>/[install prefix]/lib</tt> but is again overridable.

The resulting library is stored in variable <tt>foolib</tt> just like the include directory was stored in the previous file.

Once Meson has processed the <tt>src</tt> subdir it returns one level up to the main Meson file and executes the next line that moves it into the <tt>test</tt> subdir. Its contents look like this.

    testexe = executable('testexe', 'footest.cpp',
                         include_directories : inc,
                         link_with : foolib)
    test('foolib test', testexe)

First we build a test executable that has the same include directory as the main library and which also links against the freshly built shared library. Note that you don't need to specify <tt>glib_dep</tt> here just to be able to use the built library <tt>foolib</tt>. If the executable used GLib functionality itself, then we would of course need to add it as a keyword argument here.

Finally we define a test with the name <tt>foolib test</tt>. It consists of running the binary we just built. If the executable exits with a zero return value, the test is considered passed. Nonzero return values mark the test as failed.

At this point we can return to the pkg-config generator line. All shared libraries should provide a pkg-config file, which explains how that library is used. Meson provides this simple generator that should be sufficient for most simple projects. All you need to do is list a few basic pieces of information and Meson takes care of generating an appropriate file. More advanced users might want to create their own pkg-config files using Meson's [configuration file generator system](Configuration).

With these four files we are done. To configure, build and run the test suite, we just need to execute the following commands (starting at source tree root directory).

    mkdir build
    cd build
    meson ..
    ninja
    ninja test

To then install the project you only need one command.

    ninja install

