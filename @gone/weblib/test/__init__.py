# test framework for weblib
# (actually, this is pretty generic & could be used elsewhere..)

from testRequest import *
from testResponse import *
from testSess import *
from testAuth import *
from testPerm import *
from testEngine import *
#from testUser import *

import MySQLdb
from sqlTest import * # a module that defines the following four variables
dbc = MySQLdb.connect(db=DB, host=HOST, user=USER, passwd=PASSWD)

suites = {
    "request" : unittest.makeSuite(RequestTestCase, "check_"),
    "response" : unittest.makeSuite(ResponseTestCase, "check_"),
    "sess" : unittest.makeSuite(SessTestCase, "check_"),
    "auth" : unittest.makeSuite(AuthTestCase, "check_"),
    "perm" : unittest.makeSuite(PermTestCase, "check_"),
    "engine" : unittest.makeSuite(EngineTestCase, "check_"),
    }

