Unity builds are a technique for cutting down build times. The way it works is relatively straightforward. Suppose we have source files <tt>src1.c</tt>, <tt>src2.c</tt> and <tt>src3.c</tt>. Normally we would run the compiler three times, once for each file. In a unity build we instead compile all these sources in a single unit. The simplest approach is to create a new source file that looks like this.

    #include<src1.c>
    #include<src2.c>
    #include<src3.c>

This is then compiled rather than the individual files. The exact speedup depends on the code base, of course, but it is not uncommon to obtain more than 50% speedup in compile times. This happens even though the Unity build uses only one CPU whereas individual compiles can be run in parallel. Unity builds can also lead to faster code, because the compiler can do more aggressive optimizations (e.g. inlining).

The downside is that incremental builds are as slow as full rebuilds (because that is what they are). Unity compiles also use more memory, which may become an issue in certain scenarios. There may also be some bugs in the source that need to be fixed before Unity compiles work. As an example, if both <tt>src1.c</tt> and <tt>src2.c</tt> contain a static function or variable of the same name, there will be a clash.

Meson has built-in support for unity builds. To enable them, just pass the <tt>--unity</tt> command line argument or enable unity builds with the GUI. No code changes are necessary apart from the potential clash issue discussed above. Meson will automatically generate all the necessary inclusion files for you. 

---

[Back to index](Manual).