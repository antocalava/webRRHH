from flask import Blueprint, jsonify, request
from config.config import Config, token_required
import utils.database as data_utils
from datetime import datetime

home_office_blue_print = Blueprint('home_office_blue_print', __name__)

@home_office_blue_print.route('/get-user-home-office', methods=["POST"])
@token_required
def get_user_home_office(current_user):
    data = request.get_json() 
    email = data.get('email')

    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            home_office = database.get_home_office(email)
            home_office_json = [{'Date': day[1].strftime('%Y-%m-%d'), 'Type': day[2]} for day in home_office]
            return jsonify(home_office_json), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500


@home_office_blue_print.route('/get-department-home-office', methods=["GET"])
@token_required
def get_department_home_office(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            days = database.get_department_home_office(current_user)
            department_days = [{'FullName': day[3], 'Date': day[1].strftime('%Y-%m-%d'), 'Type': day[2]} for day in days]

            return jsonify(department_days)
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'})


@home_office_blue_print.route('/delete-home-office', methods=["DELETE"])
@token_required
def delete_home_office(current_user):
    data = request.get_json()
    day = datetime.strptime(data.get('day'), '%d/%m/%Y').date()

    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            rows_affected = database.delete_home_office(current_user, day)

            if rows_affected <= 0:
                return jsonify({'state': 'There is no request for that day'}), 400

    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return jsonify({'state': 'SUCCESS'}), 200


@home_office_blue_print.route('/get-home-office', methods=["GET"])
@token_required
def get_home_office_current_user(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            days = database.get_home_office(current_user)
            home_office_days = [{'Date': day[1].strftime('%Y-%m-%d'), 'Type': day[2]} for day in days]
            return jsonify(home_office_days), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500


@home_office_blue_print.route('/add-home-office', methods=['POST'])
@token_required
def add_home_office(current_user):
    data = request.get_json()
    day = datetime.strptime(data.get('day'), '%d/%m/%Y').date()
    type = data.get('type')

    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.create_home_office(current_user, day, type)
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return jsonify({'state': 'SUCCESS'}), 200
