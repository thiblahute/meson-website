Meson comes with a fully functional unit test system. To use it simply build an executable and then use it in a test.

    e = executable('prog', 'testprog.c')
    test('name of test', e)

You can add as many tests as you want. They are run with the command <tt>ninja test</tt>.

Meson captures the output of all tests and writes it in the log file <tt>meson-logs/testlog.txt</tt>.

Test parameters
--

Some tests require the use of command line arguments or environment variables. These are simple to define.

    test('command line test', exe, args : ['first', 'second'])
    test('envvar test', exe2, env : ['key1=value1', 'key2=value2'])

Note how you need to specify multiple values as an array.

Coverage
--

If you enable coverage measurements by giving Meson the command line flags <tt>--enable-gcov</tt>, you can generate coverage reports. Meson will autodetect what coverage generator tools you have installed and will generate the corresponding targets. These targets are <tt>coverage-xml</tt> and <tt>coverage-text</tt> which are both provided by [Gcovr](https://software.sandia.gov/trac/fast/wiki/gcovr) and <tt>coverage-html</tt>, which requires [Lcov](http://ltp.sourceforge.net/coverage/lcov.php) and [GenHTML](http://linux.die.net/man/1/genhtml).

The the output of these commands is written to the log directory <tt>meson-logs</tt> in your build directory.

Valgrind
--

If you have [Valgrind](http://valgrind.org/) installed, Meson will provide a <tt>test-valgrind</tt> target, which runs all your unit tests under Valgrind. The full Valgrind log can be found in <tt>meson-logs/testlog-valgrind.txt</tt>

You can pass custom arguments to Valgrind by specifying them in a keyword argument like this:

    test('foo', executable, valgrind_args : ['-tool=helgrind', '-v'])

Parallelism
--

To reduce test times, Meson will by default run multiple unit tests in parallel. It is common to have some tests which can not be run in parallel because they require unique hold on some resource such as a file or a dbus name. You have to specify these tests with a keyword argument.

    test('unique test', t, is_parallel : false)

Meson will then make sure that no other unit test is running at the same time. Non-parallel tests take longer to run so it is recommended that you write your unit tests to be parallel executable whenever possible.

By default Meson uses as many concurrent processes as there are cores on the test machine. You can override this with the environment variable <tt>MESON_TESTTHREADS</tt> like this.

    MESON_TESTTHREADS=5 ninja test

---

[Back to index](Manual).
