
# test framework for zikebase

import MySQLdb
from sqlTest import * # a module that defines the following four variables
dbc = MySQLdb.connect(db=DB, host=HOST, user=USER, passwd=PASSWD)

from testContent import *
from zdc.test.testObject import *  #@TODO: take this out?

suites = {
    "object" : unittest.makeSuite(ObjectTestCase, "check_"),
    "content" : unittest.makeSuite(ContentTestCase, "check_"),
}	

