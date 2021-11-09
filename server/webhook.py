import alert
import json
import requests
import datetime
dataList = []
url = "https://webhook.site/baad271b-1c0e-4559-8d97-1be1566c0690"
with open('webhookData.txt') as f:
    for jsonobj in f:
        postDict = json.loads(jsonobj)
        dataList.append(postDict)
for obj in dataList:
    requests.post(url, data=obj)
