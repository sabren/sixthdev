"""
test cases for CheckoutApp
"""
__ver__ = "$Id$"

import unittest
import zikeshop

import sys
sys.path.append("../zikeshop/public")

class CheckoutAppTestCase(unittest.TestCase):
    
    def setUp(self):
        from zikeshop.public.checkout import CheckoutApp

        # a hack to make the storage thing work.
        import weblib
        self.sess = {}
        weblib.sess = self.sess

        # wipe the database clean.
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("DELETE FROM shop_sale")
        self.cur.execute("DELETE FROM shop_detail")

        self.app = CheckoutApp()


    def check_checkout(self):
        self.cur.execute("DELETE FROM shop_product")

        # create a product to buy
        prod = zikeshop.Product()
        prod.name='coconut'
        prod.code='coco'
        prod.siteID = zikeshop.siteID
        prod.save()

        # make a cart
        from zikeshop.public.cart import CartApp
        cart = CartApp()

        #@TODO: replace silent with next
        cart.silent = 1
        
        cart.do("add",productID=prod.ID)
        self.app.cart = cart.cart
        
        self.app.do("checkout")

        sale = zikeshop.Sale(ID=1)
        det = sale.details[0]
        
        assert det.productID == prod.ID, \
               "wrong productID saved"
        
        
