"""
test cases for zikeshop.SaleEditor
"""
__ver__ = "$Id$"

import unittest
import zikeshop

class SaleEditorTestCase(unittest.TestCase):

    def check_simple(self):
        "Can we save a simple sale with one detail?"        
        req = {"action":"save"}
        ed = zikeshop.SaleEditor(input=req)
        ed.act()

        assert isinstance(ed.object, zikeshop.Sale), \
               "Didn't even save a simple sale.."

        prod = zikeshop.Product()
        prod.name="X RAY GLASSES"
        prod.code="XXX"
        prod.save()

        saleID = ed.object.ID

        ed = zikeshop.SaleEditor(saleID, input=req)
        req["details(+0|productID)"]=prod.ID
        ed.input = req
        ed.act()

        assert len(ed.object.details) == 1, \
               "didn't add the detail."

        del ed
        sale = zikeshop.Sale(ID=saleID)
        assert len(sale.details) == 1, \
               "added detail to object, but not to DB"
        
