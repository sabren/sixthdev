"""
PublicApp - a base class for zikeshop's public AppActors.
"""

import zikebase, zikeshop
zikebase.load("AppActor")

class PublicApp(zikebase.AppActor):
    __super = zikebase.AppActor

    def __init__(self, cart=None, input=None):
        self.__super.__init__(self, input)
        if cart:
            self.cart = cart
        else:
            self.cart = zikeshop.Cart()


    def enter(self):
        self.cart.start()


    def exit(self):
        self.cart.purge()
        self.cart.stop()
