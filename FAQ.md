# Meson Frequently Asked Questions #

## Why can't I specify target files with a wildcard? ##

Instead of specifying files explicitly, people seem to want to do this:

    executable('myprog', sources : '*.cpp') # This does NOT work!

Meson does not support this syntax and the reason for this is simple. This can not be made both reliable and fast. By reliable we mean that if the user adds a new source file to the subdirectory, Meson should detect that and make it part of the build automatically.

One of the main requirements of Meson is that it must be fast. This means that a no-op build in a  tree of 10 000 source files must take no more than one second. This is only possible because Meson knows the exact list of files to check. If any target is specified as a wildcard glob, this is no longer possible. Meson would need to re-evaluate the glob every time and compare the list of files produced against the previous list. This means inspecting the entire source tree (because the glob pattern could be <tt>src/\*/\*/\*/\*.cpp</tt> or something like that). This is impossible to do efficiently.

Because of this, all source files must be specified explicitly.

## But I really want to use wildcards! ##

If the tradeoff between reliability and convenience is acceptable to you, then Meson gives you all the tools necessary to do wildcard globbing. You are allowed to run arbitrary commands during configuration. First you need to write a script that locates the files to compile. Here's a simple shell script that writes all <tt>.c</tt> files in the current directory, one per line.


    #!/bin/sh

    for i in *.c; do
      echo $i
    done

Then you need to run this script in your Meson file, convert the output into a string array and use the result in a target.

    c = run_command('grabber.sh')
    sources = c.stdout().strip().split(newline)
    e = executable('prog', sources)

The script can be any executable, so it can be written in shell, Python, Lua, Perl or whatever you wish.

As mentioned above, the tradeoff is that just adding new files to the source directory does *not* add them to the build automatically. To add them you need to tell Meson to reinitialize itself. The simplest way is to touch the <tt>meson.build</tt> file in your source root. Then Meson will reconfigure itself next time the build command is run. Advanced users can even write a small background script that utilizes a filesystem event queue, such as [inotify](https://en.wikipedia.org/wiki/Inotify), to do this automatically.

## Should I use <tt>subdir</tt> or <tt>subproject</tt>? ##

The answer is almost always <tt>subdir</tt>. Subproject exists for a very specific use case: embedding external dependencies into your build process. As an example, suppose we are writing a game and wish to use SDL. Let us further suppose that SDL comes with a Meson build definition. Let us suppose even further that we don't want to use prebuilt binaries but want to compile SDL for ourselves.

In this case you would use <tt>subproject</tt>. The way to do it would be to grab the source code of SDL and put it inside your own source tree. Then you would do <tt>sdl = subproject('sdl')</tt>, which would cause Meson to build SDL as part of your build and would then allow you to link against it or do whatever else you may prefer.

For every other use you would use <tt>subdir</tt>. As an example, if you wanted to build a shared library in one dir and link tests against it in another dir, you would do something like this:

    project('simple', 'c')
    subdir('src')   # library is built here
    subdir('tests') # test binaries would link against the library here

## Why is there not a Make backend? ##

Because Make is slow. It should be noted that this is not an implementation issue, Make simply can not be made fast. For further info we recommend you read [this post](http://neugierig.org/software/chromium/notes/2011/02/ninja.html) by Evan Martin, the author of Ninja. Makefiles also have a syntax that is very unpleasant to write.

The only reason why one would use Make instead of Ninja is working on a platform that does not have a Ninja port. Even in this case it is an order of magnitude less work to port Ninja than it is to write a Make backend for Meson.

Just use Ninja, you'll be happier that way. I guarantee it.