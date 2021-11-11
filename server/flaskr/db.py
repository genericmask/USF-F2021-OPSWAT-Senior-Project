import sqlite3
from contextlib import closing
from wificheck import check_network
import click
from flask import current_app, g
from flask.cli import with_appcontext

DEFAULT_NOTIFICATION_SETTINGS = {
    'phone_number' : '',
    'sms_alert_interval' : 10,
    'webhook_url' : '',
    'heart_beat_alert_interval' : 10,
}

def init_db():
    with closing(get_db_connection()) as db:
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db_connection():
    db = sqlite3.connect(
        "./instance/flaskr.sqlite",
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = make_dicts
    return db

def init_app(app):
    app.cli.add_command(init_db_command)

def get_from_db(sql, params, one = False):
    with closing(get_db_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute(sql, params).fetchall()
            return (rows[0] if rows else None) if one else rows

def insert_into_db(sql, params):
    with closing(get_db_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                sql, params
            )
            connection.commit()

def get_SSID():
    return check_network()

def insert_SSID(ssid):
    insert_into_db("INSERT INTO networks (SSID) VALUES (?)", (ssid,))

def get_network_id():
    ssid = get_SSID()

    row = get_from_db("SELECT network_id FROM networks WHERE SSID LIKE ?", (ssid,))

    if len(row) < 1: # The network id wasn't found so lets insert it and all the things associated with it
        insert_SSID(ssid)
        insert_notification_settings(DEFAULT_NOTIFICATION_SETTINGS)
        row = get_from_db("SELECT network_id FROM networks WHERE SSID LIKE ?", (ssid,))
    
    id = row[0]["network_id"]

    return int(id)

# @return : an array containing an object with ip (str) and accessible (bool) properties
def get_endpoints():
    network_id = get_network_id()
    rows = get_from_db("SELECT endpoint, accessible FROM endpoints WHERE network_id = ?", (network_id,))
    endpoints = [{'ip': ep["endpoint"], 'accessible': ep["accessible"]=='TRUE'} for ep in rows]
    return endpoints

# @return : a dictionary containing the phone_number, sms_alert_interval, webhook_url
def get_notification_settings():
    network_id = get_network_id()
    row = get_from_db("SELECT * FROM notification_settings WHERE network_id = ?", (network_id,), True)
    return row

def get_alerts():
    network_id = get_network_id()
    alerts = get_from_db("SELECT * FROM alerts INNER JOIN endpoints ON alerts.endpoint_id=endpoints.endpoint_id WHERE endpoints.network_id = ?", (network_id,))
    return alerts

# @param=settings : a dictionary containing the phone_number, sms_alert_interval, webhook_url
def insert_notification_settings(settings):
    #print("Inserting settings into DB: ", settings)

    network_id = get_network_id()
    insert_into_db("DELETE FROM notification_settings WHERE network_id = ?", (network_id,))

    try:
        insert_into_db("INSERT INTO notification_settings (network_id, phone_number, sms_alert_interval, webhook_url, heart_beat_alert_interval) VALUES (?, ?, ?, ?, ?)", (network_id, settings["phone_number"], settings["sms_alert_interval"], settings["webhook_url"], settings["heart_beat_alert_interval"],))
    except BaseException as err:
        #print(f"Unexpected {err=}, {type(err)=}")
        return False
    
    return True

# @param=csv : a string containing the contents of a csv file where the first line is the column names and rows are ended with '\r\n'
def insert_endpoints(csv):
    network_id = get_network_id()

    insert_into_db("DELETE FROM endpoints WHERE network_id = ?", (network_id,))

    csv_arr = [x.split(",") for x in csv.split("\r\n")]

    if len(csv_arr) > 0:
        csv_arr.pop(0)
        #print(csv_arr)
        try:
            for ep, a in csv_arr:
                insert_into_db("INSERT INTO endpoints (endpoint, accessible, network_id) VALUES (?, ?, ?)", (ep, a, network_id,))
        except BaseException as err:
            #print(f"Unexpected {err=}, {type(err)=}")
            return False
    else:
        return False

    return True
