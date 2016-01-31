Syntax and structure of Meson files
==

The syntax of Meson's specification language has been kept as simple as possible. It is *strongly typed* so no object is ever converted to another under the covers. Variables have no visible type which makes Meson *dynamically typed* (also known as *duck typed*).

The main building blocks of the language are *variables*, *numbers*, *booleans*, *strings*, *arrays*, *function calls*, *method calls*, *if statements* and *includes*.

Usually one Meson statement takes just one line. There is no way to have multiple statements on one line as in e.g. *C*. Function and method calls' argument lists can be split over multiple lines. Meson will autodetect this case and do the right thing. Apart from line ending whitespace has no syntactical meaning.


Variables
--

Variables in Meson work just like in other high level programming languages. A variable can contain a value of any type, such as an integer or a string. Variables don't need to be predeclared, you can just assign to them and they appear. Here's how you would assign values to two different variables.

    var1 = 'hello'
    var2 = 102

Numbers
--

Meson supports only integer numbers. They are declared simply by writing them out.

Strings can be converted to a number like this:

    string_var = '42'
    num = var1.to_int()

Booleans
--

A boolean is either <tt>true</tt> or <tt>false</tt>.

    truth = true

Strings
--

Strings in Meson are declared with single quotes. To enter a literal single quote do it like this:

    single quote = 'contains a \' character'

Similarly <tt>\n</tt> gets converted to a newline and <tt>\\\\</tt> to a single backslash.

Strings running over multiple lines
--

Strings running over multiple lines can be declared with three single quotes, like this:

    multiline_string = '''#include <foo.h>
                          int main (int argc, char ** argv) {
                            return FOO_SUCCESS;
                          }'''

This can also be combined with the string formatting functionality described below.

String formatting
--

Strings can be built using the string formatting functionality.

    template = 'string: @0@, number: @1@, bool: @2@'
    res = template.format('text', 1, true)
    # res now has value 'string: text, number: 1, bool: true'

As can be seen, the formatting works by replacing placeholders of type <tt>@number@</tt> with the corresponding argument.

Arrays
--

Arrays are delimited by brackets. An array can contain an arbitrary number of objects of any type.

    my_array = [1, 2, 'string', some_obj]

You can add additional items to an array like this:

    my_array += [ 'foo', 3, 4, another_obj ]

Function calls
--

Meson provides a set of usable functions. The most common use case is creating build objects.

    executable('progname', 'prog.c')

Method calls
--

Objects can have methods, which are called with the dot operator. The exact methods it provides depends on the object.

    myobj = some_function()
    myobj.do_something('now')

If statements
--

If statements work just like in other languages.

    var1 = 1
    var2 = 2
    if var1 == var2 # Evaluates to false
      something_broke()
    elif var3 == var2
      something_else_broke()
    else
      everything_ok()
    endif

    opt = get_option('someoption')
    if opt == 'foo'
      do_something()
    endif

## Foreach statements

To do an operation on all elements of an array, use the <tt>foreach</tt> command. As an example, here's how you would define two executables with corresponding tests.

    progs = [['prog1', ['prog1.c', 'foo.c']],
             ['prog2', ['prog2.c', 'bar.c']]]

    foreach p : progs
      exe = executable(p.get(0), p.get(1))
      test(p.get(0), exe)
    endforeach

Note that Meson variables are immutable. Trying to assign a new value to <tt>progs</tt> inside a foreach loop will not affect foreach's control flow.

Logical operations
--

Meson has the standard range of logical operations.

    if a and b
      # do something
    endif
    if c or d
      # do something
    endif
    if not e
      # do something
    endif
    if not (f or g)
      # do something
    endif

Logical operations work only on boolean values. 

Comments
--

A comment starts with the <tt>#</tt> character and extends until the end of the line.

    some_function() # This is a comment
    some_other_function()

Includes
--

Most source trees have multiple subdirectories to process. These can be handled by Meson's <tt>subdir</tt> command. It changes to the given subdirectory and executes the contents of <tt>meson.build</tt> in that subdirectory. All state (variables etc) are passed to and from the subdirectory. The effect is roughly the same as if the contents of the subdirectory's Meson file would have been written where the include command is.

    test_data_dir = 'data'
    subdir('tests')

---

[Back to index](Manual).
