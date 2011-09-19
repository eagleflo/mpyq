#!/usr/bin/env python

import sys
from setuptools import setup

setup(name='mpyq',
      version='0.1.9',
      author='Aku Kotkavuo',
      author_email='aku@hibana.net',
      url='http://github.com/arkx/mpyq/',
      description='A Python library for extracting MPQ (MoPaQ) files.',
      py_modules=['mpyq'],
      entry_points={
        'console_scripts': ['mpyq = mpyq:main']
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Archiving',
      ],
      install_requires=['argparse'] if float(sys.version[:3]) < 2.7 else [],
     )
