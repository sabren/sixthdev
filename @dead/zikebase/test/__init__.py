
# test framework for zikebase

import MySQLdb
import zikebase.config
dbc = zikebase.config.test_dbc

from testContent import *
from testNode import *
from testObjectEditor import *
from testUser import *
from testUserAuth import *
from testPassword import *
from testRot13Password import *
from testUserApp import *

suites = {
    "objectEditor" : unittest.makeSuite(ObjectEditorTestCase, "check_"),
    "content" : unittest.makeSuite(ContentTestCase, "check_"),
    "user": unittest.makeSuite(UserTestCase, "check_"),
    "userAuth": unittest.makeSuite(UserAuthTestCase, "check_"),
    "userApp": unittest.makeSuite(UserAppTestCase, "check_"),
    "node" : unittest.makeSuite(NodeTestCase, "check_"),
    "password": unittest.makeSuite(PasswordTestCase, "check_"),
    "rot13pass": unittest.makeSuite(Rot13PasswordTestCase, "check_"),
}	

