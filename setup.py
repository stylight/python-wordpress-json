#! /usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

try:
    long_description = open('README.rst', 'r').read()
except IOError:
    long_description = "A thin wrapper around the Wordpress JSON API"

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='wordpress_json',
    version='0.1.2',
    description='A thin wrapper for the Wordpress JSON API',
    author='Raul Taranu, Dimitar Roustchev',
    author_email='raul.taranu@stylight.com, dimitar.roustchev@stylight.com',
    url='http://github.com/stylight/python-wordpress-json',
    license='MIT License',
    packages=['wordpress_json'],
    install_requires=[
        'requests',
    ],
    setup_requires=["nose>=1.0"],
    test_suite='nose.collector',
    keywords='wordpress json api'
)
