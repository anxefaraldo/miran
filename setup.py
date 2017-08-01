#!/usr/local/bin/python
#  -*- coding: UTF-8 -*-

import sys
from setuptools import setup
# from setuptools import find_packages


with open('README.rst') as f:
    long_description = f.read()

urllib = 'urllib' if sys.version_info >= (3, 0) else 'urllib2'

setup(
    name='miran',
    version='0.1',
    description='mir and music analysis tools in python.',
    author='Ángel Faraldo',
    author_email='angelfaraldo@gmail.com',
    url='https://github.com/angelfaraldo/miran',
    packages=['miran'],  #, 'key'],
    # packages=find_packages(exclude='misc'),
    long_description=long_description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
    keywords='music analysis mir',
    license='MIT',
    install_requires=[
        'appscript',
        'future',
        'librosa',
        'madmom',
        'matplotlib',
        'mido',
        'music21',
        'numpy',
        'pandas',
        'scipy',
        urllib,
        'xlrd',
        'xlwt'
    ],
    extras_require={},
    data_files = []
)
