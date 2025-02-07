from flask import Blueprint, jsonify, request
from config.config import Config, token_required
import utils.database as data_utils
from utils.mailing_system import send_email
from datetime import datetime
from decimal import Decimal
from datetime import timedelta
from collections import defaultdict

holiday_blue_print = Blueprint('holiday_blue_print', __name__)


@holiday_blue_print.route('/request', methods=['POST'])
@token_required
def create_request(current_user):
    data = request.get_json()
    partial_day = bool(data.get('partialDay'))
    hours_partial = Decimal(data.get('hours'))
    bucket_start = data.get('bucketStart')

    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            starting_day = datetime.strptime(data['startingDay'], '%d/%m/%Y').date()
            finishing_day = datetime.strptime(data['finishingDay'], '%d/%m/%Y').date()
            current_datetime = datetime.now()
            total_quantity = (finishing_day - starting_day).days + 1
            
            #si es partial day, recalcular total quantity
            if partial_day:
                finishing_day = starting_day
                total_quantity = hours_partial

            if starting_day.weekday() >= 5 or finishing_day.weekday() >= 5:
                return jsonify({'state': 'You can not choose a non-working day as a vacation day'}), 400
            
            user_festivities = [festivity[2].strftime('%Y-%m-%d') for festivity in database.select_festivity_by_user(current_user)]
            if user_festivities.count(starting_day.strftime('%Y-%m-%d')) > 0 and user_festivities.count(finishing_day.strftime('%Y-%m-%d')) > 0:
                return jsonify({'state': 'You can not request vacations starting or ending on a festivity'}), 400

            days_type = get_user_days_buckets_ordered(current_user, bucket_start)
           
            user_days = Decimal(0)
            for bucket, quantity in days_type:
                user_days += quantity
            if total_quantity > user_days:
                return jsonify({'state': 'You have marked more days than you have been given'}), 400
            
            if partial_day:
                if total_quantity <= 0:  
                    return jsonify({'state': 'Error: Partial day quantity can not be zero'}), 400
            else:
                if total_quantity < 1:
                    return jsonify({'state': 'Error: Invalid date range'}), 400

            isDuplicated = database.select_holiday_request_range(current_user, starting_day, finishing_day)
            if isDuplicated > 0:
                return jsonify({'state': 'One of the range of days has already been requested'}), 400

            #insertamos primer registro
            database.add_log_calendar_request(current_user, current_datetime, starting_day, finishing_day, partial_day, 'CREATED', total_quantity)

            calendarRequestId = database.select_last_user_calendar_request(current_user)[0][0]

            current_day = starting_day
            total_days =  1 if partial_day else total_quantity
            for each in range(total_days):
                # Verifica si el día actual es sábado, domingo o festivo
                if current_day.weekday() >= 5 or user_festivities.count(current_day.strftime('%Y-%m-%d')) > 0:
                    # Si es sábado, domingo o festivo o telebrajo, omite el proceso de agregar datos al calendario para este día
                    current_day += timedelta(days=1)
                    continue

                # Agrego 1 linea en DataBulk por dia (si de donde obtengo los dias no llega a remaining_quantity, obtengo del siguiente bucket)
                remaining_quantity = Decimal(1)
                if partial_day:
                    remaining_quantity = total_quantity
                for i, (bucket, quantity) in enumerate(days_type):
                    if quantity <= 0: continue
                    quantity_for_day = min(quantity, remaining_quantity)
                    database.add_calendar_data_bulk(calendarRequestId, current_day, partial_day, bucket, quantity_for_day)
                    days_type[i] = (bucket, quantity - quantity_for_day)
                    remaining_quantity -= quantity_for_day
                    if remaining_quantity <= 0: break

                current_day += timedelta(days=1)
                
            #UPDATE USER DAYS (we reorder the list according to column order in DB for insert)
            buckets_order = ["ExtraHours","Holidays","LiqTravel"]
            days_type_reordered = []
            for i, cur_bucket in enumerate(buckets_order):
                cur_bucket_value = next(x[1] for x in days_type if x[0] == cur_bucket)
                days_type_reordered.append((cur_bucket, cur_bucket_value)) 
            database.update_user_days(days_type_reordered[0][1], days_type_reordered[1][1], days_type_reordered[2][1], current_user)

            #SEND EMAILS
            responsible_email = database.get_user_boss(current_user)[0][0]
            current_username = get_user_full_name(current_user)
            #to responsible
            send_email(responsible_email, f"New holiday signing request [SEBN ES SUITE]", f"Employee: {current_username}<br/>Starting Day: {starting_day}<br/>Finishing Day: {finishing_day}")
            #to employee
            send_email(current_user, f"New holiday request [SEBN ES SUITE]", f"Status: Pending<br/>Starting Day: {starting_day}<br/>Finishing Day: {finishing_day}")

            database._conn.commit() 
    except data_utils.pymssql.Error as ex:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': 'DB Error, doing rollback: ' + str(ex)}), 500
    return jsonify({'state': 'SUCCESS'}), 200

#TODO: test_get_user_days_buckets_sorted
"""
Depending on which is bucket_start, we find it in days_type and put it in the front, 
then we sort the rest of the list depending on its values (from smallest to greatest value)
"""
def get_user_days_buckets_ordered(email, bucket_start):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            user_days_buckets = database.get_user_days(email)
            days_type = [("ExtraHours", Decimal(user_days_buckets[1])), ("Holidays", Decimal(user_days_buckets[2])),("LiqTravel", Decimal(user_days_buckets[3]))]
        
        #we isolate our selected bucket, then remove it from the list
        chosen_tuple = next(x for x in days_type if x[0] == bucket_start)
        days_type_filtered = [x for x in days_type if x[0] != bucket_start]
        #then we sort list without bucket_start
        days_type_sorted = sorted(days_type_filtered, key=lambda x: x[1], reverse=False) 
            
        user_days_buckets_ordered = [chosen_tuple] + days_type_sorted  
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return user_days_buckets_ordered


@holiday_blue_print.route('/get-user-holidays', methods=['GET'])
@token_required
def get_user_vacations(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            vacations = database.get_user_holidays(current_user)
            vacations_json = [
                {'id': vacation[0], 'startingDay': vacation[3], 'finishingDay': vacation[4], 'partialDay': vacation[5], 'status': vacation[6], 'totalQuantity': vacation[7]} for vacation in vacations]
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return jsonify(vacations_json), 200


@holiday_blue_print.route('/delete-user-holidays', methods=["DELETE"])
@token_required
def delete_user_vacations(current_user):
    data = request.get_json()
    id_request = data.get('id')
    try:
        delete_vacations(current_user, id_request, 'DELETED')
    except data_utils.pymssql.Error:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': 'DB error'}), 500

    return jsonify({'state': 'SUCCESS'}), 200


def delete_vacations(current_user, id, status):
    with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
        bulks = database.select_user_calendar_data_bulk(id)

        valores_diccionario = defaultdict(Decimal)

        for clave, valor in bulks:
            valores_diccionario[clave] += valor

        valores_diccionario = dict(valores_diccionario)

        database.add_user_days_on_delete(
            valores_diccionario.get('ExtraHours', Decimal(0)),
            valores_diccionario.get('Holidays', Decimal(0)),
            valores_diccionario.get('LiqTravel', Decimal(0)),
            current_user)

        database.delete_calendar_data_bulk(id)

        database.change_holiday_status(status, id)

        database._conn.commit()


@holiday_blue_print.route('/change-request-status', methods=["POST"])
@token_required
def change_request_status(current_user):
    data = request.get_json()
    id = data.get('id')
    status = data.get('status')
    user_email = data.get('email')
    
    start = data.get('start')
    finish = data.get('finish')

    try:
        if status == 'REJECTED':
            delete_vacations(current_user, id, status)
        else:
            with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
                database.change_holiday_status(status, id)

        #Notify employee
        vacation_status_change_emails([user_email],status,current_user,start,finish)
    except data_utils.pymssql.Error:
        return jsonify({'state': 'error'}), 500
    return jsonify({'state': 'SUCCESS'}), 200

#returns full name by deconstructing the email
def get_user_full_name(email): 
    try:
        name_array = email.split("@")[0].split(".")
        full_name = f"{name_array[0].capitalize()} {name_array[1].capitalize()}"
    except Exception as ex:
        return jsonify({'state': "Error" + str(ex)})
    return full_name

def vacation_status_change_emails(addressees:list, status, action_executor_email, start, finish):
    for addressee in addressees:
        executioner = get_user_full_name(action_executor_email)
        send_email(addressee, f"Holiday {status} [SEBN ES SUITE]", f"Employee: {executioner}</br>Starting Day: {datetime.strptime(start, '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')} <br/>Finishing Day: {datetime.strptime(finish, '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')}")

#TODO: test_get_city_vacation_days_cur_year
@holiday_blue_print.route('/get-city-vacation-days-cur-year', methods=['GET'])
@token_required
def get_city_vacation_days_cur_year(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            vacations = database.select_city_vacation_days_cur_year()
            all_vacations = [{vacation[1]: vacation[2]} for vacation in vacations]
            
            vacations_json = {}
            for vacation in all_vacations:
                vacations_json.update(vacation)
                
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return jsonify(vacations_json), 200