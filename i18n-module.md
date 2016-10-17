This module provides internationalisation and localisation functionality. It has the following methods.

### gettext

Sets up gettext localisation so that translations are built and placed into their proper locations during install. Takes one positional argument which is the name of the gettext module.

* `languages`: list of languages that are to be generated
* `data_dirs`: (*Added 0.36.0*) list of directories to be set for `GETTEXTDATADIRS` env var, used for local its files
* `args`: list of extra arguments to pass to `xgettext` when generating the pot file

This function also defines targets for maintainers to use:  
**Note**: These output to the source directory

* `<project_id>-pot`: runs `xgettext` to regenerate the pot file.

