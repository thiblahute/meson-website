Meson does not have native support for building OSX packages but it does provide all the tools you need to create one yourself. The reason for this is that it is a very hard task to write a system that provides for all the different ways to do that but it is very easy to write simple scripts for each application.

## Creating an app bundle

OSX app bundles are actually extremely simple. They are just a directory of files in a certain format. All the details you need to know are on [this page](https://stackoverflow.com/questions/1596945/building-osx-app-bundle) and it is highly recommended that you read it first.

Let's assume that we are creating our app bundle into <tt>/tmp/myapp.app</tt>. Suppose we have one executable, so we need to install that into <tt>Contents/MacOS</tt>. If we define the executable like this:

    executable('foo', 'foo1.c', ..., install : true)

then we just need to initialize our build tree with this command:

    meson --prefix=/tmp/myapp.app --bindir=Contents/MacOS builddir

Now when we do <tt>ninja install</tt> the system is properly staged. If you have any resource files or data, you need to install them into <tt>Contents/Resources</tt>.

Next we need to install an <tt>Info.plist</tt> file and an icon. For those we need the following two Meson definitions.

    install_data('myapp.icns', install_dir : 'Contents/Resources')
    install_data('Info.plist', install_dir : 'Contents')

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

This is the part of OSX app bundling that you must always do yourself. OSX dependencies come in many shapes and forms and unfortunately there is no reliable automatic way to tell how each dependency library should be handled. You have to do <tt>otool -L /path/to/binary</tt> and manually add the copy and fix steps to your install script. You only have to do that once per dependency, though.

After this you have a fully working, self-contained OSX app bundle ready for distribution.

---

[Back to index](Manual).