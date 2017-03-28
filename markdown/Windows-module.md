# Windows module

This module provides functionality used to build applications for Windows.

## Methods

### compile_resources

Compiles Windows `rc` files specified in the positional arguments. Returns an opaque object that you put in the list of sources for the target you want to have the resources in. This method has one keyword argument `args` which lists extra arguments to pass to the resource compiler.
