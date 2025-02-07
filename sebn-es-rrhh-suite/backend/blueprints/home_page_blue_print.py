from flask import Blueprint, jsonify, request
from config.config import Config, token_required
import utils.database as data_utils
from datetime import datetime, timedelta
from decimal import Decimal

home_page_blue_print = Blueprint('home_page_blue_print', __name__)

#to use in the title
@home_page_blue_print.route('/get-user-full-name', methods=["GET"])
@token_required
def get_user_full_name(current_user):
    try:
        name_array = current_user.split("@")[0].split(".")
        full_name = f"{name_array[0].capitalize()} {name_array[1].capitalize()}"
        return jsonify(full_name), 200
    except Exception as ex:
        return jsonify({'state': str(ex)}), 500
    
""" Builds the final json that has dates as keys and the value are 
    all the events on said date are stored inside of a list
"""
@home_page_blue_print.route('/get-calendars-info', methods=["POST"])
@token_required
def get_calendars_info(current_user):
    try:
        #todos los dias registrados del usuario y sus respectivos eventos
        calendars_all_data:dict = {} 
        
        home_office:dict = get_user_home_office(current_user)[0].json
        vacations:dict = get_user_holidays(current_user)[0].json
        festivities:dict = get_user_festivities(current_user)[0].json
        travels:dict = get_user_travels(current_user)[0].json
        
        event_types:list = [home_office, festivities, vacations, travels] 
        for type in event_types:   
            for key in type.keys():
                if key in calendars_all_data.keys():
                    calendars_all_data[key].append(type[key]) # añadimos el valor del evento a la lista del día en el que hay mas de un evento
                else:
                    calendars_all_data.update({f"{key}":[type[key]]})
                    
        return jsonify(calendars_all_data), 200
    except Exception as ex:
        return jsonify({'state': f"Error: {str(ex)}"}), 500
    
def get_user_home_office(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_home_office = database.get_home_office(current_user)
            filter_home_office = [{'Date': data[1].strftime('%Y-%m-%d'), 'Type': data[2]} for data in data_home_office]
            
            json_home_office:dict = filtered_data_to_formatted_json(filter_home_office)
            return jsonify(json_home_office), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500

def get_user_holidays(current_user):
    #TODO: optimize this by using generic query and calculating the days in date range with decompose_date_range() function
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_holidays = database.select_user_holidays_dates_bucket_status(current_user)
            print(data_holidays)
            filter_holidays = [{'Date': data[0].strftime('%Y-%m-%d'), 'Type': 'HOLIDAYS', 'Info': str(data[1]).upper()} for data in data_holidays]  
            
            holidays_json:dict = filtered_data_to_formatted_json(filter_holidays)
            return jsonify(holidays_json), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500


def get_user_travels(current_user):  
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_travels = database.select_travels_by_user(current_user)
            query_travels = [{'DateFrom': data[5].strftime('%Y-%m-%d'), 'DateTo': data[6].strftime('%Y-%m-%d'), 'Type': 'TRAVEL', 'Info': [data[3], data[17]]} for data in data_travels]  
         
            filter_travels:list = []
            for travel in query_travels:
                if travel['DateFrom'] != travel['DateTo']:
                    start = datetime.strptime(travel['DateFrom'], '%Y-%m-%d')
                    end =  datetime.strptime(travel['DateTo'], '%Y-%m-%d')
                    days = decompose_date_range(start, end)
                    
                    filtered=[{'Date': day.strftime('%Y-%m-%d'), 'Type': travel['Type'], 'Info': travel['Info']} for day in days]
                    filter_travels.extend(filtered) #append all days of one travel into all the travel days
                else:
                    filtered={'Date': travel['DateFrom'], 'Type': travel['Type'], 'Info': travel['Info']}
                    filter_travels.append(filtered)
            
            json_travels:dict = filtered_data_to_formatted_json(filter_travels)
            return jsonify(json_travels), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500 
    

def get_user_festivities(current_user): 
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_festivities = database.select_festivity_by_user(current_user)
            filter_festivities = [{'Date': data[2].strftime('%Y-%m-%d'), 'Type': "FESTIVITY"} for data in data_festivities]
            
            json_festivities:dict = filtered_data_to_formatted_json(filter_festivities)
            return jsonify(json_festivities), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500

def get_user_vacation_days_remaining(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_remaining = database.get_user_days(current_user)
            remaining = data_remaining[1] + data_remaining[2] + data_remaining[3] #we add all the buckets
            
            filter_remaining = {'Remaining': remaining}

            return jsonify(filter_remaining), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    
def get_user_vacation_days_used(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_used = database.select_user_holidays_used_cur_year(current_user)
            filter_used = [{"Quantity": data[7], "PartialDay": data[5]} for data in data_used]

            return jsonify(filter_used), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    
 
""" Obtains all individual dates within a date range """
def decompose_date_range(start:datetime, end:datetime):
    all_dates = []
    current_date = start
    while current_date <= end:
        all_dates.append(current_date)
        current_date += timedelta(days=1)
    return all_dates

""" 
Cambiamos el formato de los datos recogidos de la BD 
para sacar un JSON del formato deseado, de modo que las 
claves siempre son las fechas y los valores los tipos 
de evento posibles para el calendario.

Ejemplo de formato de salida: { '2024-04-06': [ ["OFFICE",null], ["HOLIDAYS","SIGNED"] ], ...another date... }
"""
def filtered_data_to_formatted_json(filtered_data):
    json:dict = {}
    for i in range(len(filtered_data)):
        date = filtered_data[i]['Date']
        type = filtered_data[i]['Type']
        info = filtered_data[i].get('Info',None)

        json.update({f"{date}":[f"{type}"]})
        if (info != 'None'): json[date].append(info)
    return json

""" Home office data for the user relative to the currrent month"""
@home_page_blue_print.route('/get-graph-home-office', methods=["POST"])
@token_required
def get_graph_home_office(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            data_days_worked_raw = database.get_home_office_cur_month(current_user)
            data_days_worked = [{'Date': data[1].strftime('%Y-%m-%d'), 'Type': data[2]} for data in data_days_worked_raw]
        filtered = filtered_data_to_formatted_json(data_days_worked)
        
        days_full = 0
        days_partial = 0
        days_office = 0
        for type in filtered.values():
            match type[0]:
                case 'OFFICE':
                    days_office += 1
                case 'FULL':
                    days_full += 1
                case 'PARTIAL':
                    days_partial += 1
            
        json_days_worked:dict = {'OFFICE':days_office, 'PARTIAL':days_partial, 'FULL':days_full}
        
        return jsonify(json_days_worked), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500

""" Holidays data for the user relative to the currrent year"""
@home_page_blue_print.route('/get-graph-vacations', methods=["POST"])
@token_required
def get_graph_vacations(current_user):
    try:
        #compare days you have available with the ones u have already used
        data_holidays_left:dict = get_user_vacation_days_remaining(current_user)[0].json
        data_holidays_used = get_user_vacation_days_used(current_user)[0].json
        
        decimal_holidays_used:Decimal = 0
        for each in data_holidays_used:
            decimal_holidays_used += Decimal(each['Quantity'])
            
        json_holidays:dict = {'Used': str(decimal_holidays_used)}
        json_holidays.update(data_holidays_left)
        
        return jsonify(json_holidays), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
