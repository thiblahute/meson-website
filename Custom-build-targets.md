While Meson tries to support as many languages and tools as possible, there is no possible way for it to cover all corner cases. For these cases it permits you to define custom build targets. Here is how one would use it.

     comp = find_program('custom_compiler')
     
     infile = 'source_code.txt'
     outfile = 'output.bin'
     
     mytarget = custom_target('targetname',
       output : 'output.bin',
       input : 'source_code.txt'
       command : [comp, '@INPUT@', '@OUTPUT@'],
       install : true,
       install_dir : 'subdir'
     )

This would generate the binary <tt>output.bin</tt> and install it to <tt>${prefix}/subdir/output.bin</tt>. Variable substitution works just like it does for source generation. 

## Details on compiler invocations ##

Meson only permits you to specify one command to run. This is by design as writing shell pipelines into build definition files leads to code that is very hard to maintain. If your compilation requires multiple steps you need to write a wrapper script that does all the necessary work. When doing this you need to be mindful of the following issues:

* do not assume that the command is invoked in any specific directory
* a target called <tt>target</tt> file <tt>outfile</tt> defined in subdir <tt>subdir</tt> must be written to <tt>build_dir/subdir/foo.dat</tt>
* if you need a subdirectory for temporary files, use <tt>build_dir/subdir/target.dir</tt>

---

[Back to index](Manual)
