"""
tests for zikeshop.Category
"""
__ver__="$Id$"

import unittest
import zikeshop
from zikeshop.test import clerk
from zikeshop import Category
from zikeshop import Product

class CategoryTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()


    def check_products(self):

        cat = Category()
        assert len(cat.products) == 0, \
               ".products should be empty list by default"
        
        self.cur.execute("DELETE FROM base_node")
        self.cur.execute("DELETE FROM shop_product")
        self.cur.execute("DELETE FROM shop_product_node")
        self.cur.execute("INSERT INTO base_node (name) values ('whatever')")
        self.cur.execute("INSERT INTO shop_product (code, name) "
                         "VALUES ('a', 'ant')")
        self.cur.execute("INSERT INTO shop_product (code, name) "
                         "VALUES ('b', 'box')")
        self.cur.execute("INSERT INTO shop_product (code, name) "
                         "VALUES ('c', 'car')")
        self.cur.execute("INSERT INTO shop_product_node (productID, nodeID) "
                         "VALUES (1, 1)")
        self.cur.execute("INSERT INTO shop_product_node (productID, nodeID) "
                         "VALUES (2, 1)")
        self.cur.execute("INSERT INTO shop_product_node (productID, nodeID) "
                         "VALUES (3, 1)")

        prods = clerk.fetch(Category, ID=1).products
        assert len(prods) == 3, \
               "wrong number of categories (%s) shown on category page" \
               % len(prods)


    def check_delete(self):
        cat = Category()
        cat.name = "stuff"

        prod = Product()
        prod.name = "ASDF"
        prod.code = "ASFD"
        cat.products << prod

        cat.save()
        
        assert len(cat.products)==1, \
               "got wrong lengths for products"
        try:
            gotError=0
            cat.delete()
        except AssertionError:
            gotError=1
            
        assert gotError, \
               "didn't get error deleting category with products"
