"""
test cases for various utility functions in ZDC
"""
__ver__="$Id$"

import unittest, zdc

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

