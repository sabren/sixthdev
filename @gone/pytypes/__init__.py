from FixedPoint import *
from DateTime import *
from Date import *
from IdxDict import *

def toDate(thing):
    """
    ensures that a date is a Date object
    """
    if isinstance(thing, Date):
        return thing
    else:
        return Date(thing)
    

def toDateTime(thing):
    """
    ensures that a datetime is a DateTime object
    """
    if isinstance(thing, DateTime):
        return thing
    else:
        return DateTime(thing)
    

def dateRange(date1, date2):
    """
    returns a tuple of Date objects between two dates (inclusive)
    """
    d1 = toDate(date1)
    d2 = toDate(date2)

    d = d1
    dates = []
    while d <= d2:
        dates.append(d)
        d += 1
    
    return tuple(dates)