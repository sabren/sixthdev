"""
zdc.Date stuff
"""
__ver__="$Id$"

import calendar
import copy
import time
import zdc

class Date:
    """
    A class to represent dates.
    """
    def __init__(self, datestr):
        """
        Construct a Date from a string representation.
        """
        s = datestr
        if type(s) != type(""):
            raise TypeError, "usage: Date(string)"
        if s == "today":
            s = "%i-%i-%i %i:%i:%i" % time.localtime(time.time())[:6]
        if " " in s:
            date, timeofday = s.split(" ")
        else:
            date, timetimeofday = s, None
        # US dates:
        if date.find("/") > -1:
            self.m, self.d, self.y = [int(x) for x in date.split("/")]
        # MySQL dates:
        else:
            self.y, self.m, self.d = [int(x) for x in date.split("-")]

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
        return "%i-%i-%i" % (self.y, self.m, self.d)

    def toUS(self):
        return "%02i/%02i/%04i" % (self.m, self.d, self.y)        

    def __cmp__(self, other):
        if isinstance(other, Date):
            return cmp([self.y, self.m, self.d], [other.y, other.m, other.d])
        elif other is zdc.TIMESTAMP:
            #@TODO: this is sort of a kludge... timestamp should
            # probably just be a sort of datetime singleton...
            # meanwhile, timestamp always wins
            return -1 
        else:
            return cmp(self, Date(other))

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
        return "Date('%s')" % self.toUS()
