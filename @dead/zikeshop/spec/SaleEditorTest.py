"""
test cases for zikeshop.SaleEditor
"""
__ver__="$Id$"
import unittest

class SaleEditorTest(unittest.TestCase):
    def check_noteToSelf(self):
        raise "skip" #@TODO: revive ObjectEditor so I can make this work


##     def setUp(self):

##         cur = dbc.cursor()
##         cur.execute("DELETE FROM shop_product")

##         for i in range(4):
##             prod = Product()
##             prod.code = "PROD%i" % i
##             prod.save()

##     def check_filtering(self):
##         req = {
##             "details(+0|productID)":"1",
##             "details(+0|quantity)":"2",

##             "details(+1|productID)":"2",
##             "details(+1|quantity)":"0",

##             "details(+2|productID)":"3",
##             "details(+2|quantity)":"",

##             "details(+3|productID)":"4",
##             "details(+3|quantity)":"2",
##             }
##         ed = zikeshop.SaleEditor(zikeshop.Sale, clerk, input=req)
##         ed.act("save")
##         assert len(ed.object.details)==2, \
##                "didn't filter out 0's.. expected len=2, got len=%i" \
##                % len(ed.object.details)
