#!/usr/home/sabren/bin/python

import weblib.script
import zikeshop
from zikeshop import dbc

class Cart:

    contents = []
    
    def act(self):
        action = weblib.request.get("action")
        if action=='add':
            self.do_add(weblib.request.get("code"))
        else:
            pass


    def do_add(self,code):
        if code:
            self.contents.append((code,1))
        else:
            pass


#if not weblib.sess.has_key("cart"):
#    weblib.sess["cart"] = Cart()
#
#weblib.sess["cart"].act()

print "<h1>CART PAGE</h1>"

print "(nothing happens here yet)"


print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
