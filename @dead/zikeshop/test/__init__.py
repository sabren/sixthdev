import unittest
import zdc.test
import zikebase.test

from sqlTest import dbc

from testPublicPages import *
from testProduct import *
from testCart import *
from testCategory import *
from testCustomer import *
from testShopActor import *
from testStore import *
from testSale import *
from testCard import *
from testSaleEditor import *
from testCheckoutApp import * 
suites = {}


## @TODO: rewrite testBagger as a test of cart.py?
## from testBagger import *
## suites['bagger'] = unittest.makeSuite(BaggerTestCase, "check_")

## suites = zdc.test.suites
##
## # merge the lists
## for item in zikebase.test.suites.keys():
##     suites[item] = zikebase.test.suites[item]

print ">> remember to turn public/admin test pages back on << "
#suites['publicpages'] = unittest.makeSuite(PublicPagesTestCase, "check_")

suites['category'] = unittest.makeSuite(CategoryTestCase, "check_")
suites['product'] = unittest.makeSuite(ProductTestCase, "check_")
suites['cart'] = unittest.makeSuite(CartTestCase, "check_")
suites['customer'] = unittest.makeSuite(CustomerTestCase, "check_")
suites['shopactor'] = unittest.makeSuite(ShopActorTestCase, "check_")
suites['store'] = unittest.makeSuite(StoreTestCase, "check_")
suites['sale'] = unittest.makeSuite(SaleTestCase, "check_")
suites['card'] = unittest.makeSuite(CardTestCase, "check_")
suites['saleEditor'] = unittest.makeSuite(SaleEditorTestCase, "check_")
suites['checkoutApp'] = unittest.makeSuite(CheckoutAppTestCase, "check_")
