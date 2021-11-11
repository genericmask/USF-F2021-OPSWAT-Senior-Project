import os
from flaskr.db import get_alerts, get_endpoints
from flask import ( 
    Flask, render_template
)
from turbo_flask import Turbo
import threading
import time

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import home
    app.register_blueprint(home.bp)

    return app

app = create_app()
turbo = Turbo(app)

# @arr : an array of dictionaries
def makeTable(arr):
    # Table is a dictionary with a "header" property containing an array of column names
    # and a "rows" property containing an array of arrays that contain column values  
    table = {
        "header" : [],
        "rows" : []
    }
    if len(arr) > 0:
        keys = arr[0].keys()
        for key in keys:
            table["header"].append(key.upper())
        
        for element in arr:
            row = []
            for key in keys:
                row.append(element[key])
            table["rows"].append(row)

    return table

def getEndpointsTable():
    endpoints = get_endpoints()  
    return makeTable(endpoints)

def getAlertsTable():
    alerts = get_alerts()
    return makeTable(alerts)

@app.context_processor
def inject_tables():
    alerts_table = getAlertsTable()
    return {'alerts_table' : alerts_table}

def update_alerts_table():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.update(render_template('alertstable.html'), 'alertstable'))

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_alerts_table).start()