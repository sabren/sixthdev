"""
test cases for zikeshop.SaleEditor
"""
__ver__="$Id$"
import unittest
import zikeshop

class SaleEditorTestCase(unittest.TestCase):

    def setUp(self):
        from zikeshop.test import dbc
        self.ds = dbc
        cur = dbc.cursor()
        cur.execute("DELETE FROM shop_product")

        for i in range(4):
            prod = zikeshop.Product(self.ds)
            prod.code = "PROD%i" % i
            prod.save()

    def check_filtering(self):
        req = {
            "details(+0|productID)":"1",
            "details(+0|quantity)":"2",

            "details(+1|productID)":"2",
            "details(+1|quantity)":"0",

            "details(+2|productID)":"3",
            "details(+2|quantity)":"",

            "details(+3|productID)":"4",
            "details(+3|quantity)":"2",
            }
        ed = zikeshop.SaleEditor(zikeshop.Sale, self.ds, input=req)
        ed.act("save")
        assert len(ed.object.details)==2, \
               "didn't filter out 0's.. expected len=2, got len=%i" \
               % len(ed.object.details)
