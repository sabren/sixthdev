"""
testUser.py - test suite for zikebase.User

$Id$
"""

import unittest
import zikebase

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.ds = zikebase.test.dbc
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("DELETE FROM base_user")
        self.cur.execute("DELETE FROM base_contact")
        # username: username.. password: password
        self.cur.execute(
            """
            INSERT INTO base_user (ID, username, password) 
            VALUES (1, 'username', '$1$pw$D/pJQB6/3vtfaOYajbG6l0')
            """)
        self.cur.execute(
            """
            INSERT INTO base_contact (ID, userID) values (1, 0)
            """)
        

    def check_password(self):
        user = zikebase.User(self.ds, ID=1)

        zikebase.load("Password")
        assert isinstance(user.password, zikebase.Password), \
               "user.password doesn't return a Password object"

        assert user.password == "password", \
               "user.password doesn't work right"


    def check_save(self):
        user = zikebase.User(self.ds)
        try:
            user.save()
            gotError = 0
        except:
            gotError = 1
        assert gotError, \
               "didn't get error trying to save usernameless User"

        user.username ="elmer"
        try:
            user.save()
            gotError = 0
        except:
            gotErrror = 1
        assert not gotError, \
               "got error after setting username!"

        user2 = zikebase.User(self.ds)
        try:
            user2.username = "elmer"
            gotError = 0
        except:
            gotError = 1
        assert gotError, \
               "didn't get error setting duplicate username"
        
    def tearDown(self):
	pass
