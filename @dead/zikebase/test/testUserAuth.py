"""
testUserAuth.py - test suite for zikebase.UserAuth
"""
__ver__="$Id$"

import string
import weblib, weblib.SessPool
import unittest
import zikebase.test

class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.ds = zikebase.test.dbc
        self.cur = zikebase.test.dbc.cursor()
        self.myReq = weblib.Request(environ={"PATH_INFO":"dummy.py"})


    def check_prompt(self):
        wres = weblib.Response()
        sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                           self.myReq,
                           wres)
        auth = zikebase.UserAuth(sess, self.ds)
        try:
            auth.check()
            gotExit=0
        except SystemExit:
            gotExit=1

        assert gotExit, \
               "should have demanded login"

        assert string.find(wres.buffer, auth.PLEASELOGIN) > -1, \
               "doesn't show prompt!"


    def tearDown(self):
	pass

