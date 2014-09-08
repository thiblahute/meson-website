# An in-depth tutorial of Meson #

In this tutorial we set up a project with multiple targets, unit tests and dependencies between targets. Our main product is a shared library called *foo* that is written in <tt>C++11</tt>. We are going to ignore the contents of the source files, as they are not really important from a build definition point of view.

The source tree contains three subdirectories <tt>src</tt>, <tt>include</tt> and <tt>test</tt> that contain, respectively, the source code, headers and unit tests of our project.

To start things up, here is the top level <tt>meson.build</tt> file.

    project('c++ foolib', 'cpp')
    add_global_arguments('-std=c++11', language : 'cpp')

    inc = include_directories('include')
    subdir('src')
    subdir('test')

First we define the project's name and the programmin languages it uses (in this case only <tt>C++</tt>). Then we add a global compiler argument <tt>-std=c++11</tt>. This flag is used for *all* C++ source file compilations. It is not possible to unset it for some targets. The reason for this is that it is hard to keep track of what compiler flags are in use if global settings change per target.

Since <tt>include</tt> directory contains the header files, we need a way to tell compilations to add that directory to the compiler command line. This is done with the <tt>include_directories</tt> command that takes a directory and returns an object representing this directory. It is stored in variable <tt>inc</tt> which makes it accessible later on.

After this are two <tt>subdir</tt> commands. These instruct Meson to go to the specified subdirectory, open the <tt>meson.build</tt> file that's in there and execute it.
