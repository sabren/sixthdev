"""
testAuth.py - unit tests for weblib.Auth
"""
__ver__="$Id$"

import unittest
import weblib
import string
from weblib import trim, Finished
from sixthday import Auth

class AuthTest(unittest.TestCase):

    def setUp(self):
        self.myReq = weblib.RequestBuilder().build(
            method="GET",querystring="",
            path="/",
            form={},
            cookie={},content={})
        self.myRes = weblib.Response()
        self.sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                                self.myReq,
                                self.myRes)

    def check_check(self):
        try:
            auth = Auth(self.sess, {})
            auth.check()
            gotExit = 0
        except Finished:
            gotExit = 1
        assert gotExit, \
               "didn't get systemExit (from response.end)"
        assert string.find(self.myRes.buffer, Auth.PLEASELOGIN), \
               "check doesn't show login screen"
        

    def check_login_invalid(self):
        """
        Invalid login should show error, display form, and raise Finished.
        """
        req = weblib.RequestBuilder().build(
            querystring="auth_check_flag=1",
            path="/",
            form={"auth_username":"wrong_username",
                  "auth_password":"wrong_password"})
        sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                           req, self.myRes)
        try:
            auth = Auth(sess, {'username':'password'})
            auth.check()
            gotExit = 0
        except Finished:
            gotExit = 1
        assert gotExit, \
               "invalid login didn't get Finished"
        assert string.find(self.myRes.buffer, auth.LOGINFAILED) > -1, \
               "invalid login doesn't give LOGINFAILED!"



    def check_login_valid(self):
        """
        Valid login should have no side effects.
        """
        req = weblib.RequestBuilder().build(
            querystring="auth_check_flag=1",
            path="/",
            form={"auth_username":"username",
                  "auth_password":"password"})
        sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                           req, self.myRes)
        try:
            auth = Auth(sess, {"username":"password"})
            auth.check()
            gotExit = 0
        except Finished:
            gotExit = 1
        assert self.myRes.buffer == "", \
               "valid login shouldn't output anything! [vs '%s']" \
               % self.myRes.buffer
        assert not gotExit, \
               "valid login still threw Finished"


    # @TODO: write tests for this stuff:
        
    def nocheck_Logout(self):
        pass

    def nocheck_Fetch(self):
        pass

    def nocheck_Validate(self):
        pass

    def nocheck_EncodeNormal(self):
        pass

    def nocheck_EncodePassword(self):
        pass
    
    def nocheck_Recovery(self):
        pass

    def nocheck_Persistence(self):
        pass
    
    def tearDown(self):
        pass
        #del self.auth 

