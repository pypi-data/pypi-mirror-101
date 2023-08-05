#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

with open("README", "r") as fh:
    long_description = fh.read()

setup(name='exgrex-py',
      version='0.3a2',
      description='Exgrex implementation for the Python programming language.',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      author='vshagur',
      author_email='vshagur@gmail.com',
      packages=find_packages(
          exclude=['test', '*.test.*', '*.test', 'bats', '*.bats.*', '*.bats', ]
      ),
      package_data={
          'docs': ['docs/*.md'],
          'example': ['example/execute_py', 'example/grader.config']
      },
      scripts=["bin/exgrexCourseraPy", ],
      keywords=['mooc', 'grader', 'python', 'python3', 'education', 'exgrex', 'coursera'],
      url='https://github.com/vshagur/exgrex-py',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",],
      python_requires='>=3.6',
      )
