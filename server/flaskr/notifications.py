import os
import csv
from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import get_db
from werkzeug.utils import secure_filename
from . import wificheck

bp = Blueprint('notifications', __name__, url_prefix = '/notifications')

'''
def get_network_id():
    db = get_db()
    ssid = get_SSID()
    row = db.execute(
        "SELECT network_id FROM networks WHERE SSID LIKE ?", (ssid,)
    ).fetchone() # For some reason this gets a Sqlite3.Row object or something and its properties are the column names...
    id = row["network_id"]
    return id

def insert_endpoints(csv):
    network_id = int(get_network_id())

    db = get_db()
    db.execute(
        "DELETE FROM endpoints WHERE network_id = ?", (network_id,)
    )
    db.commit()

    csv_arr = [x.split(",") for x in csv.split("\r\n")]
    csv_arr.pop(0)
    print(csv_arr)
    try:
        for ep, a in csv_arr:
            print(ep,a)
            db.execute(
                "INSERT INTO endpoints (endpoint, accessible, network_id) VALUES (?, ?, ?)", (ep, a, network_id,)
            )
            
    except:
        return False
    db.commit()
    return True
'''

def insert_phone_number(phone_number):
    print("Inserting phone_number: ", phone_number)

@bp.route('/configure', methods = ('GET', 'POST'))
def upload():
    if request.method == 'POST':
        print(request.form)

        error = None
        # TODO: Validate the request and form values

        if error is None:
            if request.form["phone_number"] is not None:
                phone_number = request.form["phone_number"]
                print("Phone Number: ", phone_number)

                # Insert the phone number
                insert_phone_number(phone_number)
            
            if request.form["alert_interval"] is not None:
                # Insert the alert_interval
                print("Alert Interval: ", request.form["alert_interval"])

            if request.form["webhook_url"] is not None:
                # Insert the webhook_url
                print("Webhook URL: ", request.form["webhook_url"])
            
            flash('Thank you')
        else:
            flash(error)

    return redirect(url_for('home'))