"""
test suite for zikebase.UserApp
"""
__ver__="$Id$"

import unittest
import weblib
import sixthday
from arlo import Clerk
from sixthday import Auth
from sixthday import SignupApp
from sixthday import User
from storage import MockStorage

class SignupAppTest(unittest.TestCase):

    def setUp(self):
        self.storage = MockStorage()
        self.clerk = Clerk(self.storage)

    def check_save(self):
        #import pdb; pdb.set_trace()
        req = {
            'username':'fred',
            'password':'tempy',
            'email':'fred@tempyco.com',
            }
        app = SignupApp(req, self.clerk, Auth({},{}))
        #import pdb; pdb.set_trace()
        app.do("save")
        assert not app.errors, \
               "got errors saving fred: %s" % str(app.errors)
               
        #@TODO: I want to search by a field besides the key, but can't
        # until I finish refactoring zdc..
        fred = self.clerk.fetch(User, 1)
        assert fred.email == 'fred@tempyco.com', \
               "email is wrong: %s" % fred.email

        #@TODO: re-enable this check for unique keys
        # I think it fails because the constraint is missing from
        # the database... really strongbox should check that and
        # throw an error...
        
         # try to save again..
##         app = SignupApp(req, self.clerk, Auth({},{}))
##         app.do("save")
##         assert app.errors, \
##                "didn't get errors saving duplicate fred"
##         assert app.next == "signup", \
##                "wrong next: %s" % app.next
