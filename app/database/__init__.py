import random
import time

from datetime import datetime
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, Security
from flask_security.forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, FieldList, RadioField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from .blood_datastore import BloodDatastore
from .admin_datastore import AdminDatastore
from .profile_datastore import ProfileDatastore


def setup(app):
    # Create database connection object
    db = SQLAlchemy(app)

    class Database(object):
        class Role(db.Model, RoleMixin):
            id = db.Column(db.Integer(), primary_key=True)
            name = db.Column(db.String(80), unique=True)
            description = db.Column(db.String(255))

        class User(db.Model, UserMixin):
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(255), unique=True)
            email_job = db.Column(db.String(255))
            name = db.Column(db.String(255), index=True, nullable=False)
            surname = db.Column(db.String(255), index=True, nullable=False)
            password = db.Column(db.String(255))
            active = db.Column(db.Boolean())

            roles = db.relationship(
                'Role',
                secondary=db.Table(
                    'roles_users',
                    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                ),
                backref=db.backref('users', lazy='dynamic')
            )

            blood_type = db.relationship(
                'Blood',
                secondary=db.Table(
                    'blood_users',
                    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                    db.Column('blood_id', db.Integer(), db.ForeignKey('blood.id'))
                ),
                backref=db.backref('users', lazy='dynamic')
            )

            def __str__(self):
                return '<User id=%s email=%s>' % (self.id, self.email)


            is_male = db.Column(db.Boolean(), default=True, nullable=False)
            gdpr = db.Column(db.Boolean())
            phone_number = db.Column(db.String(30))
            age = db.Column(db.Integer(), default=True, nullable=False)
            donation = db.Column(db.Integer(), default=0)
            address = db.Column(db.String(50))
            postcode_num = db.Column(db.String(50))

            questions = db.Column(db.String(255))
            information = db.Column(db.Boolean())
            message = db.Column(db.Boolean())
            answer = db.Column(db.Boolean())
            last_donation = db.Column(db.DateTime())

        class Blood(db.Model, RoleMixin):
                id = db.Column(db.Integer(), primary_key=True)
                name = db.Column(db.String(3))
                o_min = db.Column(db.Integer())
                o_max = db.Column(db.Integer())
                o_z = db.Column(db.Integer())


    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, Database.User, Database.Role)
    blood_datastore = BloodDatastore(db, Database.Blood)
    profile_datastore = ProfileDatastore(db, Database.User, Database.Blood)
    admin_datastore = AdminDatastore(db, Database.User, Database.Role)


    # class ExtendedLoginForm(LoginForm):
    #     email = EmailField('Email', [InputRequired()])

    class ExtendedRegisterForm(RegisterForm):
        name = StringField('Name', [InputRequired()])
        surname = StringField('Surname', [InputRequired()])
        roles = FieldList(StringField('Role', [InputRequired()]), min_entries=1, max_entries=1)
        is_male = BooleanField('Male', default=True)
        # gdpr = BooleanField('You agree to following Terms and conditions', default=False)
        gdpr = BooleanField('I accept the <a href=/terms>Terms of Service </a> '
                            'and <a href=/privacy>Privacy Notice</a>', [InputRequired()])
        # phone_number = StringField('Phone_Num', [InputRequired()])
        # email_job = StringField('Email_job')
        age = IntegerField('Age', [InputRequired()])
        # blood_type = FieldList(StringField('Blood'), min_entries=1, max_entries=1)
        # address = StringField('Address')
        # postcode_num = StringField('PostCode')

    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

    @app.before_first_request
    def before_first_request():
        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "end-user" -- unless they already exist
        # school_user = user_datastore.find_user(name='skola') or user_datastore.create_user(name='skola', password='skola')

        user_datastore.find_or_create_role(name='user', description='End user')
        user_datastore.find_or_create_role(name='admin', description='Administrator')

        blood_datastore.find_or_create_blood(name='0+', o_min=115, o_max=240, o_z=177)
        blood_datastore.find_or_create_blood(name='0-', o_min=38, o_max=78, o_z=58)
        blood_datastore.find_or_create_blood(name='A-', o_min=46, o_max=96, o_z=71)
        blood_datastore.find_or_create_blood(name='A+', o_min=100, o_max=210, o_z=155)
        blood_datastore.find_or_create_blood(name='B-', o_min=38, o_max=82, o_z=60)
        blood_datastore.find_or_create_blood(name='B+', o_min=23, o_max=50, o_z=36)
        blood_datastore.find_or_create_blood(name='AB-', o_min=8, o_max=18, o_z=13)
        blood_datastore.find_or_create_blood(name='AB+', o_min=16, o_max=36, o_z=26)

        db.session.commit()

    return db, user_datastore, profile_datastore, admin_datastore