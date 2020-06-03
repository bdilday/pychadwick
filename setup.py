# tips on building a shared library using cmake within setup.py
# https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py

from distutils.core import setup

import pathlib
import os

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig


class CMakeExtension(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):
    def run(self):
        for ext in self.extensions:
            print("build ext", ext)
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()
        print("cwd is", cwd)

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        print("make build_temp", build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = "Debug" if self.debug else "Release"
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(extdir.parent.absolute()),
            "-DCMAKE_BUILD_TYPE=" + config,
        ]

        # example of build args
        build_args = ["--config", config, "--", "-j4"]

        os.chdir(str(build_temp))
        print("cmake", str(cwd), cmake_args)
        self.spawn(["cmake", str(cwd)] + cmake_args)
        os.chdir(str(cwd))
        if not self.dry_run:
              self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))


setup(
    name="pychadwick",
    version="0.1.0",
    description="pychadwick",
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    url="https://github.com/bdilday/pychadwick",
    packages=["pychadwick"],
    ext_modules=[CMakeExtension("src/cwtools/libcwevent")],
    cmdclass={"build_ext": build_ext},
)

