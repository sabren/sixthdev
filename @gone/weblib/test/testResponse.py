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


    def check_simpleRedirect(self):
        self.assertRaises(SystemExit,
                     self.response.redirect, "http://www.sabren.com/")
        assert self.response.headers[0] == ("Status", "303"),\
               "didn't get Status: 303 header on redirect- %s" \
               % self.response.headers
        assert self.response.headers[1] \
               == ("Location", "http://www.sabren.com/"),\
               "didn't get Location: header on redirect - %s" \
               % self.response.headers


    def check_queryRedirect(self):
        """
        if the first char of a redirect is ?, should redirect to
        the current url with the querystring.
        """
        self.assertRaises(SystemExit, self.response.redirect, "?a=b")
        

## this causes problems for python 2.0
##
##     def check_cgiEnd(self):
##         import os, string
##         proc = os.popen(
##             'python -c"import weblib.script; print \'x\'; weblib.response.end()"'
##             )
        
##         actual = proc.readlines()
##         proc.close()

##         # scond line should be the set-cookie. ignore it!
##         actual = string.join([actual[0]] + actual[2:], '')
        
##         assert actual == "Content-type: text/html\n\nx\n", \
##                "CGI doesn't flush after response.end()"
        
