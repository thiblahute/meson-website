**0.37.0 is not released yet, these are preliminary**

# New features

## Mesontest

Mesontest is a new testing tool that allows you to run your tests in many different ways. As an example you can run tests multiple times:

    mesontest --repeat=1000 a_test

or with an arbitrary wrapper executable:

    mesontest --wrap='valgrind --tool=helgrind' a_test

or under gdb, 1000 times in a row. This is handy for tests that fail spuriously, as when the crash happens you are given the full GDB command line:

    mesontest --repeat=1000 --gdb a_test

## Mesonrewrite

Add description here.

## Gnome module

- Detect required programs and print useful errors if missing

### gtkdoc

- Allow passing a list of directories to `src_dir` kwarg
- Add `namespace` kwarg
- Add `mode` kwarg
- Fix `gtkdoc-scangobj` finding local libraries

### compile_resources

- Add `gresource_bundle` kwarg to output `.gresource` files
- Add `export` and `install_header` kwargs
- Use depfile support available in GLib >= 2.52.0

## i18n module

- Add `merge_file()` function for creating translated files
- Add `preset` kwarg to included common gettext flags
- Read languages from `LINGUAS` file

## Other stuff

Add your highlights here.
