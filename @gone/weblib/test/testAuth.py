#
# testAuth.py - unit tests for Auth.py
#

import unittest
from weblib.Auth import Auth

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()
        
    def checkCheck(self):
        pass

    def checkLogin(self):
        self.auth
        pass

    def checkLogout(self):
        pass

    def checkPrompt(self):
        pass

    def checkFetch(self):
        pass

    def checkValidate(self):
        pass

    def checkEncodeNormal(self):
        pass

    def checkEncodePassword(self):
        pass
    
    def checkRecovery(self):
        pass

    def checkPersistence(self):
        pass
    
    def tearDown(self):
        del self.auth 

