#! /usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.0"

def readme():
    """ print long description """
    with open('README.md') as f:
        long_descrip = f.read()
    return long_descrip

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CI_COMMIT_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="videojoiner",
    version=VERSION,
    description="make video joining easy on windows",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rveach/videojoiner",
    author="Ryan Veach",
    author_email="rveach@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Video :: Conversion",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
    ],
    keywords=['Raspberry', 'Pi', 'Raspbian'],
    packages=[],
    scripts=['videojoiner.py'],
    install_requires=[],
    python_requires='>=3.6',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
