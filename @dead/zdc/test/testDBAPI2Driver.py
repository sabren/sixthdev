"""
testDBAPI2Driver.py
"""
__ver__="$Id$"

import unittest
import zdc, zdc.test

class DBAPI2DriverTestCase(unittest.TestCase):

    def check_quotes(self):
        #@TODO: clean up this sickening lack of encapsulation :)
        table = zdc.Table(zdc.test.dbc, "test_fish")
        assert table.dbc.source._sqlQuote(table.name, "fish", "foo'fish") \
               == "'foo\\'fish'", \
               "quoting failed for STRING"
        assert table.dbc.source._sqlQuote(table.name, "ID", 0) == "0",\
               "quotes failed for NUMBER"
        # @TODO: test BINARY .. but what should it do?


