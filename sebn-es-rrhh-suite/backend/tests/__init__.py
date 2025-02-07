import sys
import os
import time
from unittest.mock import patch
from importlib import reload

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app

user_email = 'cristina.lopez@sebn.com' #normal employee
admin_email = 'antonio.calahorra@sebn.com' 
tech_responsible_email = 'cristina.lopez@sebn.com' 
travel_responsible_email = 'cristina.lopez@sebn.com' 
manager_email = 'testing.manager@sebn.com' 
aux_email:str = ''


def mock_token_user(f):
    def wrapper(*args, **kwargs):
        current_user = user_email
        return f(current_user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def mock_token_admin(f):
    def wrapper(*args, **kwargs):
        current_user = admin_email
        return f(current_user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def mock_token_aux(f):
    def wrapper(*args, **kwargs):
        current_user = aux_email
        return f(current_user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


""" 
    Delete logger file each time all tests are executed 
    & create empty one to write the logger in it 
"""
# os.remove("./tests/logs_exec_time_tests.log") 
# open("./tests/logs_exec_time_tests.log", "w")

""" 
    Decorator timer for each test to measure the function's 
    execution time, we add each measurement to a logger file
 
    NOTE: error or failed tests will not be added to the logger
"""
def measure_execution_time(f): #TODO: fix so that importing this doesnt explode if the logger file doesnt exist pls
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func = f(*args, **kwargs)
        total_time = time.time() - start_time
        info_msg = f"{f.__qualname__}: --- {total_time} seconds ---\n"
        
        """ logger = open("./tests/logs_exec_time_tests.log", "a")
        logger.write(info_msg)
        logger.close()  """
        
        print(info_msg)
        return func
    return wrapper


class TestsCommon:
    """ Create Flask app """
    def setup_app(self):
        self.app = app.create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        
        self.ctx = self.app.app_context()
        self.ctx.push()
        return self.app, self.client, self.ctx
    
    """ Initialize patch to mock employee access token (user) """
    def setup_patch_user(self):
        self.patcher_token_required = patch('config.config.token_required', mock_token_user)
        self.mock_token_required = self.patcher_token_required.start()

    """ Initialize patch to mock manager access token (admin) """
    def setup_patch_admin(self):
        self.patcher_token_required = patch('config.config.token_required', mock_token_admin)
        self.mock_token_required = self.patcher_token_required.start()

    def setup_patch_aux_user(self, email):
        global aux_email
        aux_email = email
        self.patcher_token_required = patch('config.config.token_required', mock_token_aux)
        self.mock_token_required = self.patcher_token_required.start()
    
    """ Clean up after each test """    
    def tearDown(self):
        self.ctx.pop()
        patch.stopall()
    
    """ Clean patches after all tests """    
    def _cleanup(self):
        self.patcher_token_required.stop()

    def patch_user_and_reload_blueprint(self, blueprint):
        self.setup_patch_user()
        reload(blueprint)

    def patch_admin_and_reload_blueprint(self, blueprint):
        self.setup_patch_admin()
        reload(blueprint)
    
    def patch_aux_user_and_reload_blueprint(self, blueprint, email):
        self.setup_patch_aux_user(email)
        reload(blueprint)