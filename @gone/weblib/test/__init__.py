"""
test framework for weblib
"""

__ver__="$Id$"

from testActor import *
from testRequest import *
from testResponse import *
from testSess import *
from testAuth import *
from testEngine import *
from testScript import *
from testTools import *

suites = {
    "actor" : unittest.makeSuite(ActorTestCase, "check_"),
    "request" : unittest.makeSuite(RequestTestCase, "check_"),
    "response" : unittest.makeSuite(ResponseTestCase, "check_"),
    "sess" : unittest.makeSuite(SessTestCase, "check_"),
    "auth" : unittest.makeSuite(AuthTestCase, "check_"),
    "tools" : unittest.makeSuite(ToolsTestCase, "check_"),
    "engine" : unittest.makeSuite(EngineTestCase, "check_"),
    "script" : unittest.makeSuite(ScriptTestCase, "check_"),
    }

