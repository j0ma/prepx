#! /usr/bin/env python

from os import path

from setuptools import find_packages, setup

# from prepx import __version__


def setup_package() -> None:
    root = path.abspath(path.dirname(__file__))
    with open(path.join(root, "README.md"), encoding="utf-8") as f:
        long_description = "FOO" #f.read()

    setup(
        name="prepx",
        version="0.0.1", #__version__,
        packages=find_packages(include=("prepx", "prepx.*")),
        # Package type information
        package_data={"prepx": ["py.typed"]},
        python_requires=">=3.8",
        license="MIT",
        description="prepx: it creates experiment folders",
        long_description=long_description,
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
        long_description_content_type="text/markdown",
        author="Jonne Sälevä",
        author_email="jsaleva@isi.edu",
        install_requires=[
            "click",
            "attrs",
            "rich"
        ], 
        entry_points={
            "console_scripts": ["prepx = prepx.cli:cli"]
        }

    )


if __name__ == "__main__":
    setup_package()
