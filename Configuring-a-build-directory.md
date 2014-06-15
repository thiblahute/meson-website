Often you want to change the settings of your build after it has been generated. For example you might want to change from a debug build into a release build, set custom compiler flags, change the build options provided in your <tt>meson_options.txt</tt> file and so on.

The main tool for this is the <tt>mesonconf</tt> script. You may also use the <tt>mesongui</tt> graphical application if you want. However this document describes the use of the command line client.

You invoke <tt>mesonconf</tt> by giving it the location of your build dir. If omitted, the current working directory is used instead. Here's a sample output for a simple project.

    Core properties
    
    Source dir /home/jpakkane/clangdemo/2_address
    Build dir  /home/jpakkane/clangdemo/2_address/buildmeson
    
    Core options
    
    type     Build type          debug
    strip    Strip on install    False
    coverage Coverage report     False
    pch      Precompiled headers True
    unity    Unity build         False
    
    Compiler flags
    
    cflags []

    Linker flags
    
    clinkflags []
    
    Directories
    
    installprefix Install prefix        /usr/local
    libdir        Library directory     lib
    bindir        Binary directory      bin
    includedir    Header directory      include
    datadir       Data directory        share
    mandir        Man page directory    share/man
    localedir     Locale file directory share/locale
    
    This project does not have any options

These are all the options available for the current project arranged into related groups. The first column in every field is the name of the option. To set an option you use the <tt>-D</tt> option. For example, changing the installation prefix from <tt>/usr/local</tt> to <tt>/tmp/testroot</tt> you would issue the following command.

    mesonconf -Dinstallprefix=/tmp/testroot

Then you would run your build command (usually <tt>ninja</tt>), which would cause Meson to detect that the build setup has changed and do all the work required to bring your build tree up to date.

---

[Back to index](Manual)
