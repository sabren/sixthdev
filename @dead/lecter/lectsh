"""
lecter shell
"""
__ver__="$Id$"

import lecter
while 1:
    try:
        lecter.Shell().cmdloop()
    except lecter.Reset:
        print "environment reset."
        reload(lecter)
        continue
