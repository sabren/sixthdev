"""
tests for zikeshop.Category
"""
__ver__="$Id$"

import unittest
import zikeshop
from zikeshop import Category
from zikeshop import Product
from arlo import MockClerk

class CategoryTest(unittest.TestCase):
    pass

    #@TODO: check non-empty category deletion in admin interface
    def DO_NOT_check_delete(self):
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
