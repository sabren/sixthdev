## print "content-type: text/plain"
## print ""
## import sys; sys.stderr = sys.stdout

import zikeshop
zikeshop.siteID = 1
zikeshop.basehref = "/workshop/zikeshop/public"
weblib.auth = zikeshop.CustomerAuth()

