#! /usr/bin/env python
# encoding: utf-8

import os
import sys

from codecs import open

from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='wordpress_json',
    version='0.2.4',
    description='A thin wrapper for the Wordpress JSON API',
    long_description=readme + '\n\n' + history,
    author='Raul Taranu, Julie MacDonell, Dimitar Roustchev',
    author_email='raul.taranu@stylight.com, julie.macdonell@stylight.com',
    url='http://github.com/stylight/python-wordpress-json',
    license='MIT License',
    packages=find_packages(),
    package_data={'': ['*.rst']},
    include_package_data=True,
    install_requires=[
        'requests',
        'six',
    ],
    setup_requires=["nose>=1.0"],
    test_suite='nose.collector',
    keywords='wordpress json api'
)
