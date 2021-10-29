import os
import csv
from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import get_db, insert_notification_settings
from werkzeug.utils import secure_filename
from . import wificheck

bp = Blueprint('notifications', __name__, url_prefix = '/notifications')

@bp.route('/configure', methods = ('GET', 'POST'))
def upload():
    if request.method == 'POST':
        print(request.form)

        error = None
        # TODO: Validate the request and form values
        form_params = ["phone_number", "alert_interval", "webhook_url"]

        if error is None:
            print(insert_notification_settings(request.form))
                       
            flash('Thank you')
        else:
            flash(error)

    return redirect(url_for('home'))