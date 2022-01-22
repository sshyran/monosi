from monosi_notifications.integrations.base import BaseIntegration
from monosi import mail
from flask_mail import Message

class EmailIntegration(BaseIntegration):
    @classmethod
    def name(cls):
        return "email"

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "addresses": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": "true",
                }
            },
            "required": [ "name", "addresses" ]
        }

    def alert(self, text):
        recipients = self.configuration['addresses']

        try:
            message = Message(recipients=recipients, subject="Monosi Bot: There was an alert!", html=text)
            mail.send(message)
        except Exception:
            print("There was an error sending the email")

