Meson has a very simple notational shorthand for enabling thread support on your build targets. First you obtain the thread dependency object like this:

    thread_dep = dependency('threads')

And then you just use it in a target like this:

    executable('threadedprogram', ...
      dependencies : thread_dep)

---

[Back to index](Manual).