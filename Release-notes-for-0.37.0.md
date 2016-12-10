**0.37.0 is not released yet, these are preliminary**

# New features

## Mesontest

Add description here.

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
- Use depfile support available in GLib >= 2.42.0

## i18n module

- Add `merge_file()` function for creating translated files
- Add `preset` kwarg to included common gettext flags
- Read languages from `LINGUAS` file

## Other stuff

Add your highlights here.
