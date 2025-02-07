import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.holiday_blue_print
from blueprints.holiday_blue_print import *
this_blueprint = blueprints.holiday_blue_print

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()

class TestsHolidayBlueprint(unittest.TestCase):
    """ Set up Flask app """
    def setUp(self):
        self.app, self.client, self.ctx = testsCommon.setup_app()
    
    """ Clean up after each test """    
    def tearDown(self):
        self.ctx.pop()
        patch.stopall()
    
    """ Clean patches after all tests """    
    def _cleanup(self):
        testsCommon.patcher_token_required.stop()
    
    @measure_execution_time     
    def test_create_request_success_full_day(self): 
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"12/08/2024", 'finishingDay':"13/08/2024", "reason":"test_create_request_success", "partialDay":False,"hours":0, "minutes":0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{'state': 'SUCCESS'})
        
    @measure_execution_time     
    def test_create_request_success_partial_day(self): 
        patch_and_reload_app(self, admin_email)
        hours:Decimal = 2*0.125
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"07/08/2024", 'finishingDay':"09/08/2024", "reason":"test_create_request_success_partial_day", "partialDay":True,"hours":hours})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{'state': 'SUCCESS'})
        
    @measure_execution_time     
    def test_create_request_partial_invalid_date_range(self): 
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"20/08/2024", 'finishingDay':"02/08/2024", "reason":"test_create_request_partial_invalid_date_range", "partialDay":True,"hours":0, "minutes":0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': 'Error: Partial day quantity can not be zero'})
    
    #TODO: descomentar cuando se compruebe en el back si las fechas seleccionadas caen en festivo
    """ 
    @measure_execution_time    
    def test_create_request_regional_festivity_check(self): #no se puede el 25 de julio bc es festivo en Navarra (y usuario es de pamplona)
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"25/07/2024", 'finishingDay':"25/07/2024","reason":"test_create_request_regional_holiday_check","partialDay":False,"hours":0,"minutes":0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': 'You can not choose a non-working day as a vacation day'})
    
    @measure_execution_time
    def test_create_request_national_festivity_check(self): #no se puede el 1 de enero bc es festivo en España
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"01/01/2024", 'finishingDay':"01/01/2024","reason":"test_create_request_national_holiday_check","partialDay":False,"hours":0,"minutes":0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': 'You cannot choose a non-working day as a vacation day'}) 
    """
    
    @measure_execution_time    
    def test_create_request_total_grater_than_user_days(self): #no se pueden pedir 200 días de fiesta
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"14/12/2023", 'finishingDay':"01/07/2025","reason":"test_create_request_total_grater_than_user_days","partialDay":False,"hours":0,"minutes":0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': 'You have marked more days than you have been given'}) 
    
    @measure_execution_time    
    def test_create_request_duplicate_request(self): #ya hay una request hecha para esas fechas (o que las incluya en el rango)
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'startingDay':"22/07/2024", 'finishingDay':"24/07/2024","reason":"test_create_request_duplicate_request","partialDay":False,"hours":0,"minutes":0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': 'One of the range of days has already been requested'})
    
    @measure_execution_time    
    def test_get_user_holidays_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/holiday/get-user-holidays', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('finishingDay')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time    
    def test_delete_user_holidays_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.delete('/holiday/delete-user-holidays', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'id':1086})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
    
    @measure_execution_time
    def test_delete_user_holidays_email_not_belong_to_id(self): #id no corresponde con email
        this_blueprint.delete_vacations('test.test@sebn.com', 1166, 'DELETED')
        self.assertRaises(data_utils.pymssql.Error)
    
    @measure_execution_time    
    def test_change_request_status_success_approved(self): #esto lo hace el tech responsible!!
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/change-request-status', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'id':414, 'status':"SIGNED", "email":admin_email, "name":"test_change_employees_status_approved_success", "start":"Fri, 26 Jul 2024 00:00:00 GMT", "finish":"Wed, 31 Jul 2024 00:00:00 GMT"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{'state': 'SUCCESS'})
    
    @measure_execution_time    
    def test_change_request_status_success_rejected(self): #cambiar a REJECTED y eliminar
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/holiday/change-request-status', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'id':414, 'status':"REJECTED", "email":admin_email, "name":"test_change_employees_status_rejected_success", "start":"Fri, 26 Jul 2024 00:00:00 GMT", "finish":"Wed, 31 Jul 2024 00:00:00 GMT"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{'state': 'SUCCESS'})
  
    @measure_execution_time    
    def test_get_city_vacation_days_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/holiday/get-city-vacation-days', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(response.get_json()).get('PAM')
        self.assertIsNotNone(response_first_key)  
  
if __name__ == '__main__':
    unittest.main()
