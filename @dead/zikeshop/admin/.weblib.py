## print "content-type: text/plain"
## print 
## import sys
## sys.stderr = sys.stdout

import weblib, zikeshop, zike #base,
zikeshop.tpldir = "/usr/home/sabren/work/zikeshop/public"
weblib.auth = zike.ZikeAuth()
#@TODO: allow weblib.auth.check() in .weblib.py (right now, it shows but then shows the page)
