## print "content-type: text/plain"
## print 
## import sys
## sys.stderr = sys.stdout

import weblib, zikeshop, zike #base,
zikeshop.tpldir = "/usr/home/sabren/work/zikeshop/public"
weblib.auth = zike.ZikeAuth()

#@TODO: let this happen: (can't because no sess yet)
#weblib.auth.check()
#zikeshop.siteID = weblib.auth.user.siteID
