"""
testRequest.py - unit tests for Request.py

$Id$
"""

import unittest
import weblib

class RequestTestCase(unittest.TestCase):
    
    def check_engine(self):
        request = weblib.Request()
        assert request.engine==weblib, "request.engine doesn't default to weblib. :/"
        assert weblib.request is request, "request doesn't register itself with weblib"
        

    def check_query(self):
        request = weblib.Request(querystring="a=1&b=2&b=3&e=em+cee+squared")
        assert request.query["a"] == "1", "simple querystring not working"
        assert request.query["b"] == ("2", "3"), "doesn't tupleize multiple values"
        assert request.query["e"] == "em cee squared", "query's urldecoding not working"


    def check_getitem(self):
        request = weblib.Request(querystring="a=1&aa=2&aa=3&z1=querystring",

                                 form={"b":"2", "z1":"form", "z2":"form"},

                                 cookie={"c":"3", "z1":"cookie", "z2":"cookie",
                                         "z3":"cookie"},
                                 
                                 environ={"e":"mc2", "z1":"environ", "z2":"environ",
                                          "z3":"environ", "z4":"environ"})

        assert request["a"] == "1", "getitem scews up on querystring"
        assert request["aa"] == ("2", "3"), "getitem screws up on multiple values"
        assert request["b"] == "2", "getitem screws up on forms"
        assert request["c"] == "3", "getitem screws up on cookies"
        assert request["e"] == "mc2", "getitem screws up on environ"

        # it should fetch things in this order:
        assert request["z1"][0] == "querystring", "getitem goes in wrong order (z1)"
        assert request["z2"][0] == "form", "getitem goes in wrong order (z2)"
        assert request["z3"][0] == "cookie", "getitem goes in wrong order (z3)"
        assert request["z4"] == "environ", "getitem goes in wrong order (z4)"



    def check_get(self):
        request = weblib.Request(querystring="a=1")

        assert request.get("a") == "1", "get breaks for valid keys"
        assert request.get("b") is None, "get breaks for non-present keys"



    def check_environ(self):
        myenv = {"A":"B"}
        eng = weblib.Engine(request=weblib.Request(environ=myenv))
        assert eng.request["A"] == "B", "request has wrong passed-in environ"



    def check_encoding(self):
        request = weblib.Request(content="a=<>")

        assert request.form["a"] == "<>", "doesn't handle <> correctly"



    def check_content(self):
        request = weblib.Request()
        assert request.content is None, \
               "request.content doesnt default to None"
        
        request = weblib.Request(content="abcdefg")
        assert request.content == "abcdefg", \
               "request doesn't store content correctly."
        
        assert request.contentType == "application/x-www-form-urlencoded", \
               "request.contentType doesn't default to application/x-www-form-urlencoded"

        assert request.contentLength == 7, \
               "request.contentLength isn't calculated correctly for passed-in content."



    def check_contentType(self):
        request=weblib.Request()
        assert request.contentType == None, \
               "request.contentType doesn't default to application/x-www-form-urlencoded"


        request=weblib.Request(environ={"CONTENT_TYPE":"text/plain"}, content="")
        assert request.contentType == "text/plain", \
               "request.contentType doesn't read contentType from environment"

        request=weblib.Request(contentType="text/xml")
        assert request.contentType=="text/xml", \
               "request.contentType didn't get set based on init's parameter"
    


    def check_multipart(self):
        request = weblib.Request(

            contentType=
            "multipart/form-data; boundary=---------------------------7d035c305e4",

            content=weblib.trim(
            """
            -----------------------------7d035c305e4
            Content-Disposition: form-data; name="upfile"; filename="C:\mimetest.txt"
            Content-Type: text/plain

            THIS IS A TEST
            THIS IS ONLY A TEST

            -----------------------------7d035c305e4
            Content-Disposition: form-data; name="action"

            upload
            -----------------------------7d035c305e4--
            """
            ))

        assert request.form.get("action")=="upload", \
               "form values don't work on multipart forms."


        assert request.form["upfile"].filename == "C:\mimetest.txt", \
               "file uploads don't return FieldStorage objects"
