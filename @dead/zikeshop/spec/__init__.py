import unittest
import zdc.test
import zikebase.test

from sqlTest import dbc

from testProduct import *
from testCart import *
from testCategory import *
from testCustomer import *
from testStore import *
from testSale import *
from testCard import *
from testSaleEditor import *
from testCheckoutApp import * 
suites = {}

## suites = zdc.test.suites
##
## # merge the lists
## for item in zikebase.test.suites.keys():
##     suites[item] = zikebase.test.suites[item]

suites['category'] = unittest.makeSuite(CategoryTestCase, "check_")
suites['product'] = unittest.makeSuite(ProductTestCase, "check_")
suites['cart'] = unittest.makeSuite(CartTestCase, "check_")
suites['customer'] = unittest.makeSuite(CustomerTestCase, "check_")
suites['store'] = unittest.makeSuite(StoreTestCase, "check_")
suites['sale'] = unittest.makeSuite(SaleTestCase, "check_")
suites['card'] = unittest.makeSuite(CardTestCase, "check_")
suites['checkoutApp'] = unittest.makeSuite(CheckoutAppTestCase, "check_")
