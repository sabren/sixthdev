"""
testRequest.py - unit tests for Request.py
"""

__ver__="$Id$"

import unittest
import weblib
from weblib import Request

class RequestTest(unittest.TestCase):

    def test_query(self):
        req = Request(querystring="a=1&b=2&b=3&e=em+cee+squared")
        assert req.query["a"] == "1", \
               "simple querystring not working"
        assert req.query["b"] == ("2", "3"), \
               "doesn't tupleize multiple values"
        assert req.query["e"] == "em cee squared", \
               "query's urldecoding not working"


    def test_getitem(self):
        req = Request(querystring="a=1&aa=2&aa=3&z1=querystring",
                      form={"b":"2", "z1":"form", "z2":"form"},
                      cookie={"c":"3", "z1":"cookie", "z2":"cookie",
                              "z3":"cookie"},
                      environ={"e":"mc2",
                               "z1":"environ", "z2":"environ",
                               "z3":"environ", "z4":"environ"})
        
        assert req["a"] == "1", \
               "getitem scews up on querystring"
        assert req["aa"] == ("2", "3"), \
               "getitem screws up on multiple values"
        assert req["b"] == "2", \
               "getitem screws up on forms"
        assert req["c"] == "3", \
               "getitem screws up on cookies"

        # it should fetch things in this order:
        assert req["z1"][0] == "querystring", \
               "getitem goes in wrong order (z1)"
        assert req["z2"][0] == "form", \
               "getitem goes in wrong order (z2)"
        assert req["z3"] == "cookie", \
               "getitem goes in wrong order (z3)"
        
        # environ is not part of the dictionary interface:
        assert (req.get("e") is None) and (req.get("z4") is None), \
               "request.__getitem__ should not access environ."


    def test_keys(self):
        req = Request(querystring="querystring=1",
                      form={"form":"1"},
                      cookie={"cookie":"1"},
                      environ={"environ":"1"})
        keys = req.keys()
        keys.sort()
        
        assert keys== ['cookie','form','querystring'], \
               "request.keys() doesn't work."


    def test_get(self):
        req = Request(querystring="a=1")
        assert req.get("a") == "1", \
               "get breaks for valid keys"
        assert req.get("b") is None, \
               "get breaks for non-present keys"


    def test_environ(self):
        myenv = {"A":"B"}
        eng = weblib.Engine(request=Request(environ=myenv))
        assert eng.request.environ["A"] == "B", \
               "request has wrong passed-in environ"


    def test_encoding(self):
        req = Request(content="a=<>")
        assert req.form["a"] == "<>", \
               "doesn't handle <> correctly (got %s)" \
               % repr(req.form["a"])


    def test_content(self):
        req = Request()
        assert req.content =="", \
               "request.content doesnt default to blank string"
        
        req = Request(content="abcdefg")
        assert req.content == "abcdefg", \
               "request doesn't store content correctly."
        
        assert req.contentType == "application/x-www-form-urlencoded", \
               "contentType doesn't default to application/...urlencoded"
        
        assert req.contentLength == 7, \
               "contentLength isn't correct for passed-in content."
        


    def test_contentType(self):
        req=Request()
        assert req.contentType == "application/x-www-form-urlencoded", \
               "contentType doesn't default to application/...urlencoded"

        req=Request(environ={"CONTENT_TYPE":"text/plain"},
                        content="")
        assert req.contentType == "text/plain", \
               "req.contentType doesn't read contentType from environment"

        req=Request(contentType="text/xml")
        assert req.contentType=="text/xml", \
               "req.contentType didn't get set based on init's parameter"

    def test_multipart(self):
        raise "skip"
        req = Request(
            method="POST",
            contentType=
            "multipart/form-data; boundary=---------------------------7d035c305e4",
            content=weblib.trim(
            """
            -----------------------------7d035c305e4
            Content-Disposition: form-data; name="upfile"; filename="mime.test"
            Content-Type: text/plain

            THIS IS A TEST
            THIS IS ONLY A TEST

            -----------------------------7d035c305e4
            Content-Disposition: form-data; name="action"
            
            upload
            -----------------------------7d035c305e4
            Content-Disposition: form-data; name="twovalues"
            
            value1
            -----------------------------7d035c305e4
            Content-Disposition: form-data; name="twovalues"
            
            value2
            -----------------------------7d035c305e4--
            """            
            ))

        #@TODO: try MIME-generation module instead of hard-coding the string..
        assert request.form.get("action")=="upload", \
               weblib.trim(
               """
               form values don't work on multipart forms. (got %s)
               -----------
               ** NOTE **
               this test works when I test manually, but not via
               the test script.. The bug appears to be in using StringIO
               (rather than sys.stdin) with the cgi.FieldStorage, or in
               some invisible characters in the MIME stuff.. 
               I have never been able to track it down... (help?)
               -----------
               """
               % repr(request.form.get("action")))

        assert request.form["upfile"].filename == "C:\mimetest.txt", \
               "file uploads don't return FieldStorage objects"

        assert request.form["twovalues"] == ("value1", "value2"), \
               "multi-value fields break on multi-part forms."


    def test_ampersand(self):
        """
        ampersand is %26 .. what if the querystring or
        form or whatever has an ampersand in it? At one
        point, urlDecode()ing it would break the value in
        two pieces...
        """
        ampstr = "a=apple&b=boys%26girls"
        req = Request(content=ampstr, querystring=ampstr)
        goal = {"a":"apple", "b":"boys&girls"}

        assert req.query == goal, \
               ".query doesn't grok ampersands."

        assert req.form == goal, \
               ".query doesn't grok ampersands."

