#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of a Webhook receiver using Flask.

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
"""

from flask import Flask, request

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

app = Flask(__name__)

@app.route('/my_webhook_address', methods=["POST"])
def webhook_received():
    """ Function to print webhook payload on the terminal window """

    data = request.json # save the data that was sent to you into variable 'data'

    print(f"\n{'*'*30}\n")

    print(f"Alert received from network {data['networkName']}:")
    print(f"{data['deviceModel']} ({data['deviceSerial']}): {data['alertType']}")
    print(f"Occured at: {data['occurredAt']}")

    print(f"\n{'*'*30}\n")

    return "Data received"
