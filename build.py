#!/usr/bin/env python3

import shutil
import os
import subprocess

if __name__ == "__main__":
    cwd = os.path.dirname(os.path.realpath(__file__))

    subprocess.check_call(['hotdoc', 'run'], cwd=cwd)
    docdir = os.path.join(cwd, "docs")
    os.chdir(docdir)
    built_doc = os.path.join(docdir, "html")

    try:
        in_html_files = os.listdir(docdir)
    except FileNotFoundError:
        pass

    for f in in_html_files:
        if f == 'html':
            continue

        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)

    for f in os.listdir(built_doc):
        relocated_file = os.path.join(docdir, f)
        built_file = os.path.join(built_doc, f)

        print("Copying %s -> %s" % (built_file, relocated_file))
        if os.path.isdir(built_file):
            shutil.copytree(built_file, relocated_file, symlinks=True)
        else:
            shutil.copy(built_file, relocated_file)
    shutil.rmtree(os.path.join(docdir, "html"))
