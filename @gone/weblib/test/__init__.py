"""
test framework for weblib
"""
__ver__="$Id$"

from testRequest import *
from testResponse import *
from testSess import *
from testEngine import *

suites = {
    "request" : unittest.makeSuite(RequestTestCase, "check_"),
    "response" : unittest.makeSuite(ResponseTestCase, "check_"),
    "sess" : unittest.makeSuite(SessTestCase, "check_"),
    "engine" : unittest.makeSuite(EngineTestCase, "check_"),
}
