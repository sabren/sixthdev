"""
PublicApp - a base class for zikeshop's public AppActors.
"""
__ver__="$Id$"

import sixthday
import zikeshop

class PublicApp(sixthday.App):

    def __init__(self, input, cart, clerk):
        super(PublicApp, self).__init__(input)
        self.clerk = clerk
        self.cart = cart

    def enter(self):
        super(PublicApp, self).enter()
        self.cart.start()

    def exit(self):
        self.cart.purge()
        self.cart.stop()
