#
# testRequest.py - unit tests for Request.py
#

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
        assert request["aa"] == "2", "getitem screws up on multiple values"
        assert request["b"] == "2", "getitem screws up on forms"
        assert request["c"] == "3", "getitem screws up on cookies"
        assert request["e"] == "mc2", "getitem screws up on environ"

        # it should fetch things in this order:
        assert request["z1"] == "querystring", "getitem goes in wrong order (z1)"
        assert request["z2"] == "form", "getitem goes in wrong order (z2)"
        assert request["z3"] == "cookie", "getitem goes in wrong order (z3)"
        assert request["z4"] == "environ", "getitem goes in wrong order (z4)"



    def check_get(self):
        request = weblib.Request(querystring="a=1")

        assert request.get("a") == "1", "get breaks for valid keys"
        assert request.get("b") is None, "get breaks for non-present keys"
