#!/usr/bin/env python3
""" Setup script for this package"""

from distutils.core import setup
import os

## The text of the README file
README_TEXT = ""
if os.path.exists("README.md"):
    with open("README.md") as fh:
        README_TEXT = fh.read()

setup(
    name = 'multi-git',
    version = '0.1.12',
    description = 'Manage multiple git repositories with one command',
    author = 'Daniel Kullmann',
    author_email = 'python@danielkullmann.de',
    url = 'https://pypi.org/project/multi-git/',
    packages = [],
    scripts = ['multi-git'],
    install_requires = ['toml', 'config_path'],
    license = "MIT",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
)
