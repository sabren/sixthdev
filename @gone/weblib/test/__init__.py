"""
test framework for weblib

$Id$
"""

from testActor import *
from testRequest import *
from testResponse import *
from testSess import *
from testAuth import *
from testPerm import *
from testEngine import *
from testScript import *
from testTools import *
#from testUser import *

# you should have a module called
# sqlTest that defines a DB-API 2.0 compliant
# connection object named dbc.

from sqlTest import dbc

suites = {
    "actor" : unittest.makeSuite(ActorTestCase, "check_"),
    "request" : unittest.makeSuite(RequestTestCase, "check_"),
    "response" : unittest.makeSuite(ResponseTestCase, "check_"),
    "sess" : unittest.makeSuite(SessTestCase, "check_"),
    "auth" : unittest.makeSuite(AuthTestCase, "check_"),
    "perm" : unittest.makeSuite(PermTestCase, "check_"),
    "tools" : unittest.makeSuite(ToolsTestCase, "check_"),
    "engine" : unittest.makeSuite(EngineTestCase, "check_"),
    "script" : unittest.makeSuite(ScriptTestCase, "check_"),
    }

