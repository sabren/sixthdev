"""
test cases for zikeshop.Product
"""
__ver__="$Id$"

import sixthday
import unittest
import zikeshop
import zikeshop.test
from pytypes import FixedPoint
from zikeshop import Product
from zikeshop.test import clerk

#@TODO: test picture attribute

class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("delete from base_node")
        self.cur.execute("delete from shop_product")
        self.cur.execute("delete from shop_product_node")

        self.cur.execute("insert into base_node (name) values ('cat1')")
        self.cur.execute("insert into base_node (name) values ('cat2')")
        self.cur.execute("insert into base_node (name) values ('cat3')")
        self.cur.execute("insert into base_node (name) values ('cat4')")
        
        self.cur.execute("INSERT INTO shop_product (code, name) "
                         "VALUES ('some01', 'something')")


    ## price, cost, and retail should all be FixedPoints ###############

    def check_price(self):
        assert isinstance(clerk.new(Product).price, FixedPoint), \
               "price is wrong type!"

    def check_cost(self):
        assert isinstance(clerk.new(Product).cost, FixedPoint), \
               "cost is wrong type!"

    def check_retail(self):
        assert isinstance(clerk.new(Product).retail, FixedPoint), \
               "retail is wrong type!"

    ## inventory checking ############################################

    def check_available(self):
        prod = clerk.new(Product)
        assert prod.available == 0, \
               "products shouldn't be available by default."

        prod.stock = 10
        assert prod.available == 10, \
               "available should be stock when nothing on hold"

        prod.hold = 5
        assert prod.available == 5, \
               "available should be stock - hold"

        style = prod.styles.new()
        style.stock = 10
        style.hold = 5
        prod.styles << style
        actual = prod.available
        assert actual == 10, \
               "available should take styles into account.. (got %s)" % actual
        
    ## styles collection #############################################
    def check_styles(self):

        prod = clerk.new(Product)
        assert len(prod.styles) == 0, \
               "shouldn't be any styles by default."
        style = prod.styles.new()
        style.code = "ABC"
        prod.styles << style
        assert len(prod.styles) == 1, \
               "didn't add style in memory.."


        prod = clerk.new(Product)
        prod.name = prod.code ="abc"
        prod.save()
        style = prod.styles.new()
        style.code = "xyz"
        prod.styles << style
        assert len(prod.styles)==1, \
               "didn't save style to db.."
        

    ## categories collection #########################################

    def check_categories(self):
        prod = clerk.new(Product)
        assert len(prod.categories)==0, \
               "categories should be empty list by default"

        nodeA = clerk.new(sixthday.Node)
        nodeA.name="abc"
        nodeA.save()
        
        nodeB = clerk.new(sixthday.Node)
        nodeB.name="xyz"
        nodeB.save()
        
        prod = clerk.new(Product)
        prod.code = 'some03'
        prod.name = 'something else'
        prod.categories = (nodeA.ID, nodeB.ID)
        prod.save()

        cats = prod.categories
        assert cats[0].name == "abc" and cats[1].name == "xyz", \
               ".categories broke."


    def check_categories_some_more(self):
        prod = clerk.new(Product)
        prod.code = 'some02'
        prod.name = 'something else'
        prod.categories = (1, 2, 3, 4)
        prod.save()

        self.cur.execute("SELECT nodeID FROM shop_product_node "
                         "WHERE productID=2 "
                         "ORDER by nodeID ")

        actual = [int(row[0]) for row in self.cur.fetchall()]
        assert actual == [1,2,3,4], \
               "Product doesn't save nodeIDs properly: %s" % str(actual)

        #@TODO: do I really need this?
        actual = prod.categories.IDs()
        assert  actual == (1, 2, 3, 4), \
               "Product.categories.IDs() screws up: %s " % str(actual)

        
        ## make sure it still works after an update:
        assert prod == prod.categories.owner, "what the?"
        assert prod.ID == 2, "???"
        prod.categories = (1, 2)
        assert prod.categories.IDs() == (1, 2)
        assert prod.ID == 2, "???"
        prod.save()
        
        self.cur.execute("SELECT nodeID FROM shop_product_node "
                         "WHERE productID=2 "
                         "ORDER BY nodeID")

        actual = self.cur.fetchall()
        assert actual == ((1,),(2,)), \
               "Product doesn't update nodeIDs properly: %s" % str(actual)

        assert prod.categories.IDs() == (1, 2), \
               "Product doesn't return nodeIDs properly after an update"



    def check_single_nodeID(self):
        prod = clerk.new(Product)
        prod.categories = 1
        prod.code =""
        try:
            prod.save()
        finally:
            assert prod.categories.IDs() == (1,), \
                   "product doesn't cope with single nodeID"


    def check_validation(self):
        prod = clerk.new(Product)
        prod.code = "some01"
        try:
            prod.save()
        except ValueError, e:
            pass
        else:
            e = None

        assert e, \
               "Didn't get ValueError on duplicate code"
