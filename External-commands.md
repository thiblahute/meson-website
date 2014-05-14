As a part of the software configuration, you may want to get extra data by running external commands. The basic syntax is the following.

    r = run_command('command', 'arg1', 'arg2', 'arg3')
    if r.returncode() != 0
      # it failed
    endif
    output = r.stdout().strip()
    errortxt = r.stderr().strip()

The <tt>run_command</tt> function returns an object that can be queried for return value and text written to stdout and stderr. The <tt>strip</tt> method call is used to strip trailing and leading whitespace from strings. Usually output from command line programs ends in a newline, which is unwanted in string variables. The first argument can be either a string or an executable you have detected earlier with <tt>find_program</tt>.

Note that you can not pass your command line as a single string. That is, calling <tt>run_command('do_something foo bar')</tt> will not work. You must either split up the string into separate arguments or pass the split command as an array. It should also be noted that Meson will not pass the command to the shell, so any command lines that try to use things such as environment variables, backticks or pipelines will not work. If you require shell semantics, write your command into a script file and call that with <tt>run_command</tt>.

---

[Back to index](Manual).