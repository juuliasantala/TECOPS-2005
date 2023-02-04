#!/usr/bin/env python
'''
Example for seminar of the third iteration version of your code.
This iteration moves from functions to object oriented approach.
This code retrieves all the network devices from vManage.

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


import getpass
import requests
import urllib3
urllib3.disable_warnings()

class vManage():
    ''' Class for vManage data and methods '''
    authentication_cookie = None
    xsrf_token = None

    def __init__(self,
                ip_address: str,
                username: str,
                password: str,
                port: int = 443,
                verify: bool = False):
        '''
        Initialize class with connection details.
        Authentication is done during initialization.
        '''

        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.verify = verify # False if self-signed certificate
        self.base_url = f"https://{ip_address}:{port}"

        # authenticate
        self.get_cookie()
        self.get_xsrf_token()

    def get_cookie(self) -> None:
        ''' Get authentication cookie. '''
        url = f"{self.base_url}/j_security_check"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {"j_username": self.username, "j_password": self.password}

        response = requests.post(url,
                                headers=headers,
                                data=body,
                                verify=self.verify,
                                timeout=30
                            )
        if response.status_code != 200:
            print(f"Error:\n{response.text}")
        else:
            self.authentication_cookie = response.cookies

    def get_xsrf_token(self) -> None:
        ''' Get a cross-site request forgery prevention token. '''
        url = f"{self.base_url}/dataservice/client/token"
        response = requests.get(url,
                                cookies=self.authentication_cookie,
                                verify=self.verify,
                                timeout=30
                            )
        if response.status_code != 200:
            print(f"Error:\n{response.text}")
        else:
            self.xsrf_token = response.text

    def print_devices(self) -> None:
        ''' Get devices of the vManage. '''
        url = f"{self.base_url}/dataservice/device"
        headers = {"Content-Type":"application/json", "X-XSRF-TOKEN": self.xsrf_token}
        response = requests.get(url,
                                headers=headers,
                                cookies=self.authentication_cookie,
                                verify=self.verify,
                                timeout=30)
        if response.status_code != 200:
            print(f"Error:\n{response.text}")
        else:
            print(f"\n{'* '*11}*")
            print(f"*{' '*21}*")
            print("* DEVICES IN VMANAGE: *")
            print(f"*{' '*21}*")
            print(f"{'* '*11}*\n")
            for device in response.json()["data"]:
                print(f"- {device['device-type']}: {device['host-name']} ({device['system-ip']})")

if __name__ == "__main__":

    ip = input("IP address of your vManage? ")
    user= input("Username? ")
    pw = getpass.getpass(prompt="Password? ")

    my_vmanage = vManage(ip, user, pw)
    my_vmanage.print_devices()
