Most non-trivial builds require user-settable options. As an example a program may have two different data backends that are selectable at build time. Meson provides for this by having a option definition file. Its name is <tt>meson_options.txt</tt> and it is placed at the root of your source tree.

Here is a simple option file.

    option('someoption', type : 'string', value : 'optval', description : 'An option')
    option('other_one', type : 'boolean', value : false)
    option('combo_opt', type : 'combo', choices : ['one', 'two', 'three'], value : 'three')

This demonstrates the three basic option types and their usage. String option is just a free form string and a boolean option is, unsurprisingly, true or false. The combo option can have any value from the strings listed in argument <tt>choices</tt>. If <tt>value</tt> is not set, it defaults to empty string for strings, <tt>true</tt> for booleans or the first element in a combo. You can specify <tt>description</tt>, which is a free form piece of text describing the option. It defaults to option name.

These options are accessed in Meson code with the <tt>get_option</tt> function.

    optval = get_option('opt_name')

It should be noted that you can not set option values in your Meson scripts. They have to be set externally. The easiest way to change them is to use the Meson GUI or command line tools.

---

[Back to index](Manual).