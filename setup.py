import subprocess
import sys

try:
    from skbuild import setup
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-build"])
    from skbuild import setup

from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="pychadwick",
    version="0.4.0",
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    description="Python bindings to the Chadwick library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdilday/pychadwick",
    packages=find_packages(),
    cmake_install_dir="pychadwick/lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    install_requires=["scikit-build", "ninja", "cmake", "wheel", "setuptools", "pandas>=1.0.4", "requests"],
    entry_points={"console_scripts": ["pycwevent=pychadwick.cli.pycwevent:main"]},
)
