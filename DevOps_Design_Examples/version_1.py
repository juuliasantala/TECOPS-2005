#!/usr/bin/env python
'''
Example for seminar of the first iteration version of your code.
The first version has working code, but doesn't define functions
or classes.
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

username = input("Username? ")
password = getpass.getpass(prompt="Password? ")

url = "https://10.55.100.17:443/j_security_check"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
body = {"j_username": username, "j_password": password}

response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)

cookies = response.cookies

url = "https://10.55.100.17:443/dataservice/client/token"
response = requests.get(url, cookies=cookies, verify=False, timeout=30)

xsrf_token = response.text

url = "https://10.55.100.17:443/dataservice/device"
headers = {"Content-Type":"application/json", "X-XSRF-TOKEN": xsrf_token}
response = requests.get(url, headers=headers, cookies=cookies, verify=False, timeout=30)

print(f"\n{'* '*11}*")
print(f"*{' '*21}*")
print("* DEVICES IN VMANAGE: *")
print(f"*{' '*21}*")
print(f"{'* '*11}*\n")
for device in response.json()["data"]:
    print(f"- {device['device-type']}: {device['host-name']} ({device['system-ip']})")
