import unittest
import zdc.test
import zikebase.test
from zikebase.test import dbc

from testCard import *
from testCart import *
from testCategory import *
from testCheckoutApp import * 
from testDetail import *
from testProduct import *
from testSale import *
from testSaleEditor import *
from testStore import *
suites = {}

## suites = zdc.test.suites
##
## # merge the lists
## for item in zikebase.test.suites.keys():
##     suites[item] = zikebase.test.suites[item]

suites['card'] = unittest.makeSuite(CardTestCase, "check_")
suites['cart'] = unittest.makeSuite(CartTestCase, "check_")
suites['category'] = unittest.makeSuite(CategoryTestCase, "check_")
suites['checkoutApp'] = unittest.makeSuite(CheckoutAppTestCase, "check_")
suites['detail'] = unittest.makeSuite(DetailTestCase, "check_")
suites['product'] = unittest.makeSuite(ProductTestCase, "check_")
suites['sale'] = unittest.makeSuite(SaleTestCase, "check_")
suites['saleeditor'] = unittest.makeSuite(SaleEditorTestCase, "check_")
suites['store'] = unittest.makeSuite(StoreTestCase, "check_")
