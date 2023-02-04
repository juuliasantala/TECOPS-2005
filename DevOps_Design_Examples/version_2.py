#!/usr/bin/env python
'''
Example for seminar of the second iteration version of your code.
This iteration adds the use of functions.
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

def get_cookie(ip_address, username, password, port = 443, verify = False):
    ''' Get authentication cookie. '''
    url = f"https://{ip_address}:{port}/j_security_check"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {"j_username": username, "j_password": password}

    response = requests.post(url, headers=headers, data=body, verify=verify, timeout=30)
    if response.status_code != 200:
        print(f"Error:\n{response.text}")
        return -1

    return response.cookies

def get_xsrf_token(ip_address, cookies, port = 443, verify = False):
    ''' Get a cross-site request forgery prevention token. '''
    url = f"https://{ip_address}:{port}/dataservice/client/token"
    response = requests.get(url, cookies=cookies, verify=verify, timeout=30)
    if response.status_code != 200:
        print(f"Error:\n{response.text}")
        return -1
    return response.text

def print_devices(ip_address, cookies, xsrf_token, port = 443, verify = False):
    ''' Get devices of the vManage. '''
    url = f"https://{ip_address}:{port}/dataservice/device"
    headers = {"Content-Type":"application/json", "X-XSRF-TOKEN": xsrf_token}
    response = requests.get(url, headers=headers,
                            cookies=cookies, verify=verify, timeout=30)
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
    user = input("Username? ")
    pw = getpass.getpass(prompt="Password? ")

    my_cookies = get_cookie(ip, user, pw)
    my_xsrf_token = get_xsrf_token(ip, my_cookies)
    print_devices(ip, my_cookies, my_xsrf_token)
