"""
test suite for zikebase.UserApp

$Id$
"""

import unittest
import zikebase

class UserAppTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("delete from base_user")
        self.cur.execute("delete from base_contact")

    def check_create(self):
        req = {
            'username':'fred',
            'password':'tempy',
            'email':'fred@tempyco.com',
            }
        app = zikebase.UserApp(input=req)
        app.do("create")

        fred = zikebase.User(username='fred')
        assert fred.email == 'fred@tempyco.com', \
               "email is wrong: %s" % fred.email
        
