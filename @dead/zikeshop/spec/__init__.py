import unittest
import zdc.test
import zikebase.test

from sqlTest import dbc

from testAdminPages import *
from testPublicPages import *
from testProduct import *
from testCart import *
from testCategory import *
from testBagger import *
from testCashier import *
from testCustomer import *
from testAddress import *
from testShopActor import *

suites = {}

## suites = zdc.test.suites
##
## # merge the lists
## for item in zikebase.test.suites.keys():
##     suites[item] = zikebase.test.suites[item]

suites['publicpages'] = unittest.makeSuite(PublicPagesTestCase, "check_")
suites['adminpages'] = unittest.makeSuite(AdminPagesTestCase, "check_")
suites['category'] = unittest.makeSuite(CategoryTestCase, "check_")
suites['product'] = unittest.makeSuite(ProductTestCase, "check_")
suites['cart'] = unittest.makeSuite(CartTestCase, "check_")
suites['bagger'] = unittest.makeSuite(BaggerTestCase, "check_")
suites['cashier'] = unittest.makeSuite(CashierTestCase, "check_")
suites['customer'] = unittest.makeSuite(CustomerTestCase, "check_")
suites['address'] = unittest.makeSuite(AddressTestCase, "check_")
suites['shopactor'] = unittest.makeSuite(ShopActorTestCase, "check_")
