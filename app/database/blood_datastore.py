# coding=utf-8
from flask_sqlalchemy import SQLAlchemy


class BloodDatastore(object):
    def __init__(
            self,
            db: SQLAlchemy,
            blood_model
    ):
        self._db = db
        self._blood_model = blood_model

    def _create_blood_type(
            self,
            name,
            o_min,
            o_max,
            o_z
    ):
        return self._db.session.add(self._blood_model(name=name, o_min=o_min, o_max=o_max, o_z=o_z))
        # self._db.session.add(blood)
        # self._db.session.flush()
        # self._db.session.commit()

    def _find_blood_type(
            self,
            name: str,
    ):
        return self._blood_model.query.filter_by(name=name).first()

    def _find_or_create_blood_type(self, name, o_min, o_max, o_z):
        return self._find_blood_type(name) or self._create_blood_type(name, o_min, o_max, o_z)

    def find_or_create_blood(
            self,
            name,
            o_min,
            o_max,
            o_z
    ):
        self._find_or_create_blood_type(name, o_min, o_max, o_z)
