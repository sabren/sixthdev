#print "content-type: text/plain"
#print ""
#import sys; sys.stderr = sys.stdout

import zikeshop
zikeshop.siteID = 1
zikeshop.basehref = "/zikeshop/public"
zikeshop.checkouturl = "checkout.py?auth_logout_flag=1"
zikeshop.authorizenetmerchant = "aggressive"
zikeshop.owneremail = "terrys_weblib_py@sabren.com" # for cashier.act_checkout
weblib.auth = zikeshop.CustomerAuth()

