"""
testResponse.py - unit tests for weblib.Response

$Id$
"""
import unittest
import weblib

class ResponseTestCase(unittest.TestCase):


    def setUp(self):
        self.response = weblib.Response()
        
        
    def check_init(self):
        assert self.response.buffer=="", \
               "response.buffer doesn't initialize correctly."



    def check_engine(self):
        #@TODO: get rid of this code now that I have weblib.script.. (??)
        assert self.response.engine==weblib, \
               "response.engine doesn't default to weblib. :/"
        assert weblib.response is self.response, \
               "response doesn't register itself with weblib"



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



    def check_cgiEnd(self):
        import os, string
        actual = os.popen(
            'python -c"import weblib.script; print \'x\'; weblib.response.end()"'
            ).readlines()

        # scond line should be the set-cookie. ignore it!
        actual = string.join([actual[0]] + actual[2:], '')
        
        assert actual == "Content-type: text/html\n\nx\n", \
               "CGI doesn't flush after response.end()"
        
