"""
test cases for ShopApp
"""
__ver__ = "$Id$"

import unittest
import zikeshop
import sys, os
from zikeshop.public.shop import ShopApp
from zikeshop.test import clerk

class ShopAppTestCase(unittest.TestCase):
    
    def setUp(self):

        # a hack to make the storage thing work.
        import weblib
        self.sess = {}
        weblib.sess = self.sess

        self.REQ = weblib.Request()
        self.app = ShopApp(self.REQ, zikeshop.Cart({}), clerk)
        self.cwd = os.getcwd()
        os.chdir("public")

        self.app.enter()
        
    def tearDown(self):
        os.chdir(self.cwd)
        
    def check_show_category(self):
        self.app.do("show_category")
        #@TODO: put some assertions in here!
        #@TODO: what if category doesn't exist?

    def check_show_product(self):
        from zikeshop.test import fakedata
        fakedata.load()
        self.app.do("show_product", input={"code":"GAM00"})
        #@TODO: put some assertions in here!
        #@TODO: what if product doesn't exist?
