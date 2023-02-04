#! /bin/env python
'''
Notification plugin example for pyATS
--------------------------------

Setup:
python setup.py install

--------------------------------
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


from setuptools import setup, find_packages

setup(
    # plugin package details
    name = 'notification-plugin',
    version = '1.0',
    description = 'pyATS notification plugin example',
    license = 'Cisco Sample Code License, Version 1.1',
    author = 'Juulia Santala',
    author_email = 'jusantal@cisco.com',

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    # project packages & directory
    packages = find_packages(where = 'src'),
    package_dir = {
        '': 'src',
    },

    # package dependencies
    install_requires =  ['setuptools', 'pyats', 'requests'],
)