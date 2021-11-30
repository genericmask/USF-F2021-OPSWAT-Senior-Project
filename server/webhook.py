import requests

def webhook(webhook_url, ip, failure_description, start_datetime, end_datetime=None):
    x = {"ip": ip,
        "failure_description": failure_description,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime}

    if webhook_url != '':
        try:
            requests.post(webhook_url, json=x, timeout=5)
        except requests.exceptions.RequestException as e:  # This will handle everything. TODO: Handle individual cases and give user feedback
            print(e)