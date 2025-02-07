from datetime import datetime
from flask import Blueprint, jsonify, request, current_app
from config.config import Config, token_required
import utils.database as data_utils
from utils.mailing_system import send_email, send_feedback_email
import jwt
import re

access_blue_print = Blueprint('access_blue_print', __name__)

@access_blue_print.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email_input = str(data.get('email'))
    password_input = str(data.get('password'))
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            user_login_data = database.fetch_login_data_by_email(email_input)
            
        if user_login_data:
            hash_password, salt_password = user_login_data
            if hash_password is None or salt_password is None:
                return jsonify({'message': 'Invalid user data'}), 502
            if data_utils.check_password(hash_password, salt_password, password_input):
                token = jwt.encode({'username': email_input}, current_app.config['SECRET_KEY'], algorithm='HS256')
                return jsonify({'authorization': token}), 200
            else:
                return jsonify({'message': 'Incorrect password', 'status': 'INCORRECT_PASSWORD'}), 401
        return jsonify({'message': 'User not found', 'status': 'USER_NOT_FOUND'}), 401
    except data_utils.pymssql.Error as ex:
        return jsonify({'state': 'DB error: ' + str(ex)}), 500


def is_valid_password(password: str) -> bool:
    password_length = len(password)
    if not (6 <= password_length):
        return False
    if not re.match("^[a-zA-Z0-9]+$", password):
        return False

    return True


@access_blue_print.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    data = request.get_json()
    new_password = data.get('newPassword')
    if not is_valid_password(new_password):
        return jsonify({'state': 'Invalid password'}), 401
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.update_password(current_user, new_password)
    except data_utils.pymssql.Error as ex:
        return jsonify({'state': 'DB error: ' + str(ex)}), 500
    return jsonify({'state': 'SUCCESS'}), 200


@access_blue_print.route('/get-rank', methods=["GET"])
@token_required
def get_user_rank(current_user: str):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            rank = database.get_current_user_rank(current_user)
    except data_utils.pymssql.Error as ex:
        return jsonify({'state': 'DB error: ' + str(ex)}), 500
    return jsonify({'rank': rank}), 200
    
# def generate_access_token(email):
#     SECRET_KEY = Config.SECRET_KEY
#     token = jwt.encode({'username': email}, SECRET_KEY, algorithm='HS256')
#     return token
            
@access_blue_print.route('/reset-user-password', methods=['PUT'])
@token_required
def reset_user_password(current_user):
    data = request.get_json()
    user_email = data.get('userEmail')
    default_password = 'Password123'
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.update_password(user_email, default_password)
            
        #inform user of password reset
        send_email(user_email, 'Password reset - SEBN ES SUITE',  f"<p>Your password has been reset by an administrator.</p> <br/>Your email: {user_email}<br/>New password: <b>{default_password}</b> <br/><br/>Do <i>NOT</i> share this information with anyone! <br/><br/><p>Please, <i>CHANGE YOUR PASSWORD</i> as soon as you log in.<br/>Thank you.</p>")
    except data_utils.pymssql.Error as ex:
        return jsonify({'state' : 'DB Error: ' + str(ex)}), 500
    return jsonify({'state': 'SUCCESS'}), 200


""" CAUTION, THIS RESETS THE PASWORD OF EVERY USER IN THE DATABASE """
@access_blue_print.route('/reset-all-users-password', methods=['PUT'])
@token_required
def reset_all_users_password(current_user):
    default_password = 'Password123'
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            users = database.get_users_name_mail()
            for user in users:
                user_email = user[1]
                database.update_password(user_email, default_password)
                    
                #inform user of password reset
                send_email(user_email, 'Password reset - SEBN ES SUITE',  f"<p>Your password has been reset by an administrator.</p> <br/>Your email: {user_email}<br/>New password: <b>{default_password}</b> <br/><br/>Do <i>NOT</i> share this information with anyone! <br/><br/><p>Please, <i>CHANGE YOUR PASSWORD</i> as soon as you log in.<br/>Thank you.</p>")
    except data_utils.pymssql.Error as ex:
        return jsonify({'state' : 'DB Error: ' + str(ex)}), 500
    return jsonify({'state': 'SUCCESS'}), 200


#TODO: test_send_feedback
@access_blue_print.route('/send-feedback', methods=['POST'])
@token_required
def send_feedback(current_user):
    data = request.get_json()
    tag = data.get('tag')
    title = data.get('title')
    message = data.get('message') if data.get('message') is not None else "-- No additional details have been provided --"

    try:
        send_feedback_email(current_user, tag, f"{tag} - SEBN ES SUITE HR", f"<h1>{tag}: {title}</h1>", f"<p style='color: #979797'><i>Submission date: <b>{datetime.now().strftime('%Y-%m-%d %H:%M')}</b><br/>Employee: <b>{current_user}</b></i></p><br/> <p>{message}</p>")
    except Exception as ex:
        return jsonify({'state': 'Error: ' + str(ex)}), 500
    return jsonify({'state': 'SUCCESS'}), 200
    
    
#TODO: test_forgot_password
@access_blue_print.route('/forgot-password', methods=['POST'])
def forgot_password_email():
    data = request.get_json()
    email = data.get("loginEmail")
    hr_email =  "cristina.lopez@sebn.com" #"SEBN.CHR-Everyone-ES@sebn.com" #TODO: DESCOMENTAR EN PRODUCCION
    employee_name = get_user_full_name(email)
    
    try:
        send_email(hr_email, 'Password forgotten - SEBN ES SUITE',  f"<p>{employee_name} has forgotten their password and are requesting to reset it.<br/><br/><i style='font-size:small'>Please, log-in to the Suite and search for {employee_name} in the <b>User Info</b> tab contained in the <b>HR</b> menu.</i>")
    except Exception as ex:
        return jsonify({'state': 'Error: ' + str(ex)}), 500
    return jsonify({'state': 'SUCCESS'}), 200


#returns full name by deconstructing the email
def get_user_full_name(email): 
    try:
        name_array = email.split("@")[0].split(".")
        full_name = f"{name_array[0].capitalize()} {name_array[1].capitalize()}"
    except Exception as ex:
        return jsonify({'state': "Error" + str(ex)})
    return full_name