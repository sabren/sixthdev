"""
checkout process for the cart (records the sale)
"""
__ver__="$Id$"

import zikeshop
class CheckoutApp(zikeshop.PublicApp):
    __super = zikeshop.PublicApp

    def enter(self):
        self.__super.enter(self)

        # get the customer?
        weblib.auth.check()
        self.cust = weblib.auth.user

        # internal storage device
        self.storage = weblib.sess

        # @TODO: clean this up:
        if self.cart.isEmpty():
            raise Error, "Can't check out because cart is empty."

    def act_(self):
        print "this is checkout"

    def act_set_shipping(self):
        if self.input.get('use_billing'):
            self.do("get_card")

    def act_add_card(self):
        # Add a new card to the database:
        import zikebase
        ed = zikebase.ObjectEditor(zikeshop.Card)
        ed.do("update")
        ed.object.customerID = self.cust.ID
        ed.object.save()

        # use the card for the transaction:
        self.storage['cardID'] = ed.object.ID

        #@TODO: resolve - cards with secondary billing addresses?
        self.next = "checkout"

    def act_set_card(self):
        self.storage['cardID'] = int(self.input['cardID'])
        self.next = "checkout"

    def act_get_card(self):
        import zebra, zdc
        self.consult(zdc.ObjectView(weblib.auth.user))
        zebra.show("frm_card", self.model)


    def act_show_receipt(self):
        import zebra
        self.consult({"products":[]})
        zebra.show("dsp_receipt", self.model)

    def act_checkout(self):
        sale = zikeshop.Sale()

        for item in self.cart.q_contents():
            det = sale.details.new()
            det.productID = item["extra"]["ID"]
            det.quantity = item["quantity"]
            sale.details << det
        sale.save()

        self.jumpMap={"receipt":"checkout.py?action=show_receipt"}
        self.next = ("jump", {"where":"receipt"})
        
        

if __name__=="__main__":
    CheckoutApp().act()
    
##     import weblib
##     weblib.auth.check()

##     #@TODO: consolidate all this with Cashier and replace with an Actor
##     import zikeshop
##     cart = zikeshop.Cart()
##     cash = zikeshop.Cashier(cart, weblib.auth.user)
##     cash.act()
