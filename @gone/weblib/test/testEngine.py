#
# testEngine.py - unit tests for Engine.py
#

import unittest
import weblib

class EngineTestCase(unittest.TestCase):


    def check_init(self):
        import os
        os.environ["QUERY_STRING"]="enginetest"
        engine = weblib.Engine()
        
        assert engine.request.querystring=="enginetest", \
               "engine has wrong default request"

        del engine

        request = weblib.Request(querystring="e=mc2&this=a+test")
        engine = weblib.Engine(request=request)
        assert engine.request.querystring=="e=mc2&this=a+test", \
               "engine has wrong passed-in request"
