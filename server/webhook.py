import alert
import json
import requests
import datetime

from server.alert import Alert


def Post():
    dataList = Alert.getJson()
    url = "https://webhook.site/baad271b-1c0e-4559-8d97-1be1566c0690"

    for obj in dataList:
        requests.post(url, data=obj)
