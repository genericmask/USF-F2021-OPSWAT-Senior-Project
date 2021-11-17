import requests

def webhook(webhook_url, ip, failure_description, start_datetime, end_datetime=None):
    x = {"ip": ip,
        "failure_description": failure_description,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime}

    requests.post(webhook_url, data=x)