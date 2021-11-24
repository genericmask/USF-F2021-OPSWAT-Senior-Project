from flask import (
    Blueprint, g, request, render_template, session, flash
)
from flaskr.tables import get_endpoints_table

bp = Blueprint('home', __name__, url_prefix = '/')

@bp.route('/', methods = ('GET',))
def home():
    return render_template('home.html', endpoints_table=get_endpoints_table())