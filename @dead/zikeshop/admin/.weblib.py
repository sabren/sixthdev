## print "content-type: text/plain"
## print 
## import sys
## sys.stderr = sys.stdout

import zikebase, zdc, sqlTest
zikebase.dbc.open(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlTest.dbc))

import zikeshop
zikeshop.tpldir = "/usr/home/sabren/work/zikeshop/public/"
