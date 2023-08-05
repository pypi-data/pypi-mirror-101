#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
setup(
  author="Maximilian Lange",
  author_email='maxhlange@gmail.com',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
  download_url="https://github.com/sasmlange/tablebase/blob/d9ab86d4cab0508e97cdf0157e41addbc43f8783/dist/tablebase-0.1.0.tar.gz",
  description="To make tables in python as easy as printing to the console",
  license="MIT license",
  include_package_data=True,
  name='tablebase',
  version='0.2.0',
  zip_safe=False,
  install_requires=[
      'termcolor',
  ],
)
