

import unittest
from sqlTest import dbc

from testIdxDict import *
from testRecord import *
from testObject import *
from testRecordObject import *
from testTable import *

suites = {
    "IdxDict": unittest.makeSuite(IdxDictTestCase, "check_"),
    "Record": unittest.makeSuite(RecordTestCase, "check_"),
    "Object": unittest.makeSuite(ObjectTestCase, "check_"),
    "RecordObject" : unittest.makeSuite(RecordObjectTestCase, "check_"),
    "Table": unittest.makeSuite(TableTestCase, "check_"),
    }


#@TODO: why not have some sort of scheme where if suite=="ALL"
#@TODO: it just magically loops through all the tests in __all__ ?
#@TODO: and applies makeSuite for "check_"...?
