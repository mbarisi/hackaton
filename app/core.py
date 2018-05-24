# -*- coding: utf-8 -*-
import os

from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_babelex import Babel
from flask_login import login_required, current_user
from flask_security import roles_accepted

from app import params
from . import database

def create_app(config=None):
    app = Flask('app')
    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY=b'baetorkploggdhrykdorngvhdkdofgndhdfduhfkjg',
        # USERNAME='admin',
        # PASSWORD='default',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'app.db'),
        # DEFAULT_MAIL_SENDER='info@site.com',
        SECURITY_REGISTERABLE=True,
        SECURITY_CONFIRMABLE=False,
        SECURITY_RECOVERABLE=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECURITY_PASSWORD_SALT=b'xxx',
        SECURITY_SEND_REGISTER_EMAIL=False,
        SECURITY_USER_IDENTITY_ATTRIBUTES='email'
        # SECURITY_POST_LOGIN_VIEW='/'
    ))

    # Setup babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        override = request.args.get('lang')

        if override:
            session['lang'] = override

        rv = session.get('lang', 'en')
        return rv

    db, user_datastore, profile_datastore, admin_datastore = database.setup(app)

    app.context_processor(lambda: dict(params=params))

    # Views
    @app.route('/')
    @login_required
    def home():
        user_id = current_user.get_id()
        user = user_datastore.get_user(user_id)
        # This one is a list of Role names
        print(int(str(user.roles[0])[5:-1]))
        if int(str(user.roles[0])[5:-1]) == 1:
            return redirect(url_for('home_user'))
        elif int(str(user.roles[0])[5:-1]) == 2:
            return redirect(url_for('admin'))

    # Views
    @app.route('/home_user', methods=['GET', 'POST'])
    @roles_accepted('user')
    def home_user():
        user_id = current_user.get_id()
        if request.method == 'POST':
            profile_datastore.send_answer(user_id, answer=request.form.get('rsvp'))
        return render_template('home_user.html', user=user_datastore.get_user(user_id))

    @app.route('/prepare_info')
    @login_required
    def prepare_info():
        user_id = current_user.get_id()
        return render_template('prepare_info.html', user=user_datastore.get_user(user_id))


    #  Views
    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():

        return render_template('terms.html')

    # Views
    @app.route('/admin', methods='GET POST'.split())
    @roles_accepted('admin')
    def admin():
        if request.method == 'POST':
            if request.form.get('email') and request.form.get('email') != 'Enter donors email':
                if admin_datastore.increase_donations(email=request.form.get('email')):
                    flash('donation added')
        return render_template(
                'admin.html'
            )


    @app.route('/admin_donors', methods='GET POST'.split())
    @roles_accepted('admin')
    def admin_donors():
        if request.form.get('invite'):
            admin_datastore.send_invite(user_id=request.form.get('id'))
        return render_template(
            'admin_donors.html',
            admins=admin_datastore.get_all_admins(),
            donors=admin_datastore.get_all_donors()
        )

    @app.route('/find_donors', methods='GET POST'.split())
    @roles_accepted('admin')
    def find_donors():
        return render_template(
            'find_donors.html'
        )

    # Views
    @app.route('/profile', methods='POST GET'.split())
    @login_required
    def profile():
        user_id = current_user.get_id()

        if request.method == 'POST':
            if request.form.get('blood'):
                profile_datastore.change_user_info(user_id, blood=request.form.get('blood'))

            if request.form.get('age') and request.form.get('age') != 'Enter your age here':
                print(request.form.get('age'))
                profile_datastore.change_user_info(user_id, age=request.form.get('age'))

            if request.form.get('address') and request.form.get('address') != 'Enter your address here':
                print(request.form.get('address'))
                profile_datastore.change_user_info(user_id, address=request.form.get('address'))

            if request.form.get('postcode_num') and request.form.get('postcode_num') != 'Enter your postcode here':
                print(request.form['postcode_num'])
                profile_datastore.change_user_info(user_id, postcode_num=request.form.get('postcode_num'))

            if request.form.get('email_job') and request.form.get('email_job') != 'Enter email here':
                print(request.form['email_job'])
                profile_datastore.change_user_info(user_id, email_job=request.form.get('email_job'))

            # print({info: request.form[info] for info in 'blood age address postcode_num email_job'.split()},
            #       user_id)
            # profile_datastore.change_user_info(
            #     **{info: request.form[info] for info in 'blood age address postcode_num email_job'.split()},
            #     user_id=user_id
            #  )

        return render_template(
            'profile.html',
            user = user_datastore.get_user(user_id)
        )


    return app