from flask import Blueprint, jsonify, request
from config.config import Config, token_required
import utils.database as data_utils

festivity_blue_print = Blueprint('festivity_blue_print', __name__)


@festivity_blue_print.route('/create-festivity', methods=['POST'])
@token_required
def create_festivity(current_user):
    data = request.get_json()
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            for city in data.get('cities'):
                is_valid = database.select_festivity(city, data.get('date'))
                if len(is_valid) != 0:
                    return jsonify({'state': f'A festivity already exists for {city} on that date'}), 400
                database.add_festivity(city, data.get('date'))
            return jsonify({'state': 'SUCCESS'}), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 400
    except Exception as ex:
        return jsonify({'state': 'ERROR: ' + str(ex)}), 400   


@festivity_blue_print.route('/get-all-festivities', methods=['GET'])
@token_required
def get_all_festivities(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            festivities = database.select_festivities()
            festivities_json = [
                {'ID': festivity[0], 'City': festivity[1], 'Date': festivity[2].strftime('%Y-%m-%d')} for festivity
                in festivities]
            return jsonify(festivities_json), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 400


@festivity_blue_print.route('/delete-festivity', methods=['DELETE'])
@token_required
def delete_festivity(current_user):
    data = request.get_json()
    id = data.get('id')
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            affected_rows = database.delete_festivity(id)
            if(affected_rows == 0):
                return jsonify({'state': 'Festivity could not be deleted since that ID does not exist'}), 400
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return jsonify({'state': 'SUCCESSFUL'}), 200


"""If email is null, user current_user. Else, use the provided email"""
@festivity_blue_print.route('/get-user-festivities', methods=["POST"])
@token_required
def user_festivities(current_user):
    data = request.get_json()
    email:str = current_user
    if (data.get('Email') != None): email = data.get('Email') 
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            festivities = database.select_festivity_by_user(email)
            festivities_json = [{'ID': festivity[0], 'Date': festivity[2].strftime('%Y-%m-%d')} for festivity in
                                festivities]
        print(festivities_json)
        return jsonify(festivities_json), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    
