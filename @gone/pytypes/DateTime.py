"""
zdc.DateTime stuff
"""
__ver__="$Id$"

import calendar
import copy
import time
import pytypes

class DateTime:
    """
    A class to represent datetimes.
    """
    def __init__(self, datestr):
        """
        Construct a DateTime from a string representation.
        """
        s = datestr
        if type(s) != type(""):
            raise TypeError, "usage: DateTime(string)"
        if s == "now":
            s = "%04i-%02i-%02i %02i:%02i:%02i" % time.localtime(time.time())[:6]
        elif s == "today":
            s = "%i-%i-%i 00:00:00" % time.localtime(time.time())[:3]
        if " " in s:
            date, timeofday = s.split(" ")
        else:
            date, timeofday = s, None
        # US datetimes:
        if date.find("/") > -1:
            self.m, self.d, self.y = [int(x) for x in date.split("/")]
        # MySQL datetimes:
        else:
            self.y, self.m, self.d = [int(x) for x in date.split("-")]
        if not timeofday:
            self.hh = self.mm = self.ss = 0
        else:
            self.hh, self.mm, self.ss = [int(x) for x in timeofday.split(":")]

    def daysInMonth(self):
        """
        returns number of days in the month
        """
        return calendar.monthrange(self.y, self.m)[1]

    def daysInYear(self):
        from operator import add
        return reduce(add,
                      [calendar.monthrange(self.y, m+1)[1] for m in range(12)])
        
    def toSQL(self):
        return "%i-%i-%i %i:%i:%i" % (self.y, self.m, self.d, self.hh, self.mm, self.ss)

    def toUS(self):
        return "%02i/%02i/%04i %02i:%02i:%02i" % (self.m, self.d, self.y, self.hh, self.mm, self.ss)        

    def __cmp__(self, other):
        if isinstance(other, DateTime):
            return cmp([self.y, self.m, self.d, self.hh, self.mm, self.ss],
                       [other.y, other.m, other.d,
                        other.hh, other.mm, other.ss])
        elif isinstance(other, pytypes.Date):
            return cmp([self.y, self.m, self.d, self.hh, self.mm, self.ss],
                        [other.y, other.m, other.d, 0, 0, 0])
        else:
            return cmp(self, DateTime(other))

    def __add__(self, days):
        """
        Add a certain number of days, accounting for months, etc..
        """
        res = copy.deepcopy(self)
        res.d += days
        while res.d > res.daysInMonth():
            res.d = res.d - res.daysInMonth()
            res.m += 1
            if res.m > 12:
                res.m = 1
                res.y += 1
        return res
    
    def __sub__(self, days):
        """
        same as __add__, but in reverse..
        """
        res = copy.deepcopy(self)
        res.d -= days
        while res.d < 1:
            res.m -= 1
            if res.m < 1:
                res.m = 12
                res.y -= 1
            res.d += res.daysInMonth()
        return res

    def __str__(self):
        return self.toSQL()

    def __repr__(self):
        return "DateTime('%s')" % self.toUS()
