"""
unit tests for lectet.Wildcard
"""
__ver__="$Id$"

import unittest, lecter.Wildcard

class WildcardTestCase(unittest.TestCase):

    def check_cmp(self):
        wc = lecter.Wildcard.Wildcard()
        for val in ["a",3,"SADFASDF"]:
            assert wc==val, "didn't match %s" % string(va)

    def check_tuples(self):
        wc = lecter.Wildcard.Wildcard()
        assert (wc, 2, 3) == (1, 2, 3), \
               "doesn't match in a tuple"
