#!/usr/bin/env python

import mpyq
from distutils.core import setup

setup(name='mpyq',
      version=mpyq.__version__,
      author='Aku Kotkavuo',
      author_email='aku@hibana.net',
      url='http://github.com/arkx/mpyq/',
      description='A Python library for extracting MPQ (MoPaQ) files.',
      py_modules=['mpyq'],
      scripts=['mpyq.py'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Archiving',
      ],
     )
