#! /usr/bin/env python
# encoding: utf-8

from setuptools import setup

try:
    long_description = open('README.md', 'r').read()
except IOError:
    long_description = "A thin wrapper around the Wordpress JSON API"

setup(
    name='wordpress_json',
    version='0.1.1',
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
