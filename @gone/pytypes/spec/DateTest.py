"""
testDate - test cases for zdc.Date
"""
__ver__="$Id$"

import unittest
from pytypes import Date

class DateTest(unittest.TestCase):

    def check_add(self):
        assert Date("1/1/2001") + 1 == Date("1/2/2001"), \
               "normal add didn't work."
        assert Date("1/31/2001") + 1 == Date("2/1/2001"), \
               "end of month didn't work"
        assert Date("2/28/2001") + 1 == Date("3/1/2001"), \
               "end of month didn't work for february"
        assert Date("2/28/2001") + 11 == Date("3/11/2001"), \
               "end of month + big number didn't work"
        assert Date("12/31/2001") + 1 == Date("1/1/2002"), \
               "new year didn't work"
        assert Date("1/31/2001") + 31 == Date("3/3/2001"), \
               "adding more than a month didn't work"
        assert Date("1/1/2001") + 366 == Date("1/2/2002"), \
               "adding more than a year didn't work"

    def check_subtract(self):
        assert Date("1/2/2001") - 1 == Date("1/1/2001"), \
               "normal add didn't work."
        assert Date("2/1/2001") - 1 == Date("1/31/2001"), \
               "end of month didn't work"
        assert Date("3/1/2001") - 1 == Date("2/28/2001"), \
               "end of month didn't work for february"
        assert Date("1/1/2002") - 1 == Date("12/31/2001"), \
               "new year didn't work."
        assert Date("3/3/2001") - 31 == Date("1/31/2001"), \
               "subtracting more than a month didn't work"
        assert Date("1/2/2002") - 366 == Date("1/1/2001"), \
               "subtracting more than a year didn't work"
        

    def check_today(self):
        """
        temporarily set time.time() to return 10/19/2001
        and test for today.
        """
        import time
        _time = time.time
        time.time = lambda: 1003539807.89
        try:
            assert Date("today") == Date("10/19/2001"), "wrong date"
        finally:
            time.time = _time

    def check_repr(self):
        d = Date('1/1/2001')
        assert repr(d) == "Date('01/01/2001')", "wrong __repr__"

    def check_daysInMonth(self):
        assert Date("1/1/2001").daysInMonth() == 31
        assert Date("2/1/2001").daysInMonth() == 28
        assert Date("2/1/2000").daysInMonth() == 29
        
    def check_daysInYear(self):
        assert Date("1/1/1999").daysInYear() == 365
        assert Date("1/1/2000").daysInYear() == 366 # leap year
        assert Date("1/1/2001").daysInYear() == 365
