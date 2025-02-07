import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.access_blue_print
from blueprints.access_blue_print import *
this_blueprint = blueprints.access_blue_print

from utils.encryption import *
from config.config import Config

#necesario para testear si usuarios nuevos funcionan bien
def get_token_authorization(email):
    with testsCommon.ctx:
        SECRET_KEY = Config.SECRET_KEY
        token = jwt.encode({'username': email }, SECRET_KEY, algorithm='HS256')
    return token

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()

class TestsAccessBlueprint(unittest.TestCase):
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
    def test_login_success(self):
        email = "testing.manager@sebn.com"
        password = "testing123"
        token = get_token_authorization(email)   
        response = testsCommon.client.post('/access/login', headers={'Content-type':'application/json'}, json={'email':email, "password":password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'authorization': f'{token}'})
    
    @measure_execution_time    
    def test_login_invalid_email(self):
        response = testsCommon.client.post('/access/login', headers={'Content-type':'application/json'}, json={'email': "prueba.prueba@sebn.com", "password":"ggg123"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {'message': 'User not found', 'status': 'USER_NOT_FOUND'}) 
    
    @measure_execution_time     
    def test_login_invalid_password(self):
        email = "testing.manager@sebn.com"
        response = testsCommon.client.post('/access/login', headers={'Content-type':'application/json'}, json={'email':email, "password": "otraCONTRA123"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {'message': 'Incorrect password', 'status': 'INCORRECT_PASSWORD'})
        
    @measure_execution_time     
    def test_is_valid_password_success_mixed_chars(self):
        password = "Contra123"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time     
    def test_is_valid_password_success_all_lower_case(self):
        password = "osssds"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time 
    def test_is_valid_password_success_all_upper_case(self):
        password = "DFVHGT"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time     
    def test_is_valid_password_success_all_numbers(self):
        password = "123456"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time     
    def test_is_valid_password_success_no_upper_case(self):
        password = "contra123"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time 
    def test_is_valid_password_success_no_lower_case(self):
        password = "CONTRA123"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time     
    def test_is_valid_password_success_no_numbers(self):
        password = "ConTra"
        response = this_blueprint.is_valid_password(password)
        self.assertTrue(response)
    
    @measure_execution_time     
    def test_is_valid_password_special_character(self):
        password = "Contra123#"
        response = this_blueprint.is_valid_password(password)
        self.assertFalse(response)
    
    @measure_execution_time     
    def test_is_valid_password_less_than_six_chars(self):
        password = "o2Cd3"
        response = this_blueprint.is_valid_password(password)
        self.assertFalse(response)
    
    @measure_execution_time     
    def test_change_password_success(self):
        email = "testing.manager@sebn.com"
        newPassword = "newtesting123"
        patch_and_reload_app(self, email)
        response = testsCommon.client.post('/access/change-password', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"newPassword": newPassword})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})    
        
    @measure_execution_time 
    def test_change_password_invalid_password(self):
        email = "testing.manager@sebn.com"
        newPassword = "newPASS123###"
        patch_and_reload_app(self, email)
        response = testsCommon.client.post('/access/change-password', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"newPassword": newPassword})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {'state': 'Invalid password'})  
  
    @measure_execution_time 
    def test_change_password_same_password(self):
        email = "testing.manager@sebn.com"
        newPassword = "testing123"
        patch_and_reload_app(self, email)
        response = testsCommon.client.post('/access/change-password', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"newPassword": newPassword})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'}) 
        
    @measure_execution_time     
    def test_get_rank_success_employee(self):
        patch_and_reload_app(self,user_email)
        response = testsCommon.client.get('/access/get-rank', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        response_first_key = dict(response.get_json()).get('rank')
        self.assertIsNotNone(response_first_key)
        self.assertNotEqual(response.get_json(), {'rank': None})
        has_employee_rank = list(response_first_key).count('ac2de5774e07ee521327aff50b5a00b41b3c3d2dc8ddfa833db2ebd5a30eaff3') > 0
        self.assertNotEqual(False, has_employee_rank)
    
    @measure_execution_time     
    def test_get_rank_success_tech_responsible(self):
        patch_and_reload_app(self,tech_responsible_email)
        response = testsCommon.client.get('/access/get-rank', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        response_first_key = dict(response.get_json()).get('rank')
        self.assertIsNotNone(response_first_key)
        self.assertNotEqual(response.get_json(), {'rank': None})
        has_responsible_rank = list(response_first_key).count('e7698668c7a6762266de376ce96adbea6e2cc5cd203bad0adb4e1832480b784b') > 0
        self.assertNotEqual(False, has_responsible_rank)
    
    @measure_execution_time     
    def test_get_rank_success_travel_responsible(self):
        patch_and_reload_app(self,travel_responsible_email)
        response = testsCommon.client.get('/access/get-rank', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        response_first_key = dict(response.get_json()).get('rank')
        self.assertIsNotNone(response_first_key)
        self.assertNotEqual(response.get_json(), {'rank': None})
        has_responsible_rank = list(response_first_key).count('e7698668c7a6762266de376ce96adbea6e2cc5cd203bad0adb4e1832480b784b') > 0
        self.assertNotEqual(False, has_responsible_rank)
        
    @measure_execution_time     
    def test_get_rank_success_manager(self):
        patch_and_reload_app(self, manager_email)
        response = testsCommon.client.get('/access/get-rank', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        response_first_key = dict(response.get_json()).get('rank')
        self.assertIsNotNone(response_first_key)
        self.assertNotEqual(response.get_json(), {'rank': None})
        has_manager_rank = list(response_first_key).count('38ovzt6htlz9dvkfpb6gdidjlt2zkxsue4q39wfehxlp7ykhjrp75hmk954spu0n') > 0
        self.assertNotEqual(False, has_manager_rank)
        
    @measure_execution_time     
    def test_get_rank_success_admin(self): #TODO: also do a test for HR email to see if they get admin rank as well
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/access/get-rank', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        response_first_key = dict(response.get_json()).get('rank')
        self.assertIsNotNone(response_first_key)
        self.assertNotEqual(response.get_json(), {'rank': None})
        has_admin_rank = list(response_first_key).count('cb88dfe7c01e300d2be5b0368f2e50895dd181601a7d31e61bfd7e597f7ef127') > 0
        self.assertNotEqual(False, has_admin_rank)
        
    @measure_execution_time     
    def test_reset_user_password_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.put('/access/reset-user-password', headers={"Authorization": "Bearer some_token"}, json={'userEmail':user_email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        
        
if __name__ == '__main__':
    unittest.main()
