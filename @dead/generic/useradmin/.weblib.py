## print "content-type: text/plain"
## print 
## import sys
## sys.stderr = sys.stdout

import zikebase, zdc.drivers.DBAPI2Driver, sqlExpress
zikebase.dbc.open(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlExpress.dbc))

import weblib
weblib.auth.check()
