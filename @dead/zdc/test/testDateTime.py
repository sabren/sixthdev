"""
testDateTime - test cases for zdc.DateTime
"""
__ver__="$Id$"

import unittest
import zdc
from zdc import DateTime, Date

class DateTimeTestCase(unittest.TestCase):

    def check_add(self):
        assert DateTime("1/1/2001 1:23:45") + 1 == DateTime("1/2/2001 1:23:45"), \
               "normal add didn't work."
        assert DateTime("1/31/2001 23:59:59") + 1 == DateTime("2/1/2001 23:59:59"), \
               "end of month didn't work"
        assert DateTime("2/28/2001 0:0:01") + 1 == DateTime("3/1/2001 0:0:01"), \
               "end of month didn't work for february"
        assert DateTime("2/28/2001 1:2:3") + 11 == DateTime("3/11/2001 1:2:3"), \
               "end of month + big number didn't work"
        assert DateTime("12/31/2001 00:00:01") + 1 == DateTime("1/1/2002 0:0:1"), \
               "new year didn't work"
        assert DateTime("1/31/2001 12:00:00") + 31 == DateTime("3/3/2001 12:00:00"), \
               "adding more than a month didn't work"
        assert DateTime("1/1/2001 12:00:00") + 366 == DateTime("1/2/2002 12:00:00"), \
               "adding more than a year didn't work"

    def check_subtract(self):
        assert DateTime("1/2/2001") - 1 == DateTime("1/1/2001"), \
               "normal subtract didn't work."
        assert DateTime("2/1/2001") - 1 == DateTime("1/31/2001"), \
               "end of month didn't work"
        assert DateTime("3/1/2001 1:2:3") - 1 == DateTime("2/28/2001 1:2:3"), \
               "end of month didn't work for february"
        assert DateTime("1/1/2002 0:0:0") - 1 == DateTime("12/31/2001 0:0:0"), \
               "new year didn't work."
        assert DateTime("3/3/2001 23:59:59") - 31 == DateTime("1/31/2001 23:59:59"), \
               "subtracting more than a month didn't work"
        assert DateTime("1/2/2002 1:23:45") - 366 == DateTime("1/1/2001 1:23:45"), \
               "subtracting more than a year didn't work"
        
    def check_convert(self):
        assert Date("1/2/2002") == DateTime("1/2/2002 0:0:0")

    def check_comparisons(self):
        assert DateTime("06/20/1950 08:30:00") == "1950-6-20 8:30:00", "eq string compare"
        assert DateTime("01/01/2001 00:00:00") == Date("01/01/2001"), "eq comparison"
        assert Date("2001-5-1") <= DateTime("5/1/2001 0:0:0"), "le comparison"
        assert Date("5/1/2001") < DateTime("2001-5-1 00:00:01"), "lt comparison"

    def check_todayandnow(self):
        """
        temporarily set time.time() to return 10/19/2001
        and test for today.
        """
        import time
        _time = time.time
        time.time = lambda: 1003539807.89
        try:
            assert DateTime("today") == DateTime("10/19/2001 00:00:00"), "wrong date from today"
            assert DateTime("now") == DateTime("10/19/2001 21:03:27"), "wrong date or time from now"
        finally:
            time.time = _time

    def check_gets(self):
        pass

    def check_repr(self):
        d = DateTime('1/1/2001')
        assert repr(d) == "DateTime('01/01/2001 00:00:00')", "wrong __repr__ from datetime"
        d = DateTime('1/1/2001 12:34:56')
        assert repr(d) == "DateTime('01/01/2001 12:34:56')", "wrong __repr__ from datetime"

    def check_daysInMonth(self):
        assert DateTime("1/1/2001").daysInMonth() == 31
        assert DateTime("2/1/2001").daysInMonth() == 28
        assert DateTime("2/1/2000").daysInMonth() == 29
        
    def check_daysInYear(self):
        assert DateTime("1/1/1999").daysInYear() == 365
        assert DateTime("1/1/2000").daysInYear() == 366 # leap year
        assert DateTime("1/1/2001").daysInYear() == 365
