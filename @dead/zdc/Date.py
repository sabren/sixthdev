"""
zdc.Date stuff
"""
__ver__="$Id$"

class Date:
    """
    A class to represent dates.
    """
    def __init__(self, datestr):
        if " " in datestr:
            date, time = datestr.split(" ")
        else:
            date, time = datestr, None
        # US dates:
        if date.find("/") > -1:
            self.m, self.d, self.y = [int(x) for x in date.split("/")]
        # MySQL dates:
        else:
            self.y, self.m, self.d = [int(x) for x in date.split("-")]

    def __str__(self):
        return self.toSQL()

    def toSQL(self):
        return "%i-%i-%i" % (self.y, self.m, self.d)

    def __cmp__(self, other):
        if isinstance(other, Date):
            return cmp([self.y, self.m, self.d], [other.y, other.m, other.d])
        else:
            return cmp(str(self), str(Date(other)))

