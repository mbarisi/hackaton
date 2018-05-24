# coding=utf-8
from flask_sqlalchemy import SQLAlchemy


class ProfileDatastore(object):
    def __init__(
            self,
            db: SQLAlchemy,
            user_model,
            blood_model
    ):
        self._db = db
        self._user_model = user_model
        self._blood_model = blood_model

    def _get_user(self, id:int):
        return self._user_model.query.filter_by(id=id).first()

    def change_user_info(
            self,
            user_id: int,
            blood=None,
            age=None,
            address=None,
            postcode_num=None,
            email_job=None
    ):
        user = self._get_user(user_id)

        if blood is not None:
            b_type = self._blood_model.query.filter_by(name=blood).first()
            exists=user.blood_type
            # print(exists)
            # if len(exists):
            #     print(len(exists))
            #     user.blood_type=b_type[0]
            #     # self._db.session.delete(user.blood_type)
            if not exists:
                user.blood_type.append(b_type)
                self._db.session.add(user)
        print(age, address, postcode_num, email_job)
        if age is not None:
            user.age = age

        if address is not None:
            user.address = address

        if postcode_num is not None:
            user.postcode_num = postcode_num

        if email_job is not None:
            user.email_job = email_job

        self._db.session.commit()

    def send_answer(
            self,
            user_id: int,
            answer
    ):
        user = self._get_user(user_id)
        user.message = False
        user.answer = answer

        self._db.session.commit()
