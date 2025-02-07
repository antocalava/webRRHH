import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.home_page_blue_print
from blueprints.home_page_blue_print import *
this_blueprint = blueprints.home_page_blue_print

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()

class TestsHomePageBlueprint(unittest.TestCase):
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
    def test_get_user_full_name_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.get('/home/get-user-full-name', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertIsNotNone(response.get_json())
        
    @measure_execution_time
    def test_get_calendars_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/home/get-calendars-info', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'})        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertIsNotNone(response.get_json())
        
    @measure_execution_time
    def test_get_graph_travels_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/home/get-graph-travels', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'})        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertIsNotNone(response.get_json())
        
    @measure_execution_time    
    def test_get_graph_home_office_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/home/get-graph-home-office', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertIsNotNone(response.get_json())
        
    @measure_execution_time    
    def test_get_graph_vacations_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/home/get-graph-vacations', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'})        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertIsNotNone(response.get_json())
        
    @measure_execution_time    
    def test_get_user_travels_success(self):
        response = get_user_travels(admin_email)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].status_code, 200)
        self.assertNotEqual(response[0].json, [])
        self.assertIsNotNone(response[0].json)
        
    @measure_execution_time    
    def test_get_user_vacations_success(self):
        response = get_user_holidays(admin_email)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].status_code, 200)
        self.assertNotEqual(response[0].json, [])
        self.assertIsNotNone(response[0].json)
    
    @measure_execution_time    
    def test_get_user_festivities_success(self):
        response = get_user_festivities(admin_email)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].status_code, 200)
        self.assertNotEqual(response[0].json, [])
        self.assertIsNotNone(response[0].json)

    @measure_execution_time    
    def test_get_user_home_office_success(self):
        response = get_user_home_office(admin_email)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].status_code, 200)
        self.assertNotEqual(response[0].json, [])
        self.assertIsNotNone(response[0].json)
        
  
if __name__ == '__main__':
    unittest.main()
