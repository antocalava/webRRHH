import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import blueprints.user_blue_print 
from blueprints.user_blue_print import *
this_blueprint = blueprints.user_blue_print

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()
    
        
class TestsUserBlueprint(unittest.TestCase):
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
    def test_get_bellow_users_success(self):
        patch_and_reload_app(self, tech_responsible_email)
        response = testsCommon.client.get('/user/get-bellow-employees', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(response.get_json()).get('Employees')
        self.assertIsNotNone(response_first_key)
        
    @measure_execution_time
    def test_get_bellow_users_not_tech_responsible(self):
        patch_and_reload_app(self, manager_email)
        response = testsCommon.client.get('/user/get-bellow-employees', headers={"Authorization": "Bearer some_token"})
        self.assertRaises(UnboundLocalError) #tiene que dar una excepción 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'state': 'Current user is not Tech Responsible'}) 
    
    @measure_execution_time   
    def test_get_user_logs_success(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.get('/user/get-user-logs', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('EntryDate')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time
    def test_update_single_day_success_add_extra_hours(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/user/update-user-single-day', headers={"Authorization": "Bearer some_token",'Content-type':'application/json', 'Accept':'application/json'}, json={"email":user_email, 'type':'ExtraHours', 'quantity':2, 'reason':'TEST'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state': 'SUCCESS'})
            
    @measure_execution_time
    def test_get_user_holidays_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/user/get-user-holidays', headers={"Authorization": "Bearer some_token",'Content-type':'application/json', 'Accept':'application/json'}, json={'email':user_email})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(list(response.get_json())[0]).get('id')
        self.assertIsNotNone(response_first_key)         
        
    @measure_execution_time
    def test_create_user_holidays_excel_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/user/create-user-holidays-excel', headers={'Authorization':"Bearer some_token"})
        self.assertEqual(response.status_code, 200)       
        
    @measure_execution_time
    def test_get_holidays_success(self):
        response = get_holidays(admin_email)
        response_first_key = dict(list(response)[0]).get('id')
        self.assertIsNotNone(response_first_key)
        
    @measure_execution_time    
    def test_get_holidays_holidays_not_found(self):
        response = get_holidays('user.test@sebn.com')
        self.assertEqual(response, [])   
    
    @measure_execution_time
    def test_get_holidays_email_not_found(self):
        response = get_holidays('test.example@sebn.com')
        expected_json = []
        self.assertEqual(response, expected_json)        
           
    @measure_execution_time    
    def test_get_department_users_success_user(self):
        patch_and_reload_app(self, user_email)
        response = testsCommon.client.get('/user/get-department-partners', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(response.get_json()[0]).get('FullName')
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time
    def test_get_department_users_success_admin(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/user/get-department-partners', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(response.get_json()[0]).get('FullName') 
        self.assertIsNotNone(response_first_key)
    
    @measure_execution_time
    def test_get_user_details_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.post('/user/get-user-details', headers={"Authorization": "Bearer some_token"}, json={'email':user_email})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])
        response_first_key = dict(response.get_json()).get('FullName') 
        self.assertIsNotNone(response_first_key)  
        
    @measure_execution_time
    def test_update_user_details_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.put('/user/update-user-details', headers={"Authorization": "Bearer some_token"}, json={"fullName":"FAKE TEST", "email": "usuario.test4@sebn.com", "city":"PAM", "department":"SCM", "subDepartment":"SCA", "costCenter":7777, "position":"Internship", "techResponsible":"cristina.lopez@sebn.com", "travelResponsible":"antonio.calahorra@sebn.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state':'SUCCESS'})

    @measure_execution_time
    def test_get_user_cost_center_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.get('/user/get-user-cost-center', headers={"Authorization": "Bearer some_token"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), [])

    @measure_execution_time
    def test_delete_user_success(self):
        patch_and_reload_app(self, admin_email)
        response = testsCommon.client.put('/user/delete-user', headers={"Authorization": "Bearer some_token"}, json={"email": "user.test8@sebn.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'state':'SUCCESS'})



if __name__ == '__main__':
    unittest.main()
