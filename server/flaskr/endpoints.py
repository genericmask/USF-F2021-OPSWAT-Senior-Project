import os
import csv
from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import get_db, insert_endpoints
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/caseypersonal/Documents'
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
                insert_endpoints(file.read().decode("utf-8"))
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('Thank you')
                
                return redirect(url_for('home'))

        flash(error)
            

    return redirect(url_for('home'))