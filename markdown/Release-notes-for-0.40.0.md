---
title: Release 0.40
short-description: Release notes for 0.40 (unreleased)
...

**Preliminary, 0.40.0 has not been released yet**

# New features

## Outputs of generators can be used in custom targets in the VS backend

This has been possible with the Ninja backend for a long time but now the Visual Studio backend works too.

## `compute_int` method in the compiler objects

This method can be used to evaluate the value of an expression. As an example:

    cc = meson.get_compiler('c')
    two = cc.compute_int('1 + 1') # A very slow way of adding two numbers.

## Visual Studio 2017 support

There is now a VS2017 backend (`--backend=vs2017`) as well as a generic VS backend (`--backend=vs`) that autodetects the currently active VS version.

## No download mode for wraps

Added a new option `wrap-mode` that can be toggled to prevent Meson from downloading dependency projects. Attempting to do so will cause an error. This is useful for distro packagers and other cases where you must explicitly enforce that nothing is downloaded from the net during configuration or build.

## More

Add here as they are merged to master.
