Wraptool is a helper tool that allows you to manage your source dependencies using the Wrapdb database. It gives you all things you would expect, such as installing and updating dependencies. The wrap tool works on all platforms, the only limitation is that the wrap definition works on your target platform. If you find some Wraps that don't work, please file bugs or, even better, patches.

All code examples here assume that you are running the commands in your top level source directory.

## Simple querying

The simplest operation to do is to query the list of packages available. To list them all issue the following command:

    wraptool list

The output looks something like this:

    box2d
    enet
    gtest
    libjpeg
    liblzma
    libpng
    libxml2
    lua
    ogg
    sqlite
    vorbis
    zlib

Usually you want to search for a specific package. This can be done with the `search` command:

    # wraptool search jpeg
    libjpeg

To determine which versions of libjpeg are available to install, issue the `info` command:

    # wraptool info libjpeg
    Available versions of libjpeg:
      9a 2

The first number is the upstream release version, in this case `9a`. The second number is the Wrap revision number. They don't relate to anything in particular, but larger numbers imply newer releases. You should always use the newest available release.