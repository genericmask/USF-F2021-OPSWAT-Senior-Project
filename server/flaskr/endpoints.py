from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import insert_endpoints
from flaskr.validators.csvEndpointsValidator import csvEndpointsValidator

ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('endpoints', __name__, url_prefix = '/endpoints')

def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                # Should be safe to read and decode file.
                csv_string = file.read().decode("utf-8")

                # Check for file content validity
                error = csvEndpointsValidator(csv_string)

                if error is None:
                    # Insert if nothing was wrong
                    insert_endpoints(csv_string)
                    flash('Thank you')
                    
                    return redirect(url_for('home'))

        flash(error)
            

    return redirect(url_for('home'))