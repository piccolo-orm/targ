#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

from targ import __VERSION__ as VERSION


directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(directory, "README.md")) as f:
    LONG_DESCRIPTION = f.read()


with open(os.path.join(directory, "requirements.txt")) as f:
    contents = f.read()
    REQUIREMENTS = [i.strip() for i in contents.strip().split("\n")]


setup(
    name="targ",
    version=VERSION,
    description=(
        "Build a Python CLI for your app, just using type hints and "
        "docstrings."
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Daniel Townsend",
    author_email="dan@dantownsend.co.uk",
    python_requires=">=3.7.0",
    url="https://github.com/piccolo-orm/targ/",
    packages=["targ"],
    data_files=[("", ["py.typed"])],
    install_requires=REQUIREMENTS,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
