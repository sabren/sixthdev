"""
testEngine.py - unit tests for weblib.Engine
"""
__ver__="$Id$"

import unittest
import weblib
from weblib import trim

class EngineTestCase(unittest.TestCase):

    def setUp(self):
        parts = ["request", "response"]
        for part in parts:
            if hasattr(weblib, part):
                delattr(weblib, part)


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

        myscript = trim(
            """
            import weblib
            assert weblib.request.form is weblib.MYFORM, \
                'request uses wrong form'
            """)

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
            engine = weblib.Engine(
                script="import weblib; weblib.response.end()")
            engine.run()
        except SystemExit:
            res = 0

        assert res==1, "Engine doesn't trap system.exit()!"



    def check_context(self):
        # default case:
        eng1 = weblib.Engine(script="print 'eng1'")   

        # explicit:
        eng2 = weblib.Engine(script="print 'eng2'")
        eng2.request=weblib.Request(engine=eng2)
        eng2.response=weblib.Response(engine=eng2)
                             
        # defaults after setting another engine explicitly:
        eng3 = weblib.Engine(script="print 'eng3'", )
        

        for eng in (eng1, eng2, eng3):
            eng.run()
            name = eng.response.buffer
            for what in ("request","response"):
                assert getattr(eng, what).engine is eng, \
                       ".engine screws up for " + name + "." + what
                assert getattr(getattr(eng, what).engine, what) \
                       is getattr(eng, what), \
                       ".eng." + what + " screws up for " + name 


    def check_weblib_defaults(self):
        """
        Engine should ALWAYS create a new copy of the objects in
        weblib.. The only time we use the ones in weblib is if we're
        not inside an Engine.
        """
        
        import weblib
        import __builtin__
        __builtin__.orig = {
            "request": getattr(weblib, "request", None), 
            "response": getattr(weblib, "response", None)}

        eng = weblib.Engine(script=trim(
            """
            import weblib
            
            assert weblib.request is not orig['request'], \
                  'weblib.request isn't fresh!'
            assert weblib.response is not orig['response'], \
                  'weblib.response isn't fresh!'
            """))

        eng.run()
        print eng.response.buffer
        

    def check_weblib_assigned(self):
        """
        Almost the same as above.. but make sure the ones we pass in are
        the ones that go into weblib..
        """

        import weblib
        import __builtin__

        self.request = weblib.Request(engine=self)
        self.response = weblib.Response(engine=self)

        
        __builtin__.good = {
            "request" : self.request,
            "response" : self.response
            }
        
        weblib.Engine(
            request = good["request"],
            response = good["response"],
            
            script=trim(
            """
            import weblib
            assert weblib.request is good['request'], \
                   'weblib.request is wrong!'
            assert weblib.response is good['response'], \
                   'weblib.response is wrong!'
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


    def check_result(self):
        eng = weblib.Engine(script='print "hello"')


        assert eng.result == None, \
               "engine.result doesn't default to None"
        
        eng.run()

        assert eng.result == eng.SUCCESS, \
               "engine.result doesn't return SUCCESS on success"

        eng.script = "print 'cat' + 5"
        eng.run()

        assert eng.result == eng.EXCEPTION, \
               "engine.result doesn't return EXCEPTION on error."



        eng.script = "assert 1==0, 'math is working.. :('"
        eng.run()

        assert eng.result == eng.FAILURE, \
               "engine.result doesn't return FAILURE on assertion failure."



    def check_PATH_INFO(self):
        eng = weblib.Engine(script=open("test/pathinfo.py"))
        eng.start()
        assert eng.request.environ.get("PATH_INFO") == "test/pathinfo.py", \
               "Engine doesn't set PATH_INFO correctly for open()ed scripts."
        
