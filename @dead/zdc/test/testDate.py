"""
testDate - test cases for zdc.Date
"""
__ver__="$Id$"

import unittest
import zdc
from zdc import Date

class DateTestCase(unittest.TestCase):

    def check_add(self):
        assert Date("1/1/2001") + 1 == Date("1/2/2001"), \
               "normal add didn't work."
        assert Date("1/31/2001") + 1 == Date("2/1/2001"), \
               "end of month didn't work"
        assert Date("2/28/2001") + 1 == Date("3/1/2001"), \
               "end of month didn't work for february"
        assert Date("12/31/2001") + 1 == Date("1/1/2002"), \
               "new year didn't work"

    def check_subtract(self):
        assert Date("1/2/2001") - 1 == Date("1/1/2001"), \
               "normal add didn't work."
        assert Date("2/1/2001") - 1 == Date("1/31/2001"), \
               "end of month didn't work"
        assert Date("3/1/2001") - 1 == Date("2/28/2001"), \
               "end of month didn't work for february"
        assert Date("1/1/2002") - 1 == Date("12/31/2001"), \
               "new year didn't work."
