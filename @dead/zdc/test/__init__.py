import unittest
import zdc
import sqlTest # note: this has to come after zdc, or tests break. (WHY?!?!)
import zdc.drivers.DBAPI2Driver
dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlTest.dbc))


from testRecord import *
from testObject import *
from testRecordObject import *
from testTable import *
from testLinkSet import *
from testJunction import *
from testConnection import *
from testDBAPI2Driver import *
from testObjectView import *
from testFunctions import *

suites = {
    "Connection" : unittest.makeSuite(ConnectionTestCase, "check_"),
    "LinkSet": unittest.makeSuite(LinkSetTestCase, "check_"),
    "Junction": unittest.makeSuite(JunctionTestCase, "check_"),
    "Record": unittest.makeSuite(RecordTestCase, "check_"),
    "Object": unittest.makeSuite(ObjectTestCase, "check_"),
    "RecordObject" : unittest.makeSuite(RecordObjectTestCase, "check_"),
    "Table": unittest.makeSuite(TableTestCase, "check_"),
    "DBAPI2Driver": unittest.makeSuite(DBAPI2DriverTestCase, "check_"),
    "ObjectView": unittest.makeSuite(ObjectViewTestCase, "check_"),
    "Functions": unittest.makeSuite(FunctionsTestCase, "check_"),
    }

