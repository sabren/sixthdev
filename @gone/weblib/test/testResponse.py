#
# testResponse.py - unit tests for Response.py
#

import unittest
import weblib

class ResponseTestCase(unittest.TestCase):


    def setUp(self):
        self.response = weblib.Response()
        
        
    def check_init(self):
        assert self.response.buffer=="", \
               "response.buffer doesn't initialize correctly."


    def check_engine(self):
        assert self.response.engine==weblib, "response.engine doesn't default to weblib. :/"
        assert weblib.response is self.response, "response doesn't register itself with weblib"


    def check_write(self):
        self.response.write("hello, world")
        assert self.response.buffer == "hello, world", \
               "response.write() doesn't work"

    def check_end(self):
        res = 0
        try:
            self.response.end()
        except SystemExit:
            res = 1

        assert res == 1, "response.end() doesn't exit!"
