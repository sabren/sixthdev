
# test framework for zikebase

import MySQLdb
import zikebase, zikebase.config
dbc = zikebase.dbc = zikebase.config.test_dbc

from testContent import *
from testNode import *
from testObjectEditor import *
from testUser import *
from testUserAuth import *
from testPassword import *
from testRot13Password import *
from testUserApp import *
from testAdminApp import *
from testContact import *

suites = {
    "ObjectEditor" : unittest.makeSuite(ObjectEditorTestCase, "check_"),
    "Content" : unittest.makeSuite(ContentTestCase, "check_"),
    "User": unittest.makeSuite(UserTestCase, "check_"),
    "UserAuth": unittest.makeSuite(UserAuthTestCase, "check_"),
    "UserApp": unittest.makeSuite(UserAppTestCase, "check_"),
    "AdminApp": unittest.makeSuite(AdminAppTestCase, "check_"),
    "Node" : unittest.makeSuite(NodeTestCase, "check_"),
    "Password": unittest.makeSuite(PasswordTestCase, "check_"),
    "Rot13pass": unittest.makeSuite(Rot13PasswordTestCase, "check_"),
    "Contact": unittest.makeSuite(ContactTestCase, "check_"),
}	

