import unittest
from unittest.mock import patch
from importlib import reload
import __init__ as Parent
from __init__ import measure_execution_time
from __init__ import user_email, admin_email, manager_email, travel_responsible_email, tech_responsible_email
testsCommon = Parent.TestsCommon()

import utils.mailing_system as mailing_sys
from utils.mailing_system import *

def patch_and_reload_app(self, email):
    testsCommon.patch_aux_user_and_reload_blueprint(this_blueprint, email)
    reload(Parent.app)
    self.app, self.client, self.ctx = testsCommon.setup_app()
    
class TestsUtilsMailingSystem(unittest.TestCase):
    """ Set up Flask app """
    def setUp(self):
        self.app, self.client, self.ctx = testsCommon.setup_app()
        self.patcher_token_required = patch('config.config.token_required')
        self.addCleanup(self._cleanup)
    
    """ Clean up after each test """    
    def tearDown(self):
        self.ctx.pop()
        patch.stopall()
    
    """ Clean patches after all tests """    
    def _cleanup(self):
        self.patcher_token_required.stop()
    
    @measure_execution_time    
    def test_send_email_success(self):
        addressee = user_email
        subject = "prueba mailing system"
        message = "This is a test"
        response = mailing_sys.send_email(addressee, subject, message)
        self.assertTrue(response)


  
if __name__ == '__main__':
    unittest.main()
