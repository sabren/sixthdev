"""
testUserAuth.py - test suite for zikebase.UserAuth

$Id$
"""

import string
import weblib
import unittest
import zikebase.test


class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()
        self.myReq = weblib.Request(environ={"PATH_INFO":"dummy.py"})


    def check_prompt(self):
        engine = weblib.Engine(request=self.myReq, script=weblib.trim(
            """
            from weblib import auth
            auth.check()
            print "this should not show up"
            """))
        engine.run()

        assert string.find(engine.response.buffer, engine.auth.PLEASELOGIN) > -1, \
               "doesn't show prompt!"


    def tearDown(self):
	pass

