# An in-depth tutorial of Meson #

In this tutorial we set up a project with multiple targets, unit tests and dependencies between targets. Our main product is a shared library called *foo* that is written in <tt>C++11</tt>. We are going to ignore the contents of the source files, as they are not really important from a build definition point of view.

The source tree contains three subdirectories <tt>src</tt>, <tt>include</tt> and <tt>test</tt> that contain, respectively, the source code, headers and unit tests of our project.

To start things up, here is the top level <tt>meson.build</tt> file.

    project('c++ foolib', 'cpp')
    add_global_arguments('-std=c++11', language : 'cpp')

    inc = include_directories('include')
    subdir('src')
    subdir('test')

First we define the project's name and the programmin languages it uses (in this case only <tt>C++</tt>). 