import os
from flask import (
    Blueprint, g, redirect, request, render_template, session, url_for, flash
)
from flaskr.db import get_db
from werkzeug.utils import secure_filename
from . import wificheck

UPLOAD_FOLDER = '/Users/caseypersonal/Documents'
ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('endpoints', __name__, url_prefix = '/endpoints')

def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods = ('GET', 'POST'))
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # temp_file = wificheck.check_network()
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('Thank you')
            
            return redirect(url_for('home'))
            #return 'Thank you'
        else:
            flash('Invalid file extension.')

    return redirect(url_for('home'))