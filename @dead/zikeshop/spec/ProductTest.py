"""
test cases for zikeshop.Product
"""
__ver__="$Id$"

import unittest
import zikeshop
import zikeshop.test
import zikebase
import zdc

class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("delete from base_node")
        self.cur.execute("delete from shop_product")
        self.cur.execute("delete from shop_product_node")
        
        self.cur.execute("INSERT INTO shop_product (code, name) "
                         "VALUES ('some01', 'something')")


    ## price, cost, and retail should all be FixedPoints ###############

    def check_price(self):
        assert isinstance(zikeshop.Product().price, zdc.FixedPoint), \
               "price is wrong type!"

    def check_cost(self):
        assert isinstance(zikeshop.Product().cost, zdc.FixedPoint), \
               "cost is wrong type!"

    def check_retail(self):
        assert isinstance(zikeshop.Product().retail, zdc.FixedPoint), \
               "retail is wrong type!"


    ## categories collection #########################################

    def check_categories(self):
        prod = zikeshop.Product()
        assert prod.categories == [], \
               "categories should be empty list by default"

        node = zikebase.Node()
        node.name="abc"
        node.save()
        node = zikebase.Node()
        node.name="xyz"
        node.save()
        
        prod = zikeshop.Product()
        prod.code = 'some03'
        prod.name = 'something else'
        prod.nodeIDs = (1, 2)
        prod.save()

        cats = prod.categories
        assert cats[0].name == "abc" and cats[1].name == "xyz", \
               ".categories broke."


    def check_nodeIDs(self):
        prod = zikeshop.Product()
        prod.code = 'some02'
        prod.name = 'something else'
        prod.nodeIDs = (1, 2, 3, 4)
        prod.save()

        self.cur.execute("SELECT nodeID FROM shop_product_node "
                         "WHERE productID=2 "
                         "ORDER by nodeID ")

        assert self.cur.fetchall() == [(1,),(2,),(3,),(4,)], \
               "Product doesn't save nodeIDs properly"

        assert prod.nodeIDs == (1, 2, 3, 4), \
               "Product doesn't return nodeIDs properly"

        
        ## make sure it still works after an update:

        prod.nodeIDs = (1, 2)
        prod.save()
        
        self.cur.execute("SELECT nodeID FROM shop_product_node "
                         "WHERE productID=2 "
                         "ORDER BY nodeID")

        assert self.cur.fetchall() == [(1,),(2,)], \
               "Product doesn't update nodeIDs properly"

        assert prod.nodeIDs == (1, 2), \
               "Product doesn't return nodeIDs properly after an update"



    def check_single_nodeID(self):
        prod = zikeshop.Product()
        prod.nodeIDs = 1
        prod.code =""
        try:
            prod.save()
        finally:
            assert prod.nodeIDs == (1,), \
                   "product doesn't cope with single nodeID"


    def check_validation(self):
        prod = zikeshop.Product()
        prod.code = "some01"
        try:
            prod.save()
        except ValueError, e:
            pass
        else:
            e = None

        assert e, \
               "Didn't get ValueError on duplicate code"
        

