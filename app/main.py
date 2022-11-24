import secrets

import flask_login
from flask import Blueprint, render_template, flash, url_for, redirect

from flask_login import login_required, current_user
from flask import request

from .database_manager import *

# from .models import BotInfo


import json
import logging

main = Blueprint('main', __name__)


@main.route('/')
def index():
    create_db()
    # tags = get_all_tags()
    # print(tags)

    return render_template('index.html')


@main.route('/search-vehicle', methods=["POST"])
def search_vehicle():
    registration = request.form.get("registration")
    if registration:
        vehicle = get_vehicle_record_by_registration(registration_number=registration)

        return render_template("index.html", vehicles=vehicle)
    return render_template("index.html")


@main.route('/add-vehicle')
def add_vehicle():
    return render_template("add_vehicle.html")


@main.route('/add-vehicle', methods=["POST"])
def add_vehicle_post():
    registration = request.form.get("registration")
    capacity = request.form.get("capacity")
    description = request.form.get("description")
    if registration and capacity:
        add_vehicle_info(registration_number=registration, maximum_capacity=capacity, description=description)
        flash("Vehicle Added Successfully", "success")
    return render_template("index.html")


@main.route('/add_record', methods=["POST"])
def add_record():
    data=request.get_json()
    vehicle = data["registration"]
    number_of_people = data["number_of_people"]
    speed = data["speed"]
    
    
    if vehicle and number_of_people and speed:
        print(vehicle,number_of_people,speed)
        add_vehicle_record(number_of_people=number_of_people, speed=speed, vehicle_number_plate=vehicle)
    return "OK"
