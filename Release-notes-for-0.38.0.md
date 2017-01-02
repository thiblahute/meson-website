**This is preliminary. 0.38.0 has not been released yet.**

# Uninstall target

Meson allows you to uninstall an install step by invoking the uninstall target. This will remove all files installed as part of install. Note that this does not restore the original files. This also does not undo changes done by custom install scripts (because they can do arbitrary install operations).

# Support for arbitrary test setups

Sometimes you need to run unit tests with special settings. For example under Valgrind. Usually this requires extra command line options for the tool. This is supported with the new *test setup* feature. For example to set up a test run with Valgrind, you'd write this in a `meson.build` file:

    add_test_setup('valgrind',
      exe_wrapper : [vg, '--error-exitcode=1', '--leak-check=full'],
      timeout_multiplier : 100)

This tells Meson to run tests with Valgrind using the given options and multiplying the test timeout values by 100. To run this test setup simply issue the following command:

    mesontest --setup=valgrind

# Other Features

Add them here.