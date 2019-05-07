#!/usr/bin/env python

import sys
from setuptools import setup
from mpyq import __version__ as version

setup(name='mpyq',
      version=version,
      author='Aku Kotkavuo',
      author_email='aku.kotkavuo@gmail.com',
      url='http://github.com/eagleflo/mpyq/',
      description='A Python library for extracting MPQ (MoPaQ) files.',
      py_modules=['mpyq'],
      entry_points={
        'console_scripts': ['mpyq = mpyq:main']
      },
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Archiving',
      ],
      install_requires=[
          'argparse; python_version < "2.7"',
          'mock; python_version < "3.3"',
          'six',
          ]
     )
