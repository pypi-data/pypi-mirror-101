#!/usr/bin/env python

from setuptools import setup, Command, Extension, find_packages
from setuptools.command.build_ext import build_ext

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kpclibpy",
    version="1.0.9",
    description="KeePass command application",
    url="https://github.com/passxyz/KPCLibPy",
    license="MIT",
    author="Roger Ye",
    author_email="shugaoye@yahoo.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["pycparser==2.20",
        "pythonnet==2.5.2",
        "python-nubia==0.2b5"],
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: C#",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
)
