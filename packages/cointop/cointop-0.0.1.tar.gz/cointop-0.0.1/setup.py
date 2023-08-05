#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open  # To use a consistent encoding
from os import path

pwd = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(pwd, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'cointop',
    packages = ['cointop'],
    version = '0.0.1',
    url = 'https://github.com/miguelmota/py-cointop',
    download_url = 'https://github.com/miguelmota/py-cointop/archive/master.zip',
    author = 'Miguel Mota',
    author_email = 'hello@miguelmota.com',
    license = 'MIT License',
    description = 'Cointop python package',
    long_description = long_description,
    keywords = ['cointop'],
    include_package_data=True,
    package_data={},
    dependency_links=[],
    install_requires=[]
)