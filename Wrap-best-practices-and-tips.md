There are several things you need to take into consideration when writing a Meson build definition for a project. This is especially true when the project will be used as a subproject. This page lists a few things to consider when writing your definitions.

## Do not put config.h in external search path

Many projects use a `config.h` header file that they use for configuring their project internally. These files are never installed to the system header files so there are no inclusion collisions. This is not the case with subprojects, your project tree may have an arbitrary number of configuration files, so we need to ensure they don't clash.

The basic problem is that the users of the subproject must be able to include subproject headers without seeing its `config.h` file. The most correct solution is to rename the `config.h` file into something unique, such as `foobar-config.h`. This is usually not feasible unless you are the maintainer of the subproject in question.

The pragmatic solution is to put the config header in a directory that has no other header files and then hide that from everyone else. One way is to create a top level subdirectory called `internal` and use that to build your own sources, like this:

    subdir('internal') # create config.h in this subdir
    internal_inc = include_directories('internal') #
    shared_library('foo', 'foo.c', include_directories : internal_inc)
