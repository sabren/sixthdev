"""
test cases for various utility functions in ZDC
"""
__ver__="$Id$"

import unittest
import zdc

class FunctionsTestCase(unittest.TestCase):

    def check_viewToXML(self):
        # empty view:
        actual = zdc.viewToXML([])
        assert actual=="<list></list>", \
               "got wrong item with emtpy list: %s" % actual

        # simple view:
        view = [{"name":"fred"}]
        actual = zdc.viewToXML(view, "user", "users")
        assert actual=='<users><user name="fred"/></users>', \
               "wrong simple view: %s" % actual


    def check_dateRange(self):
        range = zdc.dateRange("1/1/2001", "1/10/2001")
        assert len(range) == len([1,2,3,4,5,6,7,8,9,10]), "wrong length"


    def check_toDate(self):
        assert isinstance(zdc.toDate("1/1/2001"), zdc.Date)
        assert isinstance(zdc.toDate(zdc.toDate("1/1/2001")), zdc.Date)
