This page lists the commands to invoke to achieve some common build tasks with Meson. Unless otherwise specified all the examples below assume that the build directory is created in a directory called <tt>build</tt> which is located in the source tree's root. It is also assumed that all commands are executed in that directory.

## Producing a coverage report ##

First initialise the build directory with this command.

    meson --enable-gcov ..

Then issue the following commands.

    ninja
    ninja test
    ninja coverage-html (or coverage-xml)

The result can be found in the meson-logs subdirectory.
