
# test framework for zikebase

import MySQLdb
import zikebase, zikebase.config
dbc = zikebase.dbc = zikebase.config.test_dbc

from testContent import *
from testUser import *
from testUserAuth import *
from testPassword import *
from testRot13Password import *
from testContact import *

suites = {
    "Content" : unittest.makeSuite(ContentTestCase, "check_"),
    "User": unittest.makeSuite(UserTestCase, "check_"),
    "UserAuth": unittest.makeSuite(UserAuthTestCase, "check_"),
    "Password": unittest.makeSuite(PasswordTestCase, "check_"),
    "Rot13pass": unittest.makeSuite(Rot13PasswordTestCase, "check_"),
    "Contact": unittest.makeSuite(ContactTestCase, "check_"),
}	

