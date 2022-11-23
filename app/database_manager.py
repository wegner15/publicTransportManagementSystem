import json

from .models import *
import secrets
from . import db


def add_vehicle_record(number_of_people, speed, vehicle_number_plate):
    vehicle = VehicleInformation.query.filter_by(registration_number=vehicle_number_plate).first()
    if not vehicle:
        return None
    record = TravelRecord(vehicle_id=vehicle.id, number_of_people=number_of_people, speed=speed)
    db.session.add(record)
    db.session.commit()


def add_vehicle_info(registration_number, maximum_capacity, description):
    vehicle = VehicleInformation(registration_number=registration_number, maximum_capacity=maximum_capacity,
                                 description=description)
    db.session.add(vehicle)
    db.session.commit()


def get_vehicle_record_by_registration(registration_number):
    vehicle = VehicleInformation.query.filter_by(registration_number=registration_number).first()
    if not vehicle:
        return  None
    records = TravelRecord.query.filter_by(vehicle_id=vehicle.id).all()
    return records


def create_db():
    # db.drop_all()
    db.create_all()
