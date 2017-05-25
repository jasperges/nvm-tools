from distutils.core import setup

import os
import imp

version_file = os.path.abspath("nvm_loader/version.py")
version_mod = imp.load_source("version", version_file)
version = version_mod.version

setup(
    name='nvm-loader',
    version=version,
    packages=['nvm_loader'],
    license="LGPL",
    long_description=open('README.md').read(),
)
