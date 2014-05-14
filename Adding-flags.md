Often you need to specify extra compiler flags. Meson provides two different ways to achieve this: global flags and per-target flags.

Global flags
--

Global compiler flags are set with the following command.

    add_global_arguments('-std=c99', language : 'c')

This sets the flag that controls the C language standard used.

Global arguments have certain limitations. They all have to be defined before any build targets are specified. This ensures that the global flags are the same for every single source file built in the entire project with one exception. Compilation tests that are run as part of your project configuration do not use these flags. The reason for that is that you may need to run a test compile with and without a given flag to determine your build setup. For this reason tests do not use these global flags.

You should set only the most essential flags with this setting, you should *not* set debug or optimization flags. Instead they should be specified with the build type feature.

Per target flags
--

Per target flags are just as simple to define.

    executable('prog', 'prog.cc', cpp_args : '-DCPPTHING')

Here we create a C++ executable with an extra preprocessor definition. 

---

[Back to index](Manual).