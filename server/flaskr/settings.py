import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import insert_notification_settings, insert_endpoints, get_notification_settings
from flaskr.validators.csvEndpointsValidator import csvEndpointsValidator

from wtforms import Form, IntegerField, validators, ValidationError, TelField, URLField
import phonenumbers

class NotificationsForm(Form):
    phone_number                = TelField('Phone Number', [validators.DataRequired()])
    sms_alert_interval          = IntegerField('SMS Alert Interval', [validators.InputRequired(), validators.NumberRange(min=1, max=2147483647, message='Minimum allowed is 1')])
    webhook_url                 = URLField('Webhook URL', [validators.DataRequired()])
    heart_beat_alert_interval   = IntegerField('Heart Beat Alert Interval', [validators.InputRequired(), validators.NumberRange(min=1, max=2147483647, message=(u'Minimum allowed is 1'))])

    def validate_phone_number(form, field):
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
    print(settings)
    notifications_form = NotificationsForm()
    notifications_form.phone_number.data = settings['phone_number']
    notifications_form.sms_alert_interval.data = settings['sms_alert_interval']
    notifications_form.webhook_url.data = settings['webhook_url']
    notifications_form.heart_beat_alert_interval.data = settings['heart_beat_alert_interval']
    return notifications_form

@bp.route('/', methods = ('GET',))
def home():
    notifications_form = get_filled_notifications_form()
    return render_template('settings.html', notifications_form=notifications_form)

@bp.route('/notifications', methods = ('GET', 'POST'))
def notifications():
    notifications_form = NotificationsForm(request.form)
    print(notifications_form.data)
    if request.method == 'POST' and notifications_form.validate():
        error = None

        if error is None:
            print(insert_notification_settings(request.form))
                       
            flash('Submitted Successfully')
        else:
            flash(error)

    return render_template('settings.html', notifications_form=notifications_form), 422

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
                # Should be safe to read and decode file.
                csv_string = file.read().decode("utf-8")

                # Check for file content validity
                error = csvEndpointsValidator(csv_string)

                if error is None:
                    # Insert if nothing was wrong
                    insert_endpoints(csv_string)
                    flash('Upload Successful')
                    
                    return render_template('settings.html', notifications_form=notifications_form), 422

        flash(error)

    return render_template('settings.html', notifications_form=notifications_form), 422