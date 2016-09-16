Meson is implemented in Python. This has both positive and negative sides. The main thing people seem to be mindful about is the dependency on Python to build source code. This page discusses various aspects of this problem.

# Dependency hell

There have been many Python programs that are difficult to maintain on multiple platforms. The reasons come mostly from dependencies. The program may use dependencies that are hard to compile on certain platforms, are outdated, conflict with other dependencies, not available on a given Python version and so on.

Meson avoids dependency problems with one simple rule: Meson is not allowed to have any dependencies outside the Python basic library. The only thing you need is Python 3 (and possibly Ninja).

## Reimplementability

Meson has been designed in such a way that the implementation language is never exposed in the build definitions. This makes it possible (and maybe even easy) to reimplement Meson in any other programming language. There are currently no plans to reimplement Meson, but we will make sure that Python is not exposed inside the build definitions.