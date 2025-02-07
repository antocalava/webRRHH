from decimal import Decimal
from flask import Blueprint, request, jsonify
from config.config import Config, token_required
from utils.mailing_system import send_email
from datetime import datetime
import utils.database as data_utils

travel_blue_print = Blueprint('travel_blue_print', __name__)

#TODO: reducir codigo --> update y create son MUY SIMILARES, hay que reciclar un poco
@travel_blue_print.route('/request', methods=['POST'])
@token_required
def add_travel_request(current_user):
    data = request.get_json()
    try:
        travel_id = build_new_travel_id() #"003/24"
        email = current_user
        destination:str = data['destination']
        address:str = data['address']
        date_from = datetime.strptime(data['date_from'], '%Y-%m-%d').date()
        date_to = datetime.strptime(data['date_to'], '%Y-%m-%d').date()
        day_amount:int = int(data['day_amount'])
        cost_center:int = int(data['cost_center']) #1 == "SEBN ES"
        added_value:int = int(data['added_value'])  #bool, 0=false, 1=true
        advance_payment:int = int(data['advance_payment']) #bool, 0=false, 1=true
        advance_payment_amount:Decimal = round(Decimal(data['advance_payment_amount']), 3) if data['advance_payment_amount'] != None and Decimal(data['advance_payment_amount']) else None
        reason:str = data['reason']
        transport:str = data['transport']
        extra_documentation = int(data['extra_documentation']) if str(data['extra_documentation']).isdigit() else None #bool, 0=false, 1=true, null if not needed
  
        total_duration = (date_to - date_from).days + 1
        
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database: 
                                 
            if total_duration < 1:
                return jsonify({'state': 'Error: Invalid date range'}), 400
            
            if day_amount < 0:
                return jsonify({'state': 'Error: The trip duration has to at least be one day'}), 400
            
            if day_amount != total_duration:
                return jsonify({'state': 'Error: The trip duration is not equal to the amount of days'}), 400
        
            if advance_payment == 1 and advance_payment_amount <= 0:
                return jsonify({'state': 'Error: Invalid value for advance payment amount'}), 400

            #IF EVERYTHING ALRIGHT, WE DO INSERT
            database.add_travel_request(travel_id, email, destination, address, date_from, date_to, day_amount, cost_center, added_value, advance_payment, advance_payment_amount, reason, transport, extra_documentation)

            #SEND EMALS
            responsible_email = database.get_user_travel_responsible(current_user)[0][0] 
            current_username = get_user_full_name(current_user)
            #to employee
            send_email(current_user, f"{travel_id} - Travel request registered [SEBN ES SUITE]", f"Id: {travel_id}<br/>Subject: {reason}<br/>Destination: {destination}<br/>Starting Day: {date_from}<br/>Finishing Day: {date_to}")
            #to Travelresponsible
            send_sign_petition_email(responsible_email, current_username, travel_id, reason, destination, date_from, date_to)
            
            database._conn.commit() 
            return jsonify({'state': 'SUCCESS'}), 200
    except data_utils.pymssql.Error as error:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error (doing rollback): {error}'}), 500
    except Exception as error:
        return jsonify({'state': f'Error: {error}'}), 500
    
    
#obtener el siguiente id a partir del último
def build_new_travel_id():
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database: 
            prev_id:str = database.get_last_travel_id()[0]
            prev_code:int = int(prev_id.split('/')[0])
            prev_year:int = int(prev_id.split('/')[1])
            
        new_code = prev_code + 1
        new_year = prev_year
        
        #check if we need to change year    
        if not (str(prev_year)).endswith(str(datetime.now().year)[-2:]):
            new_year += 1
            new_code = 0
        
        id:str = str(new_code).zfill(3) + "/" + str(new_year)
        return id 
    except data_utils.pymssql.Error as error:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error (doing rollback): {error}'}), 500

        
def send_sign_petition_email(addresee, user_name, travel_id, reason, destination, date_from, date_to):
    send_email(addresee, f"New travel signing petition [SEBN ES SUITE]",  f"Id: {travel_id}<br/>Employee: {user_name}<br/>Subject: {reason}<br/>Destination: {destination}<br/>Starting Day: {date_from}<br/>Finishing Day: {date_to}") 


def send_status_change_email_hr(employee_email, travel, status_text, status_real):
    hr_email = "" #"SEBN.PHR-Travels-ES-PAM@sebn.com" #TODO: DESCOMENTAR EN PRODUCCION
    employee_name = get_user_full_name(employee_email)
    travel_id = travel['id']
    
    send_email(hr_email, f"{travel_id} - Travel {status_text} [SEBN ES SUITE]", f"<p>{employee_name}'s travel request has been {status_real}.</p>Id: {travel_id}<br/>Subject: {travel['reason']}<br/>Destination: {travel['destination']} <br/>Starting Day: {travel['dateFrom']} <br/>Finishing Day: {travel['dateTo']}")
        
        
#returns full name by deconstructing the email
def get_user_full_name(email): 
    try:
        name_array = email.split("@")[0].split(".")
        full_name = f"{name_array[0].capitalize()} {name_array[1].capitalize()}"
    except Exception as ex:
        return jsonify({'state': "Error" + str(ex)})
    return full_name


#for current user, get all their travels
@travel_blue_print.route('/get-travels', methods=['GET'])
@token_required
def get_travels(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            travels = database.select_travels_by_user(current_user)
            travels_json = [format_travel_details_json(travel) for travel in travels]
    except data_utils.pymssql.Error as err:
        return jsonify({'state': f'DB error: {str(err)}'}), 500
    return jsonify(travels_json), 200


#for other user, get all their travels
@travel_blue_print.route('/get-user-travels', methods=['POST'])
@token_required
def get_travels_for_user(current_user):
    data = request.get_json()
    email = data['user_email']
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            travels = database.select_travels_by_user(email)
            travels_json = [format_travel_details_json(travel) for travel in travels]
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500
    return jsonify(travels_json), 200
 
 
#for other user, find travel by id
@travel_blue_print.route('/get-user-travels-id', methods=['POST'])
@token_required
def get_travel_by_id(current_user):
    data = request.get_json()
    travel_id = data['travel_id']
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            travel = database.select_travel_by_id(travel_id)[0] 
            travels_json = format_travel_details_json(travel)
    except data_utils.pymssql.Error as err:
        return jsonify({'state': f'DB error: {str(err)}'}), 500
    return jsonify(travels_json), 200


#maybe for userinfo excel report(?), function not used for now
""" 
@travel_blue_print.route('/get-all-users-travels', methods=["GET"])
@token_required
def get_all_users_travels(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            employees = get_users_simple_list()[0].json
            employees_json = []
           
            for employee in employees:
                employees_json = [{'FullName': employee["FullName"], 'Email': employee["Email"]} for employee in employees]
        
            for employee in employees_json: 
                email = employee['Email']
                user_travels_raw =  database.select_travels_by_user(email)
                user_travels_result = [format_travel_details_json(travel) for travel in user_travels_raw]
                employee['Travels'] = user_travels_result
                
    except data_utils.pymssql.Error as ex:
        return jsonify({'state': 'DB error: ' + str(ex)}), 500
    return jsonify(employees_json), 200
"""


def format_travel_details_json(travel_raw):
    travel_json:dict = {'id': travel_raw[0], 
                        'userEmail': travel_raw[1], 
                        "dateSubmitted": datetime.strftime(travel_raw[2],'%Y-%m-%d'),
                        "destination": travel_raw[3],
                        "address": travel_raw[4],
                        "dateFrom": datetime.strftime(travel_raw[5],'%Y-%m-%d'),
                        "dateTo": datetime.strftime(travel_raw[6],'%Y-%m-%d'),
                        "dayAmount": travel_raw[7],
                        "costCenter": travel_raw[8],
                        "addedValue": travel_raw[9],
                        "advancePayment": travel_raw[10],
                        "advancePaymentAmount": travel_raw[11],
                        "reason": travel_raw[12],
                        "transport": travel_raw[13],
                        "extraDocumentation": travel_raw[14],
                        "responsibleSignature": travel_raw[15],
                        "managementSignature": travel_raw[16],
                        "status":travel_raw[17]
                       }
    return travel_json
    

#for current user, delete travel request
@travel_blue_print.route('/update-request-status', methods=['PUT'])
@token_required
def update_travel_request_status(current_user):
    data = request.get_json()
    email = data['user_email'] if data['user_email'] != None else current_user
    travel_id = data['travel_id']
    status = data['status']

    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.change_travel_status(status, travel_id)
            travel = format_travel_details_json(database.select_travel_by_id(travel_id)[0])
            
            status_text = "CANCELLED"
            if(status == 'REJECTED'):
                #notify employe
                send_email(email, f"{travel_id} - Travel request denied", f"<p>Your trip request has been REJECTED.</p>Id: {travel_id}<br/>Subject: {travel['reason']}<br/>Destination: {travel['destination']} <br/>Starting Day: {travel['dateFrom']} <br/>Finishing Day: {travel['dateTo']}")
                
                status_text = "DENIED"
                
            #notify hr if rejected or deleted
            send_status_change_email_hr(email, travel, status_text, status)           
    except data_utils.pymssql.Error as err:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error (doing rollback): {str(err)}'}), 500
    return jsonify({'state': 'SUCCESS'}), 200


@travel_blue_print.route('/update-request-docu', methods=['PUT'])
@token_required
def update_travel_request_documentation(current_user):
    data = request.get_json()
    travel_id = data['travel_id']
    extra_docu = int(data['extra_documentation']) if str(data['extra_documentation']).isdigit() else None
    
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.change_travel_documentation(extra_docu, travel_id)
    except data_utils.pymssql.Error as err:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error: {str(err)}'}), 500
    return jsonify({'state': 'SUCCESS'}), 200


@travel_blue_print.route('/sign-request-responsible', methods=['PUT'])
@token_required
def sign_travel_request_responsible(current_user):
    data = request.get_json()
    user_email = data['user_email']
    travel_id = data['travel_id']
    responsible = current_user
    
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.sign_travel_responsible(responsible, travel_id)
            travel = format_travel_details_json(database.select_travel_by_id(travel_id)[0])
        
            management_email = database.get_user_manager(current_user) 
        #Notify of new signing request of travel
        send_sign_petition_email(management_email, get_user_full_name(user_email), travel_id, travel['reason'], travel['destination'], travel['dateFrom'], travel['dateTo']) 
        
        #notify HR of travel creation 
        send_status_change_email_hr(user_email, travel, "REQUESTED", "CREATED")
        
        #notify employee of responsible sign
        send_email(user_email, f"{travel_id} - Travel signed by Responsible [SEBN ES SUITE]", f"<p>Your trip request has been signed by your Travel Responsible</p>Subject: {travel['reason']}<br/> Destination: {travel['destination']} <br/> Starting Day: {travel['dateFrom']} <br/> Finishing Day: {travel['dateTo']}")
            
    except data_utils.pymssql.Error as err:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error (doing rollback): {str(err)}'}), 500
    return jsonify({'state': 'SUCCESS'}), 200


@travel_blue_print.route('/sign-request-management', methods=['PUT'])
@token_required
def sign_travel_request_management(current_user):
    data = request.get_json()
    user_email = data['user_email']
    travel_id = data['travel_id']
    management = current_user
    
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            database.sign_travel_management(management, travel_id)
            travel = format_travel_details_json(database.select_travel_by_id(travel_id)[0])

        #notify employee 
        send_email(user_email, f"{travel_id} - Travel signed by Management [SEBN ES SUITE]", f"<p>Your trip request has been signed by your Manager.</p>Id: {travel_id}<br/>Subject: {travel['reason']}<br/>Destination: {travel['destination']} <br/>Starting Day: {travel['dateFrom']} <br/>Finishing Day: {travel['dateTo']}")
            
        #comprobar cantidad firmas para cambiarlo a SIGNED automaticamente     
        check_signees(travel)
    except data_utils.pymssql.Error as err:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error (doing rollback): {str(err)}'}), 500
    return jsonify({'state': 'SUCCESS'}), 200


""" If both signees have signed the request, we set the status to SIGNED """
def check_signees(travel_json):
    try:
        user_email = travel_json["userEmail"]
        travel_id = travel_json["id"]
        responsible = travel_json['responsibleSignature']
        management = travel_json['managementSignature']
        status = travel_json['status']
        
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:    
            if status == "CREATED":
                if responsible is not None and management is not None:
                    database.change_travel_status('SIGNED', travel_id)    
                    
                    #notify employee of 2/2 signs
                    send_email(user_email, f"{travel_id} - Travel request APPROVED [SEBN ES SUITE]", f"<p>Your trip request has been SIGNED by all parties</p>Id: {travel_id}<br/>Subject: {travel_json['reason']}<br/>Destination: {travel_json['destination']} <br/>Starting Day: {travel_json['dateFrom']} <br/>Finishing Day: {travel_json['dateTo']}")
                    
                    #notify HR of travel approved 
                    send_status_change_email_hr(user_email, travel_json, "APPROVED", "SIGNED")
    except data_utils.pymssql.Error as err:
        return jsonify({'state': f'DB error: {str(err)}'}), 500
    return jsonify({'state': 'SUCCESS'}), 200
    
    
""" Only the users that the manager is in charge of """
@travel_blue_print.route('/get-manager-users-travels', methods=["GET"])
@token_required
def get_management_employees_travels(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            employees = database.get_manager_users_below(current_user)
            employees_json = []
           
            for employee in employees:
                employees_json = [{'FullName': employee["FullName"], 'Email': employee["Email"], 'Department': employee["Department"]} for employee in employees]
        
            for employee in employees_json: 
                email = employee['Email']
                user_travels_raw =  database.select_travels_by_user(email)
                user_travels_result = [format_travel_details_json(travel) for travel in user_travels_raw]
                employee['Travels'] = user_travels_result
                
    except data_utils.pymssql.Error as ex:
        return jsonify({'state': 'DB error: ' + str(ex)}), 500
    return jsonify(employees_json), 200


#TODO: test_get_manager_has_unsigned
@travel_blue_print.route('/get-manager-has-unsigned', methods=["GET"])
@token_required
def get_manager_has_unsigned(current_user):
    try:
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database:
            employees_unsigned = database.get_manager_has_unsigned(current_user)
        return jsonify(employees_unsigned), 200
    except data_utils.pymssql.Error:
        return jsonify({'state': 'DB error'}), 500 
    

@travel_blue_print.route('/update-travel-details', methods=['PUT'])
@token_required
def update_travel_details(current_user):
    data = request.get_json()
    travel_id = data['travel_id']
    user_email = current_user
    destination:str = data['destination']
    address:str = data['address']
    date_from = datetime.strptime(data['date_from'], '%Y-%m-%d').date()
    date_to = datetime.strptime(data['date_to'], '%Y-%m-%d').date()
    day_amount:int = int(data['day_amount'])
    cost_center:int = int(data['cost_center']) #1 == "SEBN ES"
    added_value:int = int(data['added_value'])  #bool, 0=false, 1=true
    advance_payment:int = int(data['advance_payment']) #bool, 0=false, 1=true
    advance_payment_amount:Decimal = round(Decimal(data['advance_payment_amount']), 3) if data['advance_payment_amount'] != None and Decimal(data['advance_payment_amount']) else None
    reason:str = data['reason']
    transport:int = data['transport']
    extra_documentation = int(data['extra_documentation']) if str(data['extra_documentation']).isdigit() else None #bool, 0=false, 1=true, null if not needed
    
    try:
        total_duration = (date_to - date_from).days + 1
        
        if total_duration < 1:
                return jsonify({'state': 'Error: Invalid date range'}), 400
            
        if day_amount < 0:
            return jsonify({'state': 'Error: The trip duration has to at least be one day'}), 400
        
        if day_amount != total_duration:
            return jsonify({'state': 'Error: The trip duration is not equal to the amount of days'}), 400
    
        if advance_payment == 1 and advance_payment_amount <= 0:
            return jsonify({'state': 'Error: Invalid value for advance payment amount'}), 400
        
        with data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME) as database: 
            #IF EVERYTHING ALRIGHT, WE DO update
            database.edit_travel_request_details(travel_id, destination, address, date_from, date_to, day_amount, cost_center, added_value, advance_payment, advance_payment_amount, reason, transport, extra_documentation)
            
            database._conn.commit() 
    except data_utils.pymssql.Error as err:
        data_utils.Database(Config.DATABASE_URI, Config.DATABASE_USER, Config.DATABASE_PASSWORD, Config.DATABASE_NAME)._conn.rollback()
        return jsonify({'state': f'DB error (doing rollback): {str(err)}'}), 500
    except Exception as error:
        return jsonify({'state': f'Error: {error}'}), 500
    return jsonify({'state': 'SUCCESS'}), 200