import sys
sys.path.extend(["/home/sabren/lib","/home/sabren/work"])

from buggernaut import *
import storage, arlo, sqlTangentCode
CLERK = arlo.Clerk(storage.MySQLStorage(sqlTangentCode.dbc),
                   {Task : "bug_task",
                    Area : "bug_area",})
