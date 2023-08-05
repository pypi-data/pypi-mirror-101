#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

with open("README", "r") as fh:
    long_description = fh.read()

setup(name='exgrex-pytest',
      version='0.1a2',
      description='Package exgrex-pytest adds to package exgrex-py the ability to use '
                  'the pytest framework.',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      author='vshagur',
      author_email='vshagur@gmail.com',
      packages=find_packages(
          exclude=['test', '*.test.*', '*.test', 'bats', '*.bats.*', '*.bats', ]
      ),
      entry_points={"pytest11": ["exgrex = exgrexPytest.plugin"]},
      package_data={'docs': [], 'example': []},
      install_requires=['exgrex-py', ],
      scripts=[],
      keywords=['mooc', 'grader', 'python', 'python3', 'education', 'exgrex',
                'coursera', 'pytest'],
      url='https://github.com/vshagur/exgrex-pytest',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux", ],
      python_requires='>=3.6',
      )
