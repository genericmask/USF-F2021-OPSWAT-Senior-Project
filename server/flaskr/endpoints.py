import os
import csv
from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import get_db
from werkzeug.utils import secure_filename
from . import wificheck

UPLOAD_FOLDER = '/Users/caseypersonal/Documents'
ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('endpoints', __name__, url_prefix = '/endpoints')

def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_SSID():
    return "FiOS-ZL17E-5G"

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

@bp.route('/upload', methods = ('GET', 'POST'))
def upload():
    if request.method == 'POST':
        
        error = None

        if 'file' not in request.files:
            error = 'No file'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'No selected file'
            elif not allowed_file(file.filename):
                error = 'Invalid file extension.'
            
            if error is None:
                insert_endpoints(file.read().decode("utf-8"))
                filename = secure_filename(file.filename)
                # temp_file = wificheck.check_network()
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('Thank you')
                
                return redirect(url_for('home'))

        flash(error)
            

    return redirect(url_for('home'))