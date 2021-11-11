from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import insert_notification_settings, insert_endpoints, get_endpoints
from flaskr.validators.csvEndpointsValidator import csvEndpointsValidator
from wtforms import Form, BooleanField, StringField, IntegerField, validators, ValidationError, TelField, URLField
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

# @arr : an array of dictionaries
def makeTable(arr, header = []):
    # Table is a dictionary with a "header" property containing an array of column names
    # and a "rows" property containing an array of arrays that contain column values  
    table = {
        "header" : header,
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

bp = Blueprint('home', __name__, url_prefix = '/')

@bp.route('/', methods = ('GET',))
def home():
    notifications_form = NotificationsForm()
    return render_template('home.html', notifications_form=notifications_form, endpoints_table=getEndpointsTable())

@bp.route('/notifications', methods = ('GET', 'POST'))
def notifications():
    notifications_form = NotificationsForm(request.form)
    print(notifications_form.data)
    if request.method == 'POST' and notifications_form.validate():

        error = None
        form_params = ["phone_number", "sms_alert_interval", "webhook_url", "heart_beat_alert_interval"]

        if error is None:
            print(insert_notification_settings(request.form))
                       
            flash('Submitted Successfully')
        else:
            flash(error)
    # https://github.com/hotwired/turbo-rails/issues/12 Turbo requires rendering form responses with 422
    return render_template('home.html', notifications_form=notifications_form, endpoints_table=getEndpointsTable()), 422

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
                    endpoints_table = getEndpointsTable()
                    
                    return render_template('home.html', notifications_form=notifications_form, endpoints_table=endpoints_table), 422

        flash(error)

    return render_template('home.html', notifications_form=notifications_form, endpoints_table=getEndpointsTable()), 422