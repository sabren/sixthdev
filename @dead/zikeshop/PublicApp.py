"""
PublicApp - a base class for zikeshop's public AppActors.
"""
__ver__="$Id$"

import weblib, zikeshop

#@TODO: is this class really useful?

class PublicApp(weblib.Actor):
    __super = weblib.Actor

    def __init__(self, cart, input=None):
        self.__super.__init__(self, input)
        self.cart = cart

    def enter(self):
        self.__super.enter(self)
        self.cart.start()


    def exit(self):
        self.cart.purge()
        self.cart.stop()
