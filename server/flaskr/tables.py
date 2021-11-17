from flaskr.db import get_alerts, get_endpoints
import time

# @arr : an array of dictionaries
# @header : an array of strings to be used for the column names. Should correspond to the number of keys used
# @keys : an array of strings that can be used as keys for @arr
def make_table(arr, header = [], keys = []):
    # Table is a dictionary with a "header" property containing an array of column names
    # and a "rows" property containing an array of arrays that contain column values  
    table = {
        "header" : header,
        "rows" : []
    }
    if len(arr) > 0:
        if len(keys) == 0: keys = arr[0].keys()
        if len(header) == 0:
            for key in keys:
                table["header"].append(key.upper())
        
        for element in arr:
            row = []
            for key in keys:
                row.append(element[key])
            table["rows"].append(row)
    else:
        if len(header) > 0:
            table["rows"] = [["" for _ in header]]

    return table

def get_alerts_table():
    alerts = get_alerts()
    for alert in alerts:
        if alert["start_datetime"] != None:
            alert["start_datetime"] = time.ctime(int(float(alert["start_datetime"])))
        if alert["end_datetime"] != None:
            alert["end_datetime"] = time.ctime(int(float(alert["end_datetime"])))

    header = ["ALERT ID", "FAILURE TYPE", "ENDPOINT ID", "ENDPOINT", "START DATE TIME", "END DATE TIME"]
    keys = ["alert_id", "failure_type", "endpoint_id", "endpoint", "start_datetime", "end_datetime"]
    return make_table(alerts, header, keys)

def get_endpoints_table():
    endpoints = get_endpoints()
    header = [ "ID", "IP", "ACCESSIBLE"]
    keys = ["id", "ip", "accessible"]
    return make_table(endpoints, header, keys)