Meson has full support for cross compilation. Since cross compiling is more complicated than native building, Meson requires you to write a cross build definition file. It defines various properties of the cross build environment. Here is an example file for cross compiling Windows applications on Linux.

    name = 'windows'
    c = '/usr/bin/i586-mingw32msvc-gcc'
    cpp = '/usr/bin/i586-mingw32msvc-g++'
    ar = '/usr/i586-mingw32msvc/bin/ar'
    strip = '/usr/i586-mingw32msvc/bin/strip'
    exe_wrapper = 'wine' # A command used to run generated executables.

The first argument is called *name* and it mandatory. It defines the target platform's OS type. In cross-building terminology the target platform is called the *host*, whereas the platform doing the compilation is, confusingly, called *build*. Typical values for name include *linux* or *darwin* for OSX. Then the file defines compilers, linkers and so on to use when compiling for this host. 

The last line is special. It defines a *wrapper command* that can be used to run executables for this host. In this case we can use Wine, which runs Windows applications on Linux. Other choices include running the application with qemu or a hardware simulator. If you have this kind of a wrapper, these lines are all you need to write. Meson will automatically use the given wrapper when it needs to run host binaries. This happens e.g. when running the project's test suite.

Cross compiling without an exe wrapper
----

There are cross compilation setups where the host's binaries can not be run. In this case we need to write a slightly larger cross info file. Here is one for Linux ARM.

    name = 'linux'
    c = '/usr/bin/arm-linux-gnueabihf-gcc'
    cpp = '/usr/bin/arm-linux-gnueabihf-g++'
    ar = '/usr/arm-linux-gnueabihf/bin/ar'
    strip = '/usr/arm-linux-gnueabihf/bin/strip'

    sizeof_int = 4
    sizeof_wchar_t = 4
    sizeof_void* = 4

    alignment_char = 1
    alignment_void* = 4
    alignment_double = 4

    has_function_printf = true

As you can see, we need to information for those tests that can not be run. If some required information is missing, Meson will stop and write an error message describing how to fix the issue.

Starting a cross build
----

Once you have the cross file, starting a build is simple

    meson srcdir builddir --cross-file cross_file.txt

Once configuration is done, compilation is started by invoking Ninja in the usual way.

Introspection and system checks
----

The main *meson* object provides two functions to determine cross compilation status.

    meson.is_cross_build()  # returns true when cross compiling
    meson.has_exe_wrapper() # returns true if an exe wrapper has been defined

Note that the latter gives undefined return value when doing a native build.

You can run system checks on both the system compiler or the cross compiler. You just have to specify which one to use.

    build_compiler   = meson.get_compiler('c', native : true)
    host_compiler = meson.get_compiler('c', native : false)

    build_int_size = build_compiler.sizeof('int')
    host_int_size  = host_compiler.sizeof('int')

Mixing host and build targets
-----

Sometimes you need to build a tool which is used to generate source files. These are then compiled for the actual target. For this you would want to build some targets with the system's native compiler. This requires only one extra keyword argument.

    native_exe = executable('mygen', 'mygen.c', native : true)

You can then take <tt>native_exe</tt> and use it as part of a generator rule or anything else you might want.

---

[Back to index](Manual).
