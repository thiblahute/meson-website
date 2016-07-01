# How do I do X in Meson?

This page lists code snippets for common tasks. These are written mostly using the C compiler, but the same approach should work on almost all other compilers.

# Set compiler

When first running Meson, set it in an environment variable.

    CC=mycc meson <options>

# Set extra compiler and linker flags 

The behaviour is the same as with other build systems, with environment variables during first invocation.

    CFLAGS=-fsomething LDFLAGS=-Wl,--linker-flag meson <options>

