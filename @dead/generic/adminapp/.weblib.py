## print "content-type: text/plain"
## print 
## import sys
## sys.stderr = sys.stdout

import zikebase, zdc.drivers.DBAPI2Driver, sqlPlan
zikebase.dbc.open(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlPlan.dbc))

## authentication ###
#import weblib
#weblib.auth.check()
