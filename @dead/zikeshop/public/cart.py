
import weblib
import zikeshop
from zikeshop import dbc

class Cart:

    count = 0
    contents = []

    def __init__(self):
        
        assert Cart.count == 0, "There can be only one cart."
        Cart.count = Cart.count + 1

        
    def start(self):
        if weblib.sess.has_key("__cart"):
            self.contents = weblib.sess["__cart"]
        
    
    def act(self):
        action = weblib.request.get("action")
        if action=='add':
            self.add(weblib.request.get("code"),
                     weblib.request.get("opts"),
                     weblib.request.get("amt"))
        else:
            pass


    def add(self,code,opts=None,amt=None):
        if code:
            if amt is None:
                amt = 1

            # if the item is already in the cart with the
            # same options, just increase the amount..
            for item in self.contents:
                if (code == item[0]) and (opts==item[1]):
                    item[2] = item[2] + amt
                    return
            
            # if we're still here, just add it in
            self.contents.append([code,opts,amt])
        else:
            pass # nothing to add


    def stop(self):
        weblib.sess["__cart"] = self.contents



cart = Cart()
cart.start()
cart.act()
cart.stop()

print "<h1>Cart Page</h1>"

print "<h4>contents of cart:</h4>"
print cart.contents


print "<h4>contents of sess:</h4>"
print weblib.sess.keys()

print "<hr>"
print "zikeshop alpha (c)2000 zike interactive, inc"
