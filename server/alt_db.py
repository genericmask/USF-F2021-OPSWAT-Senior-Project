import sqlite3
from contextlib import closing
from wificheck import check_network

def get_db_connection():
    
    db = sqlite3.connect(
        "./instance/flaskr.sqlite",
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    return db

# utility functions

def get_SSID():
    return check_network()

def insert_SSID(ssid):
    with closing(get_db_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO networks (SSID) VALUES (?)", (ssid,)
            )
            connection.commit()


def get_network_id():
    ssid = get_SSID()

    with closing(get_db_connection()) as connection:
        with closing(connection.cursor()) as cursor:            
            row = cursor.execute(
                "SELECT network_id FROM networks WHERE SSID LIKE ?", (ssid,)
            ).fetchone() # For some reason this gets a Sqlite3.Row object or something and its properties are the column names...
    
    try:
        id = row["network_id"]
    except TypeError: # The network id wasn't found so lets insert it
        insert_SSID(ssid)
        return get_network_id()
    return int(id)

# @return : an array containing an object with ip (str) and accessible (bool) properties
def get_endpoints():
    network_id = get_network_id()
    
    with closing(get_db_connection()) as connection:
        with closing(connection.cursor()) as cursor:            
            rows = cursor.execute(
                "SELECT endpoint, accessible FROM endpoints WHERE network_id = ?", (network_id,)
            ).fetchall() # TODO: Not sure if fetchall will work with more than one network_id

    endpoints = [{'ip': ep[0], 'accessible': ep[1]=='TRUE'} for ep in rows]

    #print("endpoints: ", endpoints)

    return endpoints

# @return : a dictionary containing the phone_number, sms_alert_interval, webhook_url
def get_notification_settings():
    network_id = get_network_id()

    d = {"phone_number": '', "sms_alert_interval": '', "webhook_url": '', "heart_beat_alert_interval": ''}
    
    with closing(get_db_connection()) as connection:
        with closing(connection.cursor()) as cursor:  
            row = cursor.execute(
                "SELECT * FROM notification_settings WHERE network_id = ?", (network_id,)
            ).fetchone()

    # TODO: This will throw a key error if the row doesn't contain anything
    for key in d:
        d[key] = row[key]

    return d