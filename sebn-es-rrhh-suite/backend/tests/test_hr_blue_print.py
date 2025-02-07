import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.hr_blue_print
from blueprints.hr_blue_print import *
this_blueprint = blueprints.hr_blue_print

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()

class TestsHrBlueprint(unittest.TestCase):
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
    def test_get_hr_logs_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/hr/get-hr-logs', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('id')
        self.assertIsNotNone(response_first_key)
        
    @measure_execution_time    
    def test_get_departments_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/hr/get-departments', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('name')
        self.assertIsNotNone(response_first_key)
        
    @measure_execution_time    
    def test_get_sub_departments_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/hr/get-sub-departments', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('SubDepartment')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time
    def test_get_buckets_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/hr/get-buckets', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('bucket')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time    
    def test_create_user_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/create-user', headers={"Authorization": "Bearer some_token",'Content-type':'application/json', 'Accept':'application/json'}, json={"fullname":"FakeUser MustDelete", "email": "user.test8@sebn.com", "department":"SCM", "subDepartment": None, "costCenter": None, "position":"Employee", "techResponsible":tech_responsible_email, "travelResponsible":travel_responsible_email, "city":'PAM', "gerency":"Testing", "startDate":"2024-09-05"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
    
    @measure_execution_time
    def test_create_user_missing_fields(self): #travelResponsible missing
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/create-user', headers={"Authorization": "Bearer some_token",'Content-type':'application/json', 'Accept':'application/json'}, json={"fullname":"Nombre Apellido", "email": "nombre.apellido@sebn.com", "department":"SCM", "subDepartment": None, "costCenter": None, "position":"Employee", "techResponsible":tech_responsible_email, "city":"PAM","gerency":"Testing", "startDate":"2024-09-05"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'state': 'All fields are required'})  
    
    @measure_execution_time    
    def test_create_user_missing_last_name(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/create-user', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json', 'Accept':'application/json'}, json={"fullname":"Nombre", "email": "nombre.apellido@sebn.com", "department":"SCM", "subDepartment": None, "costCenter": None, "position":"Employee", "techResponsible":"joseantonio.pascual@sebn.com", "travelResponsible":"joseantonio.pascual@sebn.com", "city":"PAM", "gerency":"Testing", "startDate":"2024-09-05"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'state': 'The full name must contain at least one first and one last name'})
    
    @measure_execution_time
    def test_create_user_missing_last_name_with_space(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/create-user', headers={"Authorization": "Bearer some_token",'Content-type':'application/json', 'Accept':'application/json'}, json={"fullname":"Nombre ", "email": "nombre.apellido@sebn.com", "department":"SCM", "subDepartment": None, "costCenter": None, "position":"Employee", "techResponsible":'joseantonio.pascual@sebn.com',  "travelResponsible":"joseantonio.pascual@sebn.com", "city":"PAM", "gerency":"Abigail", "startDate":"15/07/2024"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'state': 'The full name must contain at least a first and a last name'}) 
    
    @measure_execution_time    
    def test_user_days_calculation_success(self): #THIS ONE CAN FAIL IF THE CITY VACATIONS VALUE CHANGES! right now, PAM is 39.13
        response = this_blueprint.user_days_calculation("PAM", datetime(2024,7,15))
        self.assertGreater(response, 18)
        self.assertLess(response, 19)
        self.assertEqual(response, 18.11772602739726068)
    
    @measure_execution_time    
    def test_string_generator_success(self):
        response = string_generator()
        self.assertNotEqual(response, "")
        
    @measure_execution_time
    def test_edit_user_days_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.put('/hr/edit-user-days', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"Email":user_email, "UserDays":[{"ExtraHours":1, "Holidays":7, "LiqTravel":2}]})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
    
    @measure_execution_time    
    def test_get_home_office_report_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/get-reporting-home-office', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"starting_date":"2024-06-01", "finishing_date":"2024-07-01"})
        self.assertEqual(response.status_code, 200)
    
    @measure_execution_time    
    def test_get_home_office_report_invalid_date_range(self): #start date is AFTER finishing date
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/get-reporting-home-office', headers={"Authorization": "Bearer some_token", 'Content-type':'application/json'}, json={"starting_date":"2024-08-01", "finishing_date":"2024-07-01"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'state': 'Invalid date range'})
    
    @measure_execution_time    
    def test_get_head_count_cue_report_success(self): 
        #TODO: test_get_head_count_cue_report_success
        pass
    
    @measure_execution_time
    def test_get_all_users_simple_list_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/hr/get-all-users-simple-list', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('FullName')
        self.assertIsNotNone(response_first_key)
        
    @measure_execution_time
    def test_get_user_days_buckets_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/hr/get-user-days-buckets', headers={"Authorization": "Bearer some_token"}, json={"email":user_email})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('BucketName')
        self.assertIsNotNone(response_first_key)
        
if __name__ == '__main__':
    unittest.main()
