#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='py-itime',
    version='0.0.1',
    author='Avins Wang',
    author_email='avinswang@gmail.com',
    url='https://github.com/AvinsWang/itime',
    download_url="http://pypi.python.org/pypi/itime/",
    description="Chained call time handlers",
    long_description=open(os.path.join(here, 'README.md')).read(),
    license='LGPL-3.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['iTime'],
    classifiers=['Topic :: Utilities', 
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 3.6'],
)
