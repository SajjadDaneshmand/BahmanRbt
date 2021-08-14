from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')


@login_required
@bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')
