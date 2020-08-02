import os
from typing import List
from requests import Response, post


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:

    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = 'do-not-reply@sandboxe4339243883e4aaa9a4c5f6ee478c132.mailgun.org'

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        mapi_key = os.environ.get('MAILGUN_API_KEY', None)
        mdomain = os.environ.get('MAILGUN_DOMAIN', None)

        print(f"API_KEY = {mapi_key}   DOMAIN = {mdomain}")

        print("IF API KEY Code")
        if mapi_key is None:
            raise MailGunException('Failed to load Mailgun API Key.')

        print("IF DOMAIN Code")
        if mdomain is None:
            raise MailGunException('Failed to load Mailgun DOMAIN.')

        print("Into Response Code")
        response = post(
            f'https://api.mailgun.net/v3/{mdomain}/messages',
            auth=('api', mapi_key),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text,
                'html': html
            }
        )
        print(f"Out of Response Code:: {response.status_code}")
        if response.status_code != 200:
            print(response.status_code)
            print(response.json())
            raise MailGunException('An error occurred while sending e-mail.')
        return response
