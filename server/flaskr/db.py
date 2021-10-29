import sqlite3
from typing import Any
from wificheck import check_network

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# utility functions

def get_SSID():
    return check_network()

def insert_SSID(ssid):
    db = get_db()
    db.execute(
        "INSERT INTO networks (SSID) VALUES (?)", (ssid,)
    )
    db.commit()


def get_network_id():
    db = get_db()
    ssid = get_SSID()
    row = db.execute(
        "SELECT network_id FROM networks WHERE SSID LIKE ?", (ssid,)
    ).fetchone() # For some reason this gets a Sqlite3.Row object or something and its properties are the column names...
    try:
        id = row["network_id"]
    except TypeError: # The network id wasn't found so lets insert it
        insert_SSID(ssid)
        return get_network_id()
    return int(id)


# endpoints

# @param=csv : a string containing the contents of a csv file where the first line is the column names and rows are ended with '\r\n'
def insert_endpoints(csv):
    network_id = get_network_id()

    db = get_db()
    db.execute(
        "DELETE FROM endpoints WHERE network_id = ?", (network_id,)
    )
    db.commit()

    csv_arr = [x.split(",") for x in csv.split("\r\n")]
    csv_arr.pop(0)
    #print(csv_arr)
    try:
        for ep, a in csv_arr:
            #print(ep,a)
            db.execute(
                "INSERT INTO endpoints (endpoint, accessible, network_id) VALUES (?, ?, ?)", (ep, a, network_id,)
            )
            db.commit()
    except BaseException as err:
        #print(f"Unexpected {err=}, {type(err)=}")
        return False
    
    return True

# @return : an array containing an object with ip (str) and accessible (bool) properties
def get_endpoints():
    network_id = get_network_id()
    db = get_db()

    rows = db.execute(
        "SELECT endpoint, accessible FROM endpoints WHERE network_id = ?", (network_id,)
    ).fetchall() # TODO: Not sure if fetchall will work with more than one network_id

    endpoints = [{'ip': ep[0], 'accessible': ep[1]=='TRUE'} for ep in rows]
    
    #print("endpoints: ", endpoints)

    return endpoints

# notifications

# @param=settings : a dictionary containing the phone_number, sms_alert_interval, webhook_url
def insert_notification_settings(settings):
    print("Inserting settings into DB: ", settings)

    network_id = get_network_id()

    db = get_db()
    db.execute(
        "DELETE FROM notification_settings WHERE network_id = ?", (network_id,)
    )
    db.commit()

    try:
        db.execute(
            "INSERT INTO notification_settings (network_id, phone_number, sms_alert_interval, webhook_url, heart_beat_alert_interval) VALUES (?, ?, ?, ?, ?)", (network_id, settings["phone_number"], settings["sms_alert_interval"], settings["webhook_url"], settings["heart_beat_alert_interval"],)
        )
        db.commit()
    except BaseException as err:
        #print(f"Unexpected {err=}, {type(err)=}")
        return False
    
    return True

# @return : a dictionary containing the phone_number, sms_alert_interval, webhook_url, heart_beat_alert_interval
def get_notification_settings():
    network_id = get_network_id()
    db = get_db()

    d = {"phone_number": '', "sms_alert_interval": '', "webhook_url": '', "heart_beat_alert_interval": ''}
    
    row = db.execute(
        "SELECT * FROM notification_settings WHERE network_id = ?", (network_id,)
    ).fetchone()

    # TODO: This will throw a key error if the row doesn't contain anything
    if len(row.keys()) > 1:
        for key in d:
            d[key] = row[key]

    return d


    

    