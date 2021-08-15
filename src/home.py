from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    name = g.user[1]
    ho = 'home.home'
    return f'<h1>Hello {name}</h1><a href="{url_for(ho)}"><br>This is a index page</a>'
