"""
testEngine.py - unit tests for weblib.Engine

$Id$
"""
import unittest
import weblib
from weblib import trim

class EngineTestCase(unittest.TestCase):


    def check_request(self):
        import os
        os.environ["QUERY_STRING"]="enginetest"
        engine = weblib.Engine()
        
        assert engine.request.querystring=="enginetest", \
               "engine has wrong default request"

        del engine

        req = weblib.Request(querystring="e=mc2&this=a+test")
        engine = weblib.Engine(request=req)
        assert engine.request.querystring=="e=mc2&this=a+test", \
               "engine has wrong passed-in request:" + \
               engine.request.querystring


    def check_form(self):

        weblib.MYFORM = {"a":"bcd"}

        myscript = "import weblib\n" +\
                   "assert weblib.request.form is weblib.MYFORM, 'request uses wrong form'"

        req = weblib.Request(form=weblib.MYFORM)
        weblib.Engine(request=req, script=myscript).run()


        del weblib.MYFORM



    def check_simple(self):
        engine = weblib.Engine(script="print 'hello'")
        engine.run()
        assert engine.response.buffer == "hello\n", \
               "engine doesn't execute the script!"
        

    def check_responseEnd(self):
        res = 1
        try:
            engine = weblib.Engine(script="import weblib; weblib.response.end()")
            engine.run()
        except SystemExit:
            res = 0

        assert res==1, "Engine doesn't trap system.exit()!"



    def check_context(self):
        eng1 = weblib.Engine(script="print 'eng1'")   # default case
        eng2 = weblib.Engine(script="print 'eng2'",   # explicit 
                             auth=weblib.Auth(),
                             sess=weblib.Sess(),
                             perm=weblib.Perm(),
                             request=weblib.Request(),
                             response=weblib.Response())
        eng3 = weblib.Engine(script="print 'eng3'", ) # default after explicit pass

        for eng in (eng1, eng2, eng3):
            eng.run()
            name = eng.response.buffer
            for what in ("auth","sess","perm","request","response"):
                assert getattr(eng, what).engine is eng, \
                       ".eng screws up for " + name + "." + what
                assert getattr(getattr(eng, what).engine, what) is getattr(eng, what), \
                       ".eng." + what + " screws up for " + name 


    def check_weblib_defaults(self):
        
        """Engine should ALWAYS create a new copy of the objects in
        weblib.. The only time we use the ones in weblib is if we're
        not inside an Engine."""
        
        import weblib
        import __builtin__
        __builtin__.orig = {
            "auth": weblib.auth,
            "sess": weblib.sess,
            "perm": weblib.perm,
            "request": weblib.request,
            "response": weblib.response }

        eng = weblib.Engine(script=trim(
            """
            import weblib
            
            assert weblib.auth is not orig["auth"], "weblib.auth isn't fresh!"
            assert weblib.sess is not orig["sess"], "weblib.sess isn't fresh!"
            assert weblib.perm is not orig["perm"], "weblib.perm isn't fresh!"
            assert weblib.request is not orig["request"], "weblib.request isn't fresh!"
            assert weblib.response is not orig["response"], "weblib.response isn't fresh!"

            """))

        eng.run()
        print eng.response.buffer
        

    def check_weblib_assigned(self):

        """Almost the same as above.. but make sure the ones we pass in are
        the ones that go into weblib.."""

        import weblib
        import __builtin__
        
        __builtin__.good = {
            "auth" : weblib.Auth(),
            "sess" : weblib.Sess(),
            "perm" : weblib.Perm(),
            "request" : weblib.Request(),
            "response" : weblib.Response()
            }
        
        weblib.Engine(
            auth = good["auth"],
            sess = good["sess"],
            perm = good["perm"],
            request = good["request"],
            response = good["response"],
            
            script=trim(
            """
            import weblib
            
            assert weblib.auth is good["auth"], "weblib.auth is wrong!"
            assert weblib.sess is good["sess"], "weblib.sess is wrong!"
            assert weblib.perm is good["perm"], "weblib.perm is wrong!"
            assert weblib.request is good["request"], "weblib.request is wrong!"
            assert weblib.response is good["response"], "weblib.response is wrong!"
            """)

            ).run()

        del __builtin__.good



    def check_print(self):
        eng = weblib.Engine(script='import weblib; print "hello"')
        eng.run()
        assert eng.response.buffer == "hello\n", \
               "doesn't grab prints after import weblib!"



    def check_runtwice(self):
        eng = weblib.Engine(script='print "hello"')
        eng.run()
        eng.run()

        assert eng.response.buffer == "hello\n", \
               "engine doesn't let you run twice!"



    def check_cgi(self):
        import os, string
        actual = os.popen('python -c"import weblib.script; print \'hello\'"').readlines()

        # scond line should be the set-cookie. ignore it!
        actual = string.join([actual[0]] + actual[2:], '')
        
        target = trim(
            """
            Content-type: text/html
            
            hello
            """)

        assert actual==target, "didn't get headers in CGI-mode!"



