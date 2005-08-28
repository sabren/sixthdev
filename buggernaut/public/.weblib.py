import sys
#print "content-type: text/plain"
#print 
#sys.stderr = sys.stdout


sys.path.extend(["/home/blaze/lib"])
from buggernaut.sqlBuggernaut import connect
dbc = connect()
from strongbox import *

class Story(Strongbox):
    ID = attr(int)
    summary = attr(str)
    detail = attr(str)
    area = attr(str)
    type = attr(str, default='story')
    target = attr(str, default='new')
    status = attr(str, default='devel')
    risk = attr(int, okay=range(1,10))
    worth = attr(int, okay=range(1,10))
    hrsOrig = attr(int)
    hrsCurr = attr(int)
    hrsElapsed = attr(int)

from buggernaut import Task

import arlo, storage

dbmap = arlo.Schema({
    #Story: "plan_story",
    Task: "bug_task",
    })
CLERK = arlo.Clerk(storage.MySQLStorage(dbc), dbmap)

