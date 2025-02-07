import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.festivity_blue_print
from blueprints.festivity_blue_print import *
this_blueprint = blueprints.festivity_blue_print

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()

class TestsFestivityBlueprint(unittest.TestCase):
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
    def test_create_holiday_success(self): #anadimos fiesta en Pamplona y Cuenca el 26 de julio del 2024
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/festivity/create-festivity', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'}, json={'cities': ["PAM", "CUE"], "date":"2024-07-30"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{'state': 'SUCCESS'})
        
    @measure_execution_time     
    def test_create_holiday_duplicate_date(self): #ya es fiesta en Pamplona el 25 de julio del 2024
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/festivity/create-festivity', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={'cities': ["PAM"], "date":"2024-07-25"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': 'A festivity already exists for PAM on that date'})
        
    @measure_execution_time 
    def test_get_festivities_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/festivity/get-all-festivities', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        response_first_key = dict(list(response.get_json())[0]).get('Date')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time     
    def test_delete_festivity_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.delete('/festivity/delete-festivity', headers={"Authorization":"Bearer some_token", 'Content-type':'application/json'}, json={"id":189})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{'state': 'SUCCESSFUL'})
    
    @measure_execution_time     
    def test_delete_festivity_id_not_exist(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.delete('/festivity/delete-festivity', headers={"Authorization":"Bearer some_token", 'Content-type':'application/json'}, json={"id":-1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),{'state': "Festivity could not be deleted since that ID does not exist"})
    
    @measure_execution_time     
    def test_get_user_festivities_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/festivity/get-user-festivities', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('Date')
        self.assertIsNotNone(response_first_key)
    
    
  
if __name__ == '__main__':
    unittest.main()
