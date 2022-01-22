import requests
import sys
import json

from .base import BaseIntegration

class SlackIntegration(BaseIntegration):
    @classmethod
    def name(cls):
        return "slack"

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "url": {"type": "string", "title": "Slack Webhook URL"},
            },
            "secret": [ "name", "url" ],
        }

    def alert(self, message):
        url = self.configuration['url']
        slack_data = {
            "text": message
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

