import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.home_office_blue_print
from blueprints.home_office_blue_print import *
this_blueprint = blueprints.home_office_blue_print

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()
    
class TestsHomeOfficeBlueprint(unittest.TestCase):
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
    def test_get_user_home_office_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/home-office/get-user-home-office', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"email":admin_email})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('Date')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time   
    def test_get_department_home_office_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.get('/home-office/get-department-home-office', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('Date')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time
    def test_delete_home_office_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.delete('/home-office/delete-home-office', headers={"Authorization": "Bearer some_token", 'Content-Type': 'application/json'}, json={'day':'04/07/2024'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])   
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})

    @measure_execution_time
    def test_get_home_office_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/home-office/get-home-office', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])   
        response_first_key = dict(list(response.get_json())[0]).get('Date')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time    
    def test_add_home_office_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.post('/home-office/add-home-office', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'day':"23/07/2024", "type":"PARTIAL"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
        

  
if __name__ == '__main__':
    unittest.main()
