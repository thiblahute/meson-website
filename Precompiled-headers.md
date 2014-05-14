Parsing header files of system libraries is surprisingly expensive. A typical source file has less than one thousand lines of code. In contrast the headers of large libraries can be tens of thousands of lines. This is especially problematic with C++, where header-only libraries are common and they may contain extremely complex code. This makes them slow to compile.

Precompiled headers are a tool to mitigate this issue. Basically what they do is parse the headers and then serialize the compiler's internal state to disk. The downside of precompiled headers is that they are tricky to set up. Meson has native support for precompiled headers, but using them takes a little work.

A precompiled header file is relatively simple. It is a header file that contains <tt>#include</tt> directives for the system headers to precompile. Here is a C++ example.

    #include<vector>
    #include<string>
    #include<map>

In Meson, precompiled header files are always per-target. That is, the given precompiled header is used when compiling every single file in the target. Due to limitations of the underlying compilers, this header file must not be in the same subdirectory as any of the source files. It is strongly recommended that you create a subdirectory called <tt>pch</tt> in the target directory and put the header files (and nothing else) there.

Toggling the usage of precompiled headers
--

If you with to compile your project without precompiled headers, you can configure it by running Meson with the <tt>--disable-pch</tt> flag. You can also toggle the use of pch in a configured build directory with the gui tool. You don't have to do any changes to the source code. Typically this is done to test whether your project compiles cleanly without pch (that is, checking that its #includes are in order) and working around compiler bugs.

Using precompiled headers with GCC and derivatives
--

Once you have a file to precompile, you can enable the use of pch for a give target with a *pch* keyword argument. As an example, here's how you would use it with a C binary.

    executable('myexe', sources : sourcelist, c_pch : 'pch/myexe_pch.h')

You should note that your source files must _not_ include the file <tt>myexe_pch.h</tt> and you must _not_ add the pch subdirectory to your search path. Meson will make the compiler include the pch with compiler options. If you want to disable pch (because of, say, compiler bugs), it can be done entirely on the build system side with no changes to source code.

You can use precompiled headers on any build target. If your target has multiple languages, you can specify multiple pch files like this.

    executable('multilang', sources : srclist,
    c_pch : 'pch/c_pch.h', cpp_pch : 'pch/cpp_pch.h'])

Using precompiled headers with MSVC
--

MSVC is a bit trickier, because in addition to the header file, it also requires a correspongind source file. If your header is called <tt>foo_pch.h</tt>, the corresponding source file is usually called <tt>foo_pch.cpp</tt> and it resides in the same <tt>pch</tt> subdirectory as the header. Its contents are this:

    #if !defined(_MSC_VER)
    #error "This file is only for use with MSVC."
    #endif

    #include "foo_pch.h"

To enable pch, simply list both files in the target definition:

    executable('myexe', sources : srclist, cpp_pch : ['pch/foo_pch.h', 'pch/foo_pch.cpp'])

This form will work with both gcc and msvc, because Meson knows that gcc does not need a <tt>.cpp</tt> file and thus just ignores it.

It should be noted that due to implementation details of the MSVC compiler, having precompiled headers for multiple languages in the same target is not guaranteed to work.

---

[Back to index](Manual).