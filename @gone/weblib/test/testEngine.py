"""
testEngine.py - unit tests for weblib.Engine
"""
__ver__="$Id$"

import os
import unittest
import weblib
from weblib import Engine
from weblib import trim

class EngineTestCase(unittest.TestCase):

    def check_globals(self):
        myscript = trim(
            """
            import weblib
            assert isinstance(REQ, weblib.Request)
            assert isinstance(RES, weblib.Response)
            assert isinstance(ENG, weblib.Engine)
            """)
        eng = Engine(script=myscript)
        eng.run()
        assert eng.result == Engine.SUCCESS, eng.error
        

    def check_print(self):
        import sys, StringIO
        eng = weblib.Engine(script=trim(
            """
            import weblib
            print >> RES, 'this should show'
            print 'this should not'
            """))
        tempout, sys.stdout = sys.stdout, StringIO.StringIO()
        eng.run()
        sys.stdout, tempout = tempout, sys.stdout
        assert eng.response.buffer == "this should show\n", \
               "doesn't grab prints after import weblib!"
        assert tempout.getvalue() == "this should not\n", \
               "doesn't print rest to stdout"


    def check_exit(self):
        try:
            eng = weblib.Engine(script="raise SystemExit")
            eng.run()
        except SystemExit:
            raise AssertionError, "Engine doesn't trap sys.exit()!"


    def check_runtwice(self):
        eng = weblib.Engine(script='print >> RES, "hello"')
        eng.run()
        eng.run()
        assert eng.response.buffer == "hello\n", \
               "engine doesn't let you run twice!"


    def check_on_exit(self):
        """
        engine.do_on_exit(XXX) should remember XXX and call it at end of page.
        """
        def nothing():
            pass
        
        eng = weblib.Engine(script="")
        eng.start()
        assert len(eng._exitstuff)==0, \
               "exitstuff not empty by default"
        
        eng.do_on_exit(nothing)
        assert len(eng._exitstuff)==1, \
               "do_on_exit doesn't add to exitstuff" 

        eng._exitstuff = []
        
        eng = weblib.Engine(script=trim(
            """
            # underscores on next line are just for emacs.. (trim strips them)
        ___ def cleanup():   
                print >> RES, 'wokka wokka wokka'
            ENG.do_on_exit(cleanup)
            """))
        eng.start()
        eng.execute(eng.script)
        assert len(eng._exitstuff) == 1, \
               "didn't register exit function: %s" % str(eng._exitstuff)

        eng.stop()
        assert eng.response.buffer=='wokka wokka wokka\n', \
               "got wrong response: %s" % eng.response.buffer
        


    def check_result(self):
        eng = weblib.Engine(script='1+1')
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

        eng.script = "import weblib; raise weblib.Redirect, '?newquery'"
        eng.run()
        assert eng.result == eng.REDIRECT, \
               "engine.result doesn't return REDIRECT on redirect."




    ## CGI-SPECIFIC (needs to move) ############################

    ## @TODO: this is really a test of Request
    def check_request(self):
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

    #@TODO: move to testRequest
    def check_form(self):
        weblib.MYFORM = {"a":"bcd"}
        try:
            myscript = trim(
                """
                import weblib
                assert REQ.form is weblib.MYFORM, \
                    'request uses wrong form'
                """)
            req = weblib.Request(form=weblib.MYFORM)
            eng = weblib.Engine(request=req, script=myscript)
            eng.run()
            assert eng.result == eng.SUCCESS, eng.result
        finally:
            del weblib.MYFORM
            

    # Is this really something Engine should do?
    # If so, why?
    def check_PATH_INFO(self):
        eng = weblib.Engine(script=open("test/pathinfo.py"))
        eng.start()
        assert eng.request.environ.get("PATH_INFO") == "test/pathinfo.py", \
               "Engine doesn't set PATH_INFO correctly for open()ed scripts."
        
