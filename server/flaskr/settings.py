import functools
from io import TextIOWrapper
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from flaskr.turbo_flash import turbo_flash
from flaskr.db import insert_notification_settings, insert_endpoints, get_notification_settings
from flaskr.validators.csvEndpointsValidator import csvEndpointsValidator

from wtforms import Form, IntegerField, validators, ValidationError, TelField, URLField
import phonenumbers

class NotificationsForm(Form):
    phone_number                = TelField('Phone Number', [])
    sms_alert_interval          = IntegerField('SMS Alert Interval', [validators.InputRequired(), validators.NumberRange(min=1, max=2147483647, message='Minimum allowed is 1')])
    webhook_url                 = URLField('Webhook URL', [])
    heart_beat_alert_interval   = IntegerField('Heart Beat Alert Interval', [validators.InputRequired(), validators.NumberRange(min=1, max=2147483647, message=(u'Minimum allowed is 1'))])

    def validate_phone_number(form, field):
        if len(field.data) == 0:
            return
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            try:
                input_number = phonenumbers.parse("+1"+field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                    raise ValidationError('Invalid phone number.')
            except:
                raise ValidationError('Invalid phone number.')

ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('settings', __name__, url_prefix='/settings')

def get_filled_notifications_form():
    settings = get_notification_settings()
    notifications_form = NotificationsForm()
    notifications_form.phone_number.data = settings['phone_number']
    notifications_form.sms_alert_interval.data = settings['sms_alert_interval']
    notifications_form.webhook_url.data = settings['webhook_url']
    notifications_form.heart_beat_alert_interval.data = settings['heart_beat_alert_interval']
    return notifications_form

def replace_notifications_form_and_flash(notifications_form, message=''):
    from flaskr import turbo
    if turbo.can_stream():
        return turbo.stream([
            turbo.replace(
                render_template('notifications.html', notifications_form=notifications_form),
                target="turbo-notifications"
            ),
            turbo.replace(
                render_template("_turbo_flashing.html.j2", message=message, category="error"),
                target="turbo-flash",
            )
        ]
        )
    else:
        return False

@bp.route('/', methods = ('GET',))
def home():
    notifications_form = get_filled_notifications_form()
    return render_template('settings.html', notifications_form=notifications_form)

@bp.route('/notifications', methods = ('GET', 'POST'))
def notifications():
    notifications_form = NotificationsForm(request.form)
    message = ''

    if request.method == 'POST':
        if notifications_form.validate():
            print(insert_notification_settings(request.form))
            message = "Submitted Successfully"
    
    return replace_notifications_form_and_flash(notifications_form, message)
        

def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/endpoints', methods = ('GET', 'POST'))
def endpoints():
    notifications_form = NotificationsForm()
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
                # Check for file content validity
                csvfile = TextIOWrapper(file, encoding="utf-8")
                error = csvEndpointsValidator(csvfile)

                if error is None:
                    # Insert if nothing was wrong
                    insert_endpoints(csvfile)
                    csvfile.close()
                    return turbo_flash("Upload Successful")
                    
                csvfile.close()

        return turbo_flash(error)

    return render_template('settings.html', notifications_form=notifications_form)