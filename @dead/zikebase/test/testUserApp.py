"""
test suite for zikebase.UserApp
"""
__ver__="$Id$"

import unittest
import zikebase

class UserAppTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("delete from base_user")
        self.cur.execute("delete from base_contact")

    def check_save(self):
        #import pdb; pdb.set_trace()
        req = {
            'username':'fred',
            'password':'tempy',
            'email':'fred@tempyco.com',
            }
        app = zikebase.UserApp(input=req)
        app.do("save")
        assert not app.errors, "got errors saving fred: %s" % str(app.errors)
               
        #@TODO: I want to search by a field besides the key, but can't
        # until I finish refactoring zdc..
        fred = zikebase.User(username='fred')

        assert fred.email == 'fred@tempyco.com', \
               "email is wrong: %s" % fred.email
        
