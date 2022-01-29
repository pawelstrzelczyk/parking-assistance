import os
import sqlite3
from sqlite3 import OperationalError, IntegrityError

import flask
from flask import Flask
from flask_cors import cross_origin

max_length = 40

max_width = 30


def create_app(test_config=None):
    # create and configure the app
    flask_app = Flask("Garage Assistance", instance_relative_config=True)
    flask_app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        flask_app.config.from_pyfile('config.py', silent=True)
    else:
        flask_app.config.from_mapping(test_config)

    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    @flask_app.route('/grant-access/<string:plate>/<int:grant>', methods=['POST'])
    @cross_origin()
    def access(plate, grant):
        db = sqlite3.connect('../main_controllers/garage.db', timeout=25)
        cur = db.cursor()
        try:
            cur.execute("UPDATE access SET isAllowed=(?) WHERE license_plate_number=(?)",
                        (1 if grant != 0 else 0, plate))
            db.commit()
            db.close()
            return {'success': True}
        except OperationalError:
            return {'success': False}
        except IntegrityError:
            return {'success': False,
                    'reason': 'DB Integrity Violation'}

    @flask_app.route('/add-vehicle/<string:plate>/<float:length>/<float:width>/<int:allowed>', methods=['POST'])
    @cross_origin()
    def add_car(plate, length, width, allowed):
        if length > max_length or width > max_width:
            return {"error": "Error: too small vehicle size!"}
        if length < 5 or width < 5:
            return {"error": "Error: too small vehicle size!"}

        db = sqlite3.connect('../main_controllers/garage.db', timeout=25)
        cur = db.cursor()
        try:
            cur.execute('INSERT INTO car_parameters(width, length, license_plate_number) VALUES(?, ?, ?)',
                        (width, length, plate))
            cur.execute('INSERT INTO access VALUES (?, ?)', (plate, 1 if allowed != 0 else 0))
            print('car added')
            db.commit()
            db.close()
            return {'success': True}
        except OperationalError:
            return {'success': False}

    @flask_app.route('/get-vehicles', methods=['GET'])
    @cross_origin()
    def get_cars():
        cars = []

        db = sqlite3.connect('../main_controllers/garage.db', timeout=25)
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM car_parameters NATURAL JOIN access')
            for row in cur:
                car = {'width': row[0], 'length': row[1], 'license_plate': row[2], 'hasAccess': row[3]}
                cars.append(car)
            db.close()
            response = flask.jsonify(cars)
            return response
        except OperationalError:
            return {'success': False}

    @flask_app.route('/get-logs', methods=['GET'])
    @cross_origin()
    def get_logs():
        logs = []

        db = sqlite3.connect('../main_controllers/garage.db', timeout=25)
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM access_log")
            for row in cur:
                log = {'timestamp': row[0], 'isAllowed': row[1], 'license_plate': row[2]}
                logs.append(log)
            db.close()
            response = flask.jsonify(logs)
            return response
        except OperationalError:
            return {'success': False}

    @flask_app.route('/get-gas-logs', methods=['GET'])
    @cross_origin()
    def get_gas_logs():
        logs = []

        db = sqlite3.connect('../main_controllers/garage.db', timeout=25)
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM gas_alerts')
            for row in cur:
                log = {'timestamp': row[0]}
                logs.append(log)
            db.close()
            response = flask.jsonify(logs)
            return response
        except OperationalError:
            return {'success': False}

    @flask_app.route('/get-accesses', methods=['GET'])
    @cross_origin()
    def get_accesses():
        accesses = []

        db = sqlite3.connect('../main_controllers/garage.db', timeout=25)
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM access")
            for row in cur:
                acc = {'license_plate_number': row[0], 'is_allowed': row[1]}
                accesses.append(acc)
            db.close()
            response = flask.jsonify(accesses)
            return response
        except OperationalError:
            return {'success': False}

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(debug=True, host='0.0.0.0')
