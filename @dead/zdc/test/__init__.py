import unittest

import sqlTestZdc, zdc
import zdc.drivers.DBAPI2Driver
dbc = zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlTestZdc.dbc))


from testIdxDict import *
from testRecord import *
from testObject import *
from testRecordObject import *
from testTable import *
from testLinkSet import *
from testJunction import *
from testConnection import *
from testDBAPI2Driver import *

suites = {
    "Connection" : unittest.makeSuite(ConnectionTestCase, "check_"),
    "LinkSet": unittest.makeSuite(LinkSetTestCase, "check_"),
    "IdxDict": unittest.makeSuite(IdxDictTestCase, "check_"),
    "Junction": unittest.makeSuite(JunctionTestCase, "check_"),
    "Record": unittest.makeSuite(RecordTestCase, "check_"),
    "Object": unittest.makeSuite(ObjectTestCase, "check_"),
    "RecordObject" : unittest.makeSuite(RecordObjectTestCase, "check_"),
    "Table": unittest.makeSuite(TableTestCase, "check_"),
    "DBAPI2Driver": unittest.makeSuite(DBAPI2DriverTestCase, "check_"),
    }

import zikebase.test
import zikeshop.test
suites.update(zikebase.test.suites)
suites.update(zikeshop.test.suites)


#@TODO: why not have some sort of scheme where if suite=="ALL"
#@TODO: it just magically loops through all the tests in __all__ ?
#@TODO: and applies makeSuite for "check_"...?
