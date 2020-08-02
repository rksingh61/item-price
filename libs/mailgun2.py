import requests

def send_email():
    return requests.post(
            "https://api.mailgun.net/v3/sandboxe4339243883e4aaa9a4c5f6ee478c132.mailgun.org/messages",
            auth=("api", "key-8qptm9o9xdzp588t87hwb5mmtehcsd57"),
            data={
                "from": "Excited User <excited@sandboxe4339243883e4aaa9a4c5f6ee478c132.mailgun.org>",
                "to": ["rksingh61@yahoo.com"],
                "subject": "Hello Friend",
                "text": "Testing Mailgun"})

print(send_email())
