#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='py-itime',
    version='0.0.2',
    author='Avins Wang',
    author_email='avinswang@gmail.com',
    url='https://github.com/AvinsWang/py-itime',
    download_url="http://pypi.python.org/pypi/py-itime/",
    description="Time package supporting chain call",
    long_description=open(os.path.join(here, 'ReadMe.rst')).read(),
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
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 3.6'],
)
