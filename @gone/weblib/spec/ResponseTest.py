"""
$Id$
"""
import unittest
from weblib import Finished
from weblib import Response

class ResponseTest(unittest.TestCase):

    def setUp(self):
        self.response = Response()
        
    def test_init(self):
        assert self.response.buffer=="", \
               "response.buffer doesn't initialize correctly."

    def test_write(self):
        self.response.write("hello, world")
        assert self.response.buffer == "hello, world", \
               "response.write() doesn't work"
        
    def test_end(self):
        try:
            self.response.end()
            gotIt = 0
        except Finished:
            gotIt = 1
        assert gotIt, "response.end() doesn't raise Finished!"

    def test_simpleRedirect(self):
        #@TODO: use idxDict for status
        self.assertRaises(Finished,
                          self.response.redirect, "http://www.sabren.com/")
        assert self.response.headers[0] == ("Status", "303"),\
               "didn't get Status: 303 header on redirect- %s" \
               % self.response.headers
        assert self.response.headers[1] \
               == ("Location", "http://www.sabren.com/"),\
               "didn't get Location: header on redirect - %s" \
               % self.response.headers

    def test_queryRedirect(self):
        """
        if the first char of a redirect is ?, should redirect to
        the current url with the querystring.

        BUT: this is actually handled by Engine, because Response
        doesn't know anything at all about what page we're looking
        at. That info is stored in the Request.

        See EngineTest.test_redirectToQuerystring() for details.       
        """       
        self.assertRaises(Finished, self.response.redirect, "?a=b")

