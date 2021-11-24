import os
from flask import ( 
    Flask, render_template
)
from turbo_flask import Turbo
import threading
import time
from flaskr.tables import get_alerts_table

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

    from . import settings
    app.register_blueprint(settings.bp)

    return app

app = create_app()
turbo = Turbo(app)

@app.context_processor
def inject_tables():
    alerts_table = get_alerts_table()
    return {'alerts_table' : alerts_table}

def update_alerts_table():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.update(render_template('alertstable.html'), 'alertstable'))

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_alerts_table).start()