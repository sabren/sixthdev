"""
test suite for zikebase.UserApp
"""
__ver__="$Id$"

import unittest
import weblib
import sixthday
import sixthday.spec
from sixthday import Auth
from sixthday import SignupApp
from sixthday import User

class SignupAppTest(unittest.TestCase):

    def setUp(self):
        self.ds = sixthday.spec.dbc
        self.cur = self.ds.cursor()
        self.cur.execute("delete from base_user")
        self.cur.execute("delete from base_contact")

    def check_save(self):
        #import pdb; pdb.set_trace()
        req = {
            'username':'fred',
            'password':'tempy',
            'email':'fred@tempyco.com',
            }
        app = SignupApp(req, self.ds, Auth({},{}))
        #import pdb; pdb.set_trace()
        app.do("save")
        assert not app.errors, \
               "got errors saving fred: %s" % str(app.errors)
               
        #@TODO: I want to search by a field besides the key, but can't
        # until I finish refactoring zdc..
        fred = User(self.ds, username='fred')
        assert fred.email == 'fred@tempyco.com', \
               "email is wrong: %s" % fred.email
        
        # try to save again..
        app = SignupApp(req, self.ds, Auth({},{}))
        app.do("save")
        assert app.errors, \
               "didn't get errors saving duplicate fred"
        assert app.next == "signup", \
               "wrong next: %s" % app.next
