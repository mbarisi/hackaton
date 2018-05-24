# coding=utf-8
from flask_sqlalchemy import SQLAlchemy


class AdminDatastore(object):
    def __init__(
            self,
            db: SQLAlchemy,
            user_model,
            role_model
    ):
        self._db = db
        self._user_model = user_model
        self._role_model = role_model

    def _get_user(self, id:int):
        return self._user_model.query.filter_by(id=id).first()

    def get_all_roles(
            self
    ):
        users = self._user_model.query.all()
        print(users)
        for user in users:
            print(user.roles[0].id, user.name)

    def get_specific_users(
            self,
            role_id: int
    ):
        spec_users = []
        users = self._user_model.query.all()
        for user in users:
            if user.roles[0].id == role_id:
                spec_users.append(user)
        return spec_users

    def get_all_admins(
            self
    ):
        return self.get_specific_users(2)

    def get_all_donors(
            self
    ):
        return self.get_specific_users(1)

    def _exists_email(
            self,
            email: str
    ):
        print(email)
        exists = self._user_model.query.filter_by(email=email).first()
        return exists

    def _get_user(
            self,
            email: str
    ):
        user = self._user_model.query.filter_by(email=email).first()
        return user

    def increase_donations(
            self,
            email: str
    ):
        if self._exists_email(email):
            user = self._get_user(email)
            print(user)
            user.donation +=1
            self._db.session.commit()
            return True
        return False

    def send_invite(
            self,
            user_id: int
    ):
        user = self._user_model.query.filter_by(id=user_id).first()
        user.message = True
        self._db.session.commit()