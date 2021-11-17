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
# @header : an array of strings to be used for the column names. Should correspond to the number of keys used
# @keys : an array of strings that can be used as keys for @arr
def makeTable(arr, header = [], keys = []):
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

def getAlertsTable():
    alerts = get_alerts()
    for alert in alerts:
        if alert["start_datetime"] != None:
            alert["start_datetime"] = time.ctime(int(float(alert["start_datetime"])))
        if alert["end_datetime"] != None:
            alert["end_datetime"] = time.ctime(int(float(alert["end_datetime"])))

    header = ["ALERT ID", "FAILURE TYPE", "ENDPOINT ID", "ENDPOINT", "START DATE TIME", "END DATE TIME"]
    keys = ["alert_id", "failure_type", "endpoint_id", "endpoint", "start_datetime", "end_datetime"]
    return makeTable(alerts, header, keys)

@app.context_processor
def inject_tables():
    alerts_table = getAlertsTable()
    return {'alerts_table' : alerts_table}

def update_alerts_table():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.update(render_template('alertstable.html'), 'alertstable'))

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_alerts_table).start()