# -*- coding: utf-8 -*-

from setuptools import setup
import os


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [
        (dirpath.replace(package + os.sep, "", 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename) for filename in filenames])
    return {package: filepaths}


setup(
    name="notifier",
    version="1.0",
    description="Notifier",
    url="http://github.com/grigorilab/notifier",
    author="Grigori Kartashyan",
    author_email="grigori.kartashyan@gmail.com",
    license="MIT",
    packages=get_packages("notifier"),
    package_data=get_package_data("notifier"),
    install_requires=[],
    scripts=[],
    zip_safe=False,
)
