In addition to core language features, Meson also provides a module system aimed at providing helper methods for common build operations. Using modules is simple, first you import them:

```meson
mymod = import('somemodule')
```

After this you can use the returned object to use the functionality provided:

```meson
mymod.do_something('text argument')
```

The list of modules and their functionality is available on [this page](Module-reference).

---

[Back to index](Manual).
