"""
PublicApp - a base class for zikeshop's public AppActors.
"""
__ver__="$Id$"

import weblib, zikeshop

class PublicApp(weblib.Actor):
    __super = weblib.Actor

    def __init__(self, input, cart, ds):
        self.__super.__init__(self, input)
        self.ds = ds
        self.cart = cart

    def enter(self):
        self.__super.enter(self)
        self.cart.start()

    def exit(self):
        self.cart.purge()
        self.cart.stop()
