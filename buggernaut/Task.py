"""
Task: stuff to do.
"""
__ver__="$Id$"

from strongbox import *
from pytypes import *
auto = None

class Task(Strongbox):

    ID = attr(int, default=auto)
    summary = attr(str)
    detail = attr(str)    
    typeID = attr(int)
    owner = attr(str, default='michal', okay=['michal'])
    project = attr(str, default='rantelope', okay=['rantelope'])
    status = attr(str, default='open', okay=['open','closed','ignore'])
    priority = attr(str, default='medium', okay=['low','medium','high','critical'])
    risk = attr(str, default='medium', okay=['low','medium','high','unknown'])
    targetDate = attr(Date)
    createDate = attr(Date, default="today")
    hrsOrig = attr(FixedPoint)
    hrsCurr = attr(FixedPoint)
    hrsElap = attr(FixedPoint)


    def get_hrsLeft(self):
        return (self.hrsCurr or 0) - (self.hrsElap or 0)
    
