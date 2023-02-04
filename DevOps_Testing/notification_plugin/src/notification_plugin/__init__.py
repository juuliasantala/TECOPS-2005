import logging

from pyats.easypy.plugins.bases import BasePlugin
from pyats import configuration

import requests

logger = logging.getLogger(__name__)

class CustomWebexPlugin(BasePlugin):
    '''
    Custom Webex Plugin to send detailed information about test results
    '''
    name = 'CustomWebex'
    url = "https://webexapis.com/v1/messages"
    job_details = {}

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def __init__(self, *args, **kwargs):
        self.token = configuration.get("custom_webex.token") or None
        self.space = configuration.get("custom_webex.space") or None
        super().__init__(*args, **kwargs)

    def post_job(self, job):
        logger.info(f"Preparing the Webex message...")

        # Retrieving runtime details
        runtime_details = job.runtime.details()
        message = f"# {job.name}\n"
        icons = {"passed":"✅", "failed":"❌"}
        for task in runtime_details.tasks:
            message += f"**{task.id}**\n"
            if not task.result:
                for section in task.sections:
                    message += f"- {icons[str(section.result)]} {section.name}\n"
                    if not section.result or str(section.type) == "Testcase":
                        for subsection in section.sections:
                            message += f"  - {icons[str(subsection.result)]} {subsection.name}\n"
                            if not subsection.result:
                                for step in subsection.sections:
                                    message += f"    -  {icons[str(step.result)]} {step.name}: {str(step.result)}"
                                    if not step.result:
                                        message += f" -> {step.details[0]}"
                                    message += "\n"

            message += "------\n\n"

        logger.info("Creating the message to send to Webex...")
        # message = json.dumps(self.job_details)
        print(message)
        response = requests.post(self.url, headers=self.headers, json={"markdown":message, "roomId":self.space})
        logger.info(f"Message sent with the status code: {response.status_code}")
        if response.status_code != 200:
            logger.info(response.text)
