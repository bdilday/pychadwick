from setuptools import find_packages

from skbuild import setup

import pathlib
import os


setup(
    name="pychadwick",
    version="0.1.0",
    description="pychadwick",
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    packages=find_packages(),
    url="https://github.com/bdilday/pychadwick",
    cmake_install_dir="pychadwick/build",
)
