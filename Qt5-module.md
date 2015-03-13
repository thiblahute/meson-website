The Qt5 module provides tools to automatically deal with the various tools and steps required for Qt. The module has one method.

## preprocess

This method takes four keyword arguments, <tt>moc_headers</tt>, <tt>moc_sources</tt>, <tt>ui_files</tt> and <tt>qresources</tt> which define the files that require preprocessing with <tt>moc</tt>, <tt>uic</tt> and <tt>rcc</tt>. It returns an opaque object that should be passed to a main build target. A simple example would look like this:

    moc_files = qt5.preprocess(moc_headers : 'myclass.h')
    executable('myprog', 'main.cpp', 'myclass.cpp', moc_files)

---

Back to [module reference](Module reference).