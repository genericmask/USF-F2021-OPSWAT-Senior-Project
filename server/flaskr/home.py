from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import insert_notification_settings, insert_endpoints
from flaskr.validators.csvEndpointsValidator import csvEndpointsValidator
from wtforms import Form, BooleanField, StringField, IntegerField, validators, ValidationError
from wtforms.fields.html5 import TelField, URLField
import phonenumbers

ALLOWED_EXTENSIONS = {'csv'}

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

bp = Blueprint('home', __name__, url_prefix = '/')

@bp.route('/', methods = ('GET',))
def home():
    notifications_form = NotificationsForm()
    return render_template('home.html', notifications_form=notifications_form)

@bp.route('/notifications', methods = ('GET', 'POST'))
def notifications():
    notifications_form = NotificationsForm(request.form)
    print(notifications_form.data)
    if request.method == 'POST' and notifications_form.validate():

        error = None
        # TODO: Validate the request and form values
        form_params = ["phone_number", "sms_alert_interval", "webhook_url", "heart_beat_alert_interval"]

        if error is None:
            print(insert_notification_settings(request.form))
                       
            flash('Submitted Successfully')
        else:
            flash(error)

    return render_template('home.html', notifications_form=notifications_form)

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
                    flash('Thank you')
                    
                    return render_template('home.html', notifications_form=notifications_form)

        flash(error)
            

    return render_template('home.html', notifications_form=notifications_form)