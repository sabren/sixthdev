"""
testAuth.py - unit tests for weblib.Auth

$Id$
"""
import unittest
import weblib
import string
from weblib import trim                                                         

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # auth requires a PATH_INFO variable.. otherwise,
        # it doesn't know where to redirect the form.
        self.myReq = weblib.Request(environ={"PATH_INFO":"dummy.py"})


    def check_engine(self):
        auth = weblib.Auth()
        assert auth.engine==weblib, "auth.engine doesn't default to weblib. :/"
        assert weblib.auth is auth, "auth doesn't register itself with weblib"


    def check_check(self):
        engine = weblib.Engine(request=self.myReq,
                               script="import weblib; weblib.auth.check()" )
        engine.run()
        assert string.find(engine.response.buffer, weblib.Auth.PLEASELOGIN), \
               "check doesn't show login screen"
        

    def check_prompt(self):
        engine = weblib.Engine(request=self.myReq, script=trim(
            """
            from weblib import auth
            auth.check()
            print "this should not show up"
            """))
        engine.run()
        assert string.find(engine.response.buffer,
                           engine.auth.PLEASELOGIN) > -1, \
               "doesn't show prompt!"


    def check_login(self):
        engine = weblib.Engine(
            request= 
            weblib.Request(environ = {"PATH_INFO":"sadfaf"},
                           querystring="auth_check_flag=1",
                           form={"auth_name":"wrong_username",
                                 "auth_pass":"wrong_password"},
                           ),
            script=
            trim(
                """
                import weblib
                weblib.auth.check()
                
                print "this should show up"
                """))
        
        engine.run()
        assert string.find(engine.response.buffer,
                           engine.auth.LOGINFAILED) > -1, \
               "invalid login doesn't give LOGINFAILED!"



        ## run it again with the "right" credentials 
        engine.request.form = {"auth_username" : "username",
                               "auth_password":"password"}
        engine.run()

        assert engine.response.buffer == "this should show up\n", \
               "valid login doesn't let you in!!!!"
        
        
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

