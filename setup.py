#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright wh1100717
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from os.path import dirname, join
from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)


with open(join(dirname(__file__), 'rqalpha_mod_shipane/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='rqalpha-mod-shipane',
    version=version,
    description='RQAlpha Mod ShipanE to support stock real time trading',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=[]),
    author='wh1100717',
    author_email='me@emptystack.net',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='https://github.com/wh1100717/rqalpha-mod-ShiPanE',
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
