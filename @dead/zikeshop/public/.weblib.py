#print "content-type: text/plain\n\n"
#import sys; sys.stderr = sys.stdout

import zikeshop, weblib
zikeshop.basehref = "/zikeshop/public"
zikeshop.checkouturl = "checkout.py?auth_logout_flag=1"
zikeshop.authorizenetmerchant = None #"aggressive"
zikeshop.owneremail = "terrys_weblib_py@sabren.com" # for cashier.act_checkout
weblib.auth = zikeshop.CustomerAuth()

