Meson does not have native support for building OSX packages but it does provide all the tools you need to create one yourself. The reason for this is that it is a very hard task to write a system that provides for all the different ways to do that but it is very easy to write simple scripts for each application.

Sample code for this can be found in [the Meson manual test suite](https://github.com/jpakkane/meson/tree/master/manual%20tests/3%20osx%20bundle).

## Creating an app bundle

OSX app bundles are actually extremely simple. They are just a directory of files in a certain format. All the details you need to know are on [this page](https://stackoverflow.com/questions/1596945/building-osx-app-bundle) and it is highly recommended that you read it first.

Let's assume that we are creating our app bundle into <tt>/tmp/myapp.app</tt>. Suppose we have one executable, so we need to install that into <tt>Contents/MacOS</tt>. If we define the executable like this:

    executable('foo', 'foo1.c', ..., install : true)

then we just need to initialize our build tree with this command:

    meson --prefix=/tmp/myapp.app --bindir=Contents/MacOS builddir <other flags you might need>

Now when we do <tt>ninja install</tt> the system is properly staged. If you have any resource files or data, you need to install them into <tt>Contents/Resources</tt> either by custom install commands or specifying more install paths to the Meson command.

Next we need to install an <tt>Info.plist</tt> file and an icon. For those we need the following two Meson definitions.

    install_data('myapp.icns', install_dir : 'Contents/Resources')
    install_data('Info.plist', install_dir : 'Contents')

The simplest way to create an icon in the <tt>icns</tt> format is to create an icon in tiff format and then use the <tt>tiff2icns</tt> helper application that comes with XCode.

Some applications assume that the working directory of the app process is the same where the binary executable is. If this is the case for you, then you need to create a wrapper script that looks like this:

    #!/bin/bash

    cd "${0%/*}"
    ./myapp

install it with this:

    install_data('myapp.sh', install_dir : 'Contents/MacOS')

and make sure that you specify <tt>myapp.sh</tt> as the executable to run in your <tt>Info.plist</tt>.

If you are not using any external libraries, this is all you need to do. You now have a full app bundle in <tt>/tmp/myapp.app</tt> that you can use. Most applications use third party frameworks and libraries, though, so you need to add them to the bundle so it will work on other peoples' machines.

As an example we are going to use the [SDL2](https://libsdl.org/) framework. In order to bundle it in our app, we first specify an installer script to run.

    meson.set_install_script('install_script.sh')

The install script does two things. First it copies the whole framework into our bundle.

    mkdir -p ${MESON_INSTALL_PREFIX}/Contents/Frameworks
    cp -r /Library/Frameworks/SDL2.framework ${MESON_INSTALL_PREFIX}/Contents/Frameworks

Then it needs to alter the library search path of our executable(s). This tells OSX that the libraries your app needs are inside your bundle. In the case of SDL2, the invocation goes like this:

    install_name_tool -change @rpath/SDL2.framework/Versions/A/SDL2 \
      @executable_path/../FrameWorks/SDL2.framework/Versions/A/SDL2 \
      ${MESON_INSTALL_PREFIX}/Contents/MacOS/myapp

This is the part of OSX app bundling that you must always do yourself. OSX dependencies come in many shapes and forms and unfortunately there is no reliable automatic way to tell how each dependency library should be handled. Frameworks go to the <tt>Frameworks</tt> directory while plain <tt>.dylib</tt> files usually go to <tt>Contents/Resources/lib</tt> (but you can put them wherever you like). To get this done you have to check what your program links against with <tt>otool -L /path/to/binary</tt> and manually add the copy and fix steps to your install script. Do not copy system libraries inside your bundle, though.

After this you have a fully working, self-contained OSX app bundle ready for distribution.

## Creating a .dmg installer

A .dmg installer is similarly quite simple, at its core it is basically a slightly fancy compressed archive. A good description can be found on [this page](https://el-tramo.be/guides/fancy-dmg/). Please read it and create a template image file according to its instructions.

The actual process of creating the installer is very simple: you mount the template image, copy your app bundle in it, unmount it and convert the image into a compressed archive. The actual commands to do this are not particularly interesting, feel free to steal them from either the linked page above or from the sample script in Meson's test suite.

## Putting it all together

There are many ways to put the .dmg installer together and different people will do it in different ways. The linked sample code does it by having two different scripts. This separates the different pieces generating the installer into logical pieces.

<tt>install_script.sh</tt> only deals with embedding dependencies and fixing the library paths.

<tt>build_osx_installer.sh</tt> sets up the build with the proper paths, compiles, installs and generates the .dmg package.

The main reasoning here is that in order to build a complete OSX installer package from source, all you need to do is to cd into the source tree and run <tt>./build_osx_installer.sh</tt>.

---

[Back to index](Manual).