"""
testUser.py - test suite for zikebase.User

$Id$
"""

import unittest
import zikebase

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("DELETE FROM base_user")
        # username: username.. password: password
        self.cur.execute("INSERT INTO base_user (username, password) "
                         "VALUES ('username', '$1$pw$D/pJQB6/3vtfaOYajbG6l0')")
        self.cur.execute("INSERT INTO base_contact (userID) values (0)")
        

    def check_password(self):
        user = zikebase.User(ID=1)

        zikebase.load("Password")
        assert isinstance(user.password, zikebase.Password), \
               "user.password doesn't return a Password object"

        assert user.password == "password", \
               "user.password doesn't work right"
        
    

    def tearDown(self):
	pass
