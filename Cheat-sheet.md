This page lists the commands to invoke to achieve some common build tasks with Meson. Unless otherwise specified all the examples below assume that the build directory is created in a directory called <tt>build</tt> which is located in the source tree's root. It is also assumed that all commands are executed in that directory.

## Producing a coverage report ##

First initialise the build directory with this command.

    meson --enable-gcov ..

Then issue the following commands.

    ninja
    ninja test
    ninja coverage-html (or coverage-xml)

The coverage report can be found in the meson-logs subdirectory.

## Using Clang and the static analyzer ##

Clang comes with a selection of analysis tools such as the [address sanitizer](http://clang.llvm.org/docs/AddressSanitizer.html). They are enabled by adding a few compiler flags. In addition we set the compiler to clang, though the sanitizers work with recent GCC versions, too.

First we set up meson.

    CC=clang CFLAGS='-fsanitize=address -fno-omit-frame-pointer' meson ..

This example uses only plain C. For C++ you would set the variables <tt>CXX</tt> and <tt>CXXFLAGS</tt>, respectively.

After this you just compile your code and run the test suite. Address sanitizer will abort executables which have errors so they show up as test failures.