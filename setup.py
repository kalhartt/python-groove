#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from codecs import open
from setuptools import setup

cffi_modules = [
    'src/groove/_build.py:ffi_groove',
]

packages = [
    'groove',
]

requires = [
]

with open('src/groove/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name='groove',
    version=version,
    description='Python music backend',
    author='kalhartt',
    author_email='kalhartt@gmail.com',
    url='https://github.com/kalhartt/python-groove',
    license='MIT',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'': 'src'},
    include_package_data=True,
    setup_requires=['cffi>=1.0.0'],
    cffi_modules=cffi_modules,
    install_requires=requires,
    zip_safe=False,
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Sound/Audio',
    ),
)
