"""
testDBAPI2Driver.py
"""
__ver__="$Id$"

import unittest
import zdc, zdc.test

class DBAPI2DriverTestCase(unittest.TestCase):

    def check_quotes(self):
        table = zdc.Table(zdc.test.dbc, "test_fish")
        assert table.driver._sqlQuote(table, table.fields["fish"], "foo'fish") \
               == "'foo\\'fish'", \
               "quoting failed for STRING"
        assert table.driver._sqlQuote(table, table.fields["ID"], 0) == "0",\
               "quotes failed for NUMBER"
        # @TODO: test BINARY .. but what should it do?


