#!/usr/bin/env python
'''
Configuration validation ("Is it there?") to test port status by
executing a simple DNAC API test.

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

from pyats import aetest, topology, configuration
import requests
import urllib3

# Disable warnings -- OBS not recommended in production!
urllib3.disable_warnings()

import logging

logger = logging.getLogger(__name__)

class CiscoDnaCenter():

    token = None

    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.retrieve_token()

    @property
    def headers(self):
        return {"Content-Type": "application/json","X-Auth-Token":self.token}

    @property
    def base_url(self):
        return f"https://{self.address}/dna/intent/api/v1"

    def retrieve_token(self):
        """
        This function generates an authentication token to Cisco DNA Center and which is valid for 1h
        """
        auth_url = f"https://{self.address}/dna/system/api/v1/auth/token"
        req = requests.post(
            url=auth_url,
            auth=(self.username, self.password),
            headers=self.headers,
            verify=False,
            timeout=30
        )

        if req.status_code in (200, 201):
            logger.info("Token retrieved")
            self.token = req.json()["Token"]
        else:
            print("ERROR in generate_token()")
            print(req.text)

    def get_device(self, device_ip):
        url = f"{self.base_url}/network-device"
        params = {"managementIpAddress":device_ip}
        req = requests.get(url, headers=self.headers, params=params, verify=False, timeout=30)
        print(f"Getting device {device_ip}")
        return req.json()["response"][0]["id"]

    def get_ports(self, device_ip, interfaces):
        device = self.get_device(device_ip)
        url = f"{self.base_url}/network-device/{device}/interface/poe-detail"
        params = {"interfaceNameList":interfaces}
        req = requests.get(url, headers=self.headers, params=params, verify=False, timeout=30)
        return req.json()["response"]

class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''
    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        """
        Each iteration of the marked Testcase will be passed the parameter
        "device" with the current device from the testbed.
        """
        aetest.loop.mark(InterfaceConfigTestcase, device=testbed)

class InterfaceConfigTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking port status using Cisco DNAC.
    '''

    @aetest.setup
    def get_dnac_device_interfaces(self, device, interfaces):
        addr = configuration.get('DNAC.address') or None
        user = configuration.get('DNAC.username') or None
        pw = configuration.get('DNAC.password') or None
        dnac = CiscoDnaCenter(addr, user, pw)
        self.ports = dnac.get_ports(device.connections.cli.ip, interfaces)

    @aetest.test
    def interface(self, steps, device):
        '''
        Simple port test: using Cisco DNA Center port API response, check
        that nothing is down.
        '''
        for port in self.ports:
            with steps.start(
                f"{device}: {port['interfaceName']}",
                description=f"Checking {str(device.name)} {port['interfaceName']}",
                continue_=True
                ) as step:
                try:
                    assert port["operStatus"] == "ON"
                except:
                    step.failed(f"{str(device.name)} {port['interfaceName']} is {port['operStatus']}")
                else:
                    step.passed(f"{str(device.name)} {port['interfaceName']} is ON!")

if __name__ == "__main__":
    testbed = topology.loader.load("../testbed.yaml")
    aetest.main(testbed=testbed, interfaces="GigabitEthernet1/0/2,GigabitEthernet1/0/23,GigabitEthernet1/0/24")
