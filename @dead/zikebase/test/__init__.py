
# test framework for zikebase

import MySQLdb
from sqlTest import dbc

from testContent import *
from zdc.test.testObject import *  #@TODO: take this out?

suites = {
    "object" : unittest.makeSuite(ObjectTestCase, "check_"),
    "content" : unittest.makeSuite(ContentTestCase, "check_"),
}	

