import sys
#print "content-type: text/plain"
#print
#sys.stderr = sys.stdout

sys.path.extend(["/home/blaze/lib"])

from buggernaut import *
import storage, arlo, sqlBuggernaut
CLERK = arlo.Clerk(storage.MySQLStorage(sqlBuggernaut.connect()),
                   arlo.Schema({
                       Task : "bug_task",
                       Area : "bug_area",
                   }))
