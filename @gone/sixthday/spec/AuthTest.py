"""
testAuth.py - unit tests for weblib.Auth
"""
__ver__="$Id$"

import unittest
import weblib
import string
from weblib import trim
from sixthday import Auth

class AuthTest(unittest.TestCase):

    def setUp(self):
        # auth requires a PATH_INFO variable.. otherwise,
        # it doesn't know where to redirect the form.
        #
        # @TODO: is PATH_INFO correct? I think standard might be SCRIPT_NAME
        #
        self.myReq = weblib.Request(environ={"PATH_INFO":"dummy.py"})
        self.myRes = weblib.Response()
        self.sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                                self.myReq,
                                self.myRes)

    def check_check(self):
        try:
            auth = Auth(self.sess, {})
            auth.check()
            gotExit = 0
        except SystemExit:
            gotExit = 1
        assert gotExit, \
               "didn't get systemExit (from response.end)"
        assert string.find(self.myRes.buffer, Auth.PLEASELOGIN), \
               "check doesn't show login screen"
        

    def check_login_invalid(self):
        """
        Invalid login should show error, display form, and raise SystemExit.
        """
        req = weblib.Request(environ = {"PATH_INFO":"sadfaf"},
                             querystring="auth_check_flag=1",
                             form={"auth_username":"wrong_username",
                                   "auth_password":"wrong_password"})
        sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                           req, self.myRes)
        try:
            auth = Auth(sess, {'username':'password'})
            auth.check()
            gotExit = 0
        except SystemExit:
            gotExit = 1
        assert gotExit, \
               "invalid login didn't get SystemExit"
        assert string.find(self.myRes.buffer, auth.LOGINFAILED) > -1, \
               "invalid login doesn't give LOGINFAILED!"



    def check_login_valid(self):
        """
        Valid login should have no side effects.
        """
        req = weblib.Request(environ = {"PATH_INFO":"sadfaf"},
                             querystring="auth_check_flag=1",
                             form={"auth_username":"username",
                                   "auth_password":"password"})
        sess = weblib.Sess(weblib.SessPool.InMemorySessPool(),
                           req, self.myRes)
        try:
            auth = Auth(sess, {"username":"password"})
            auth.check()
            gotExit = 0
        except SystemExit:
            gotExit = 1
        assert self.myRes.buffer == "", \
               "valid login shouldn't output anything! [vs '%s']" \
               % self.myRes.buffer
        assert not gotExit, \
               "valid login still got SystemExit"


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

