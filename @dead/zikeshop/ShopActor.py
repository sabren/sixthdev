
import weblib

class ShopActor(weblib.Actor):

    def __init__(self, cart, input=None):
        self.cart = cart
        weblib.Actor.__init__(self, input)


    def enter(self):
        self.cart.start()


    def exit(self):
        self.cart.purge()
        self.cart.stop()

