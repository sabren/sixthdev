import unittest
import zdc.test
import zikebase.test
from zikebase.test import dbc

from testCard import *
from testCart import *
from testCategory import *
from testCheckoutApp import * 
from testShopApp import * 
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

suites['Card'] = unittest.makeSuite(CardTestCase, "check_")
suites['Cart'] = unittest.makeSuite(CartTestCase, "check_")
suites['Category'] = unittest.makeSuite(CategoryTestCase, "check_")
suites['CheckoutApp'] = unittest.makeSuite(CheckoutAppTestCase, "check_")
suites['ShopApp'] = unittest.makeSuite(ShopAppTestCase, "check_")
suites['Detail'] = unittest.makeSuite(DetailTestCase, "check_")
suites['Product'] = unittest.makeSuite(ProductTestCase, "check_")
suites['Sale'] = unittest.makeSuite(SaleTestCase, "check_")
suites['Saleeditor'] = unittest.makeSuite(SaleEditorTestCase, "check_")
suites['Store'] = unittest.makeSuite(StoreTestCase, "check_")
