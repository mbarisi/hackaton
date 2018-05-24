# -*- coding: utf-8 -*-
# create our blueprint :)
from flask import Blueprint, request, session, redirect, url_for, abort, \
    render_template, flash, current_app

bp = Blueprint('core', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != current_app.config['EMAIL']:
            error = 'Invalid email'
        elif request.form['password'] != current_app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('core.show_entries'))
    return render_template('login/login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('core.show_entries'))


@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return None


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return None
