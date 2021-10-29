from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import insert_notification_settings

bp = Blueprint('notifications', __name__, url_prefix = '/notifications')

@bp.route('/configure', methods = ('GET', 'POST'))
def upload():
    if request.method == 'POST':
        print(request.form)

        error = None
        # TODO: Validate the request and form values
        form_params = ["phone_number", "sms_alert_interval", "webhook_url", "heart_beat_alert_interval"]

        if error is None:
            print(insert_notification_settings(request.form))
                       
            flash('Thank you')
        else:
            flash(error)

    return redirect(url_for('home'))