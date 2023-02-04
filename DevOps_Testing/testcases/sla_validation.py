#!/usr/bin/env python
'''
SLA validation ("Does it perform??") to test SLA by executing a
simple ThousandEyes test.

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

from pyats import aetest, configuration
import requests
import time

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def mark_tests_for_looping(self, urls):
        aetest.loop.mark(PerformanceTestcase, my_url=urls)

class PerformanceTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking performance of websites.
    '''
    @aetest.setup
    def run_test_in_TE(self, steps, my_url):
        headers = {"Authorization": f"Bearer {configuration.get('TE.bearer') or None}"}

        with steps.start(
            f"Running ThousandEyes test on {my_url}", continue_=True
            ) as step:
            try:
                url = "https://api.thousandeyes.com/v6/endpoint-instant/agent-to-server.json"
                payload = {
                    "agentSelectorType": "ANY_AGENT",
                    "maxMachines": 5,
                    "testName": "API Instant test",
                    "serverName": my_url
                }
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response = response.json()
                test_id = response["endpointTest"][0]["testId"]
            except:
                step.failed(f'Invalid URL {my_url}')
            else:
                step.passed(f'Ran the test with {my_url}')

        with steps.start(
            f"Retrieving ThousandEyes performance data for {my_url}", continue_=True
            ) as step:
            for i in range (6):
                print(f"Trying to retrieve data ({i})...")
                url = f"https://api.thousandeyes.com/v6/endpoint-data/tests/net/metrics/{test_id}.json"
                response = requests.get(url, headers=headers, timeout=30)
                response = response.json()
                if response["endpointNet"]["metrics"]:
                    self.te_test = {"url":my_url, "result":response["endpointNet"]["metrics"]}
                    print(self.te_test)
                    step.passed(f"TE tests succesful")
                print("sleep for 10 seconds") # It takes a moment for the metrics to generate
                time.sleep(10)
            step.failed("Couldn't retrieve metrics data")

    @aetest.test
    def performance(self, steps):
        '''
        Simple performance test: Using the reponse from ThousandEyes tests, test for
        the appropriate quality of service.
        '''
        with steps.start(
            f"Checking latency of {self.te_test['url']}", continue_=True
            ) as step:
            latency = self.te_test["result"][0]["avgLatency"]
            try:
                assert latency < 32
            except:
                step.failed(f'Latency too high ({latency})')
            else:
                step.passed(f'Latency good ({latency})')

        with steps.start(
            f"Checking loss of {self.te_test['url']}", continue_=True
            ) as step:
            loss = self.te_test["result"][0]["loss"]
            try:
                assert loss == 0.0
            except:
                step.failed(f'Loss too high ({loss})')
            else:
                step.passed(f'Loss good ({loss})')

        with steps.start(
            f"Checking jitter of {self.te_test['url']}", continue_=True
            ) as step:
            jitter = self.te_test["result"][0]["jitter"]
            try:
                assert jitter < 15
            except:
                step.failed(f'Jitter too high ({jitter})')
            else:
                step.passed(f'Jitter good ({jitter})')

if __name__ == "__main__":
    my_urls = ("www.thousandeyes.com", "www.google.com", "ciscolive.com")

    aetest.main(urls=my_urls)