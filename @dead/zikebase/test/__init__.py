
# test framework for zikebase

import MySQLdb
from sqlTest import dbc

from testContent import *
from testNode import *
from testObjectEditor import *
from testUser import *
from testUserAuth import *

suites = {
    "objectEditor" : unittest.makeSuite(ObjectEditorTestCase, "check_"),
    "content" : unittest.makeSuite(ContentTestCase, "check_"),
    "user": unittest.makeSuite(UserTestCase, "check_"),
    "userAuth": unittest.makeSuite(UserAuthTestCase, "check_"),
    "node" : unittest.makeSuite(NodeTestCase, "check_"),
}	

