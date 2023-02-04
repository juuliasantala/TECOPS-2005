#!/usr/bin/env python
'''
Job to run the tests.

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
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

import os
from pyats.easypy import run
from pyats import topology

def full_path(script_name):
    test_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_path, script_name)

def main(runtime):
    testbed = topology.loader.load(full_path("testbed.yaml"))
    destinations = (
        '10.105.22.34',
        '10.105.0.10',
        '8.8.8.8'
        )

    urls = (
        "www.thousandeyes.com",
        "www.google.com",
        "ciscolive.com"
    )
    interfaces = "GigabitEthernet1/0/2,GigabitEthernet1/0/23,GigabitEthernet1/0/24"
    runtime.job.name = 'PRE-TEST'

    run(testscript=full_path('testcases/config_validation.py'),
        runtime=runtime,
        taskid="Configuration Validation",
        testbed=testbed,
        interfaces=interfaces)

    run(testscript=full_path('testcases/functional_validation.py'),
        runtime=runtime,
        taskid="Functional Validation",
        testbed=testbed,
        destinations=destinations)

    run(testscript=full_path('testcases/sla_validation.py'),
        runtime=runtime,
        taskid="SLA Validation",
        urls=urls)
