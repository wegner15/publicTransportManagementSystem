from datetime import datetime

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class VehicleInformation(db.Model):
    id = db.Column('vehicle_id', db.Integer, primary_key=True)
    registration_number = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50))
    maximum_capacity = db.Column(db.Integer)


class TravelRecord(db.Model):
    id = db.Column('Record_id', db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, nullable=False)
    record_date_time = db.Column(db.DateTime, default=datetime.utcnow)
    number_of_people = db.Column(db.Integer)
    speed = db.Column(db.Integer)
