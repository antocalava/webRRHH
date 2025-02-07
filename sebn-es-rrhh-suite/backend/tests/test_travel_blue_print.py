import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.travel_blue_print
from blueprints.travel_blue_print import *
this_blueprint = blueprints.travel_blue_print

#TODO: this one still doesnt work well :c 
def patch_and_update_blueprint(app, email): #patch_and_update_blueprint(self.app, user_email) 
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    Parent.app.update_blueprint(app, "travel_blue_print", '/travel', this_blueprint)

def patch_and_reload_app(self, email): 
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()
    
class TestsTravelBlueprint(unittest.TestCase):
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
    def test_create_travel_request_success(self):    
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.post('/travel/request', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"destination": "Germany", "address": "Berlin street", "date_from": "2024-08-21",  "date_to": "2024-08-23",  "day_amount": 3,"cost_center": 1, "added_value": 1, "advance_payment": 0, "advance_payment_amount": None, "reason": "Have a fun meeting", "transport": [1,1,1,1,1,1], "extra_documentation": None})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
    @measure_execution_time
    def test_get_travels_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.get('/travel/get-travels', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('destination')
        self.assertIsNotNone(response_first_key)    
        
    @measure_execution_time
    def test_get_user_travels_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.post('/travel/get-user-travels', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"user_email":user_email})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('destination')
        self.assertIsNotNone(response_first_key)    
        
    @measure_execution_time
    def test_get_user_travels_id_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.post('/travel/get-user-travels-id', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"user_email":user_email, "travel_id":3})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(response.get_json()).get('destination')
        self.assertIsNotNone(response_first_key)    
           
    @measure_execution_time
    def test_get_manager_users_travels_success(self):
        patch_and_reload_app(self, manager_email)
        response = testsCommon.client.get('/travel/get-manager-users-travels', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(dict(list(response.get_json())[0]).get('Travels'))[0]).get('destination')
        self.assertIsNotNone(response_first_key)       
        
    @measure_execution_time
    def test_update_request_status_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.put('/travel/update-request-status', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"user_email":user_email, "travel_id":18,"status":"DELETED"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
    @measure_execution_time
    def test_update_request_docu_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.put('/travel/update-request-docu', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"user_email":user_email, "travel_id":18,"extra_documentation":0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
    @measure_execution_time
    def test_sign_request_responsible_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.put('/travel/sign-request-responsible', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"user_email":user_email, "travel_id":18})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
    @measure_execution_time
    def test_sign_request_management_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.put('/travel/sign-request-management', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"user_email":user_email, "travel_id":18})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
    @measure_execution_time
    def test_get_plants_europe_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.get('/travel/get-sebn-plants', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        
    @measure_execution_time
    def test_update_travel_details_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.put('/travel/update-travel-details', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"travel_id":18, "destination": "Spain", "address": "Edited street", "date_from": "2024-08-21",  "date_to": "2024-08-23",  "day_amount": 3, "cost_center": 9999, "added_value": 1, "advance_payment": 0, "advance_payment_amount": None, "reason": "test_update_travel_details_success", "transport": 31, "extra_documentation": None})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
if __name__ == '__main__':
    unittest.main()
