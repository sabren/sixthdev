# test framework for weblib
# (actually, this is pretty generic & could be used elsewhere..)

from testRequest import *
from testResponse import *
from testSess import *
from testAuth import *
from testPerm import *
#from testUser import *

import MySQLdb
from sqlTest import * # a module that defines the following four variables
dbc = MySQLdb.connect(db=DB, host=HOST, user=USER, passwd=PASSWD)

suites = {
    "request" : unittest.makeSuite(RequestTestCase, "check_"),
    "response" : unittest.makeSuite(ResponseTestCase, "check_"),
    "sess" : unittest.makeSuite(SessTestCase, "check_"),
    "auth" : unittest.makeSuite(AuthTestCase, "check_"),
    }


def run(full=0):
    failures, errors = 0, 0
    modules = ["Sess", "Auth", "Perm", "User", "Request"]
    if full:
        modules.append("uid")

    print "* unit tests"
    import unittest
    for m in modules:

        # make a new test suite
        suite = unittest.TestSuite()

        # get the TestCase...
        exec("import test" + m)
        testCaseClass = eval("test" + m + "." + m + "TestCase")
       
        # now add one test per "check*" method:
        for t in dir(testCaseClass):
            if t[:5] == "check":
                suite.addTest(testCaseClass(t))
                
        # finally, run the suite
        print "** testing " + m
        result = unittest.TextTestRunner().run(suite)
        failures = failures + len(result.failures)
        errors = errors + len(result.errors)
        print ""

    # summary
    print "* summary:\n"
    print failures, "failures,", errors, "errors in", len(modules), "modules.",
    if failures + errors == 0:
        print ":)"
    else:
        print ":("
    print ""
