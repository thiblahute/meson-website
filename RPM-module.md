The RPM module can be used to create a sample rpm spec file for a Meson project. It autodetects installed files, dependencies and so on. Using it is very simple. At the very end of your Meson project add these two lines.

    rpm = import('rpm')
    rpm.generate_spec_template()

You can find the template in your build directory. Then remove the two lines above and manually edit the generated template to add missing information. After this it is ready for use.

---

Back to [module reference](Module reference).
