import unittest
import zdc.test
import zikebase.test

from sqlTest import dbc

from testAdminPages import *
from testProduct import *

suites = {}

## suites = zdc.test.suites
##
## # merge the lists
## for item in zikebase.test.suites.keys():
##    suites[item] = zikebase.test.suites[item]

suites['adminpages'] = unittest.makeSuite(AdminPagesTestCase, "check_")
suites['product'] = unittest.makeSuite(ProductTestCase, "check_")
