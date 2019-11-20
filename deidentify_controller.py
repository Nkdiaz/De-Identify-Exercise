import flask
import re
from flask import request, jsonify
from datetime import datetime, date
import sqlite3
from deidentify_utils import calculate_age, dict_factory, zipcode_mask, zipcode_clean, extract_year, notes_cleanup


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(ValueError) 
def handle_value_error(error):
    response = {
        "status_code" : 400,
        "message" : str(error)
    }
    return jsonify(response), 400


@app.route('/deidentify', methods = ['POST'])
def deidentify():
    req_data = request.get_json()
    age = calculate_age(req_data['birthDate']) 
    admission_date = extract_year(req_data['admissionDate'])
    discharge_date = extract_year(req_data['dischargeDate'])
    note_cleanup = notes_cleanup(req_data['notes'])
    zipResult = zipcode_clean(req_data['zipCode'])

    response = {
        "age": age,
        "zipCode": zipResult,
        "admissionYear": admission_date,
        "dischargeYear": discharge_date,
        "notes" : note_cleanup
    }
    return jsonify(response)

app.run()

