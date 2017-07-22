import sys
from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

urllib = 'urllib' if sys.version_info >= (3, 0) else 'urllib2'

setup(
    name='tonaledm',
    version='0.1',
    description='Tools for key estimation and evaluation in EDM',
    author='Angel Faraldo',
    author_email='angelfaraldo@gmail.com',
    url='https://github.com/angelfaraldo/tonaledm',
    packages=['tonaledm'],
    long_description=long_description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords='audio music mir dsp',
    license='MIT',
    install_requires=[
        'numpy >= 1.7.0',
        'scipy >= 0.14.0',
        'pandas >= 0.18.1',
        'future',
        urllib,
        'xlrd',
        'xlwt'
    ],
    extras_require={
        'display': ['matplotlib>=1.5.0',
                    'scipy>=0.16.0'],
        'testing': ['matplotlib>=2.0.0']
    }
)
