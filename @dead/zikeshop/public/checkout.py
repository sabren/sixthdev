"""
checkout process for the cart (records the sale)
"""
__ver__="$Id$"

import zikeshop
import weblib

class CheckoutApp(zikeshop.PublicApp):
    __super = zikeshop.PublicApp

    def __init__(self, cart=None, input=None):
        self.__super.__init__(self, cart, input)

        # internal data:
        #@TODO: why  won't weblib store a Sale object in the session?
        if not weblib.sess.has_key("checkout_data"):
            weblib.sess["checkout_data"] = {}
        self.data = weblib.sess["checkout_data"]
          
        
    ## Actor methods ############################
    
    def enter(self):
        self.__super.enter(self)

        # @TODO: clean this up:
        # once they checkout (or before they go shopping,
        # all they can do is view their latest receipt..
        if self.input.get("action") != "show_receipt":
            assert not self.cart.isEmpty(), \
                   "Can't check out because cart is empty."

    def exit(self):
        self.__super.exit(self)
        if self.data:
            weblib.sess["checkout_data"] = self.data

    def act_(self):
        self.next = 'get_billing'

    ## other stuff ... ###################################

    def checkShipToBilling(self):
        if self.input.get('shipToBilling'):
            self.data['ship_addressID']=self.data['bill_addressID']
            
    def act_get_billing(self,refresh=1):
        import zebra, zdc, zikebase
        if refresh:
            self.consult(zdc.ObjectView(zikebase.Contact()))
        zebra.show('frm_billing', self.model)

    def act_set_billing(self):
        self.data['bill_addressID']=self.input['addressID']
        self.checkShipToBilling()
        if self.data.get('ship_addressID'):
            self.redirect(action='get_card')
        else:
            self.redirect(action='get_shipping')

    def act_get_shipping(self, refresh=1):
        import zebra, zdc, zikebase
        if refresh:
            self.consult(zdc.ObjectView(zikebase.Contact()))
        zebra.show('frm_shipping', self.model)

    def act_set_shipping(self):
        self.checkShipToBilling()
        self.redirect(action='get_card')

    def act_add_address(self):
        #@TODO: this is a lot like userapp..
        import zikebase
        zikebase.load("Contact")
        context = self.input.get('context','bill')
        errs = []
        required=[
            ('fname','first name'),
            ('lname','last name'),
            ('email','email'),
            ('address1','address'),
            ('city','city'),
            ('postal','ZIP/postal code')]
        for item in required:
            if not self.input.get(item[0],""):
                errs.append("The '%s' field is required." % item[1])
        if (self.input.get("countryCD")=="US") and not self.input.get("stateCD"):
            errs.append("A state is required for US orders")
        try:
            ed = zikebase.ObjectEditor(zikebase.Contact)
            ed.do("update")
            #@TODO: should let you edit data already there (eg, BACK button)
            ed.object.save()
        except ValueError, err:
            errorMsg = ""
            errs = errs + err[0]
        if errs:
            self.model["errors"] = map(lambda e: {"error":e}, errs)
            if context=='bill':
                self.act_get_billing(0) # don't refresh data
            else:
                self.act_get_shipping(0) # don't refresh data
        else:
            if context=='bill':
                self.data['bill_addressID']=ed.object.ID
                if self.input.get('shipToBilling'):
                    self.data['ship_addressID']=self.data['bill_addressID']
                    self.redirect(action='get_card')
                else:
                    self.redirect(action='get_shipping')
            elif context=='ship':
                self.data['ship_addressID']=ed.object.ID
                self.redirect(action='get_card')

    def act_add_card(self):
        # Add a new card to the database:
        import zikebase
        try:
            ed = zikebase.ObjectEditor(zikeshop.Card)
            ed.do("save")
            # use the card for the transaction:
            self.data['cardID'] = ed.object.ID
            #@TODO: resolve - cards with secondary billing addresses?
            self.redirect(action="checkout")
        except ValueError, e:
            self.model["error"] = e[0][0] # e is a LoL 
            self.redirect(action = "get_card")

    def act_set_card(self):
        self.data['cardID'] = int(self.input['cardID'])
        self.redirect(action = "checkout")

    def act_get_card(self):
        import zebra, zdc, zikebase
        addr = zikebase.Contact(ID=self.data["bill_addressID"])
        self.model["number"]=""
        self.model["name"]=addr.fname + " " + addr.lname
        zebra.show("frm_card", self.model)


    def act_show_receipt(self):
        assert self.data.get("saleID"), \
               "No receipt to show."

        import zebra, zdc
        sale = zikeshop.Sale(ID=self.data['saleID'])
        self.consult(zdc.ObjectView(sale))
        zebra.show("dsp_receipt", self.model)

        # clear the session info:
        self.cart.empty()
        # but remember the last sale in case they refresh..
        self.data={"saleID":self.data["saleID"]}


    def act_checkout(self):
        sale = zikeshop.Sale()
        shop = zikeshop.Store()

        #@TODO: update test suite to ensure cardID <> 0 if it shouldn't be.
        sale.cardID = self.data.get('cardID', 0)
        sale.bill_addressID = self.data.get('bill_addressID', 0)
        sale.ship_addressID = self.data.get('ship_addressID', 0)
        
        for item in self.cart.q_contents():
            det = sale.details.new()
            det.productID = item["extra"]["ID"]
            det.quantity = item["quantity"]

            # @TODO: make updating .hold a transaction AND put in Sale..
            # @TODO: in fact, need to cleanly separate ordering + fufulliment
            # @TODO: some products don't need .hold (eg, downloads)
            prod = det.product
            prod.hold = prod.hold + det.quantity
            prod.save()              

            sale.details << det
            
        import zdc
        sale.tsSold = zdc.TIMESTAMP
        sale.salestax = shop.calcSalesTax(sale.shipAddress, sale.subtotal)
        sale.shipping = shop.calcShipping(sale.billAddress,
                                          self.cart.calcWeight())
        sale.save()
        self.data['saleID'] = sale.ID

        # send the receipt ---- @TODO: clean this up!!!
        if getattr(zikeshop, "SEND_EMAIL",0):
            import zebra, zikebase
            model = {}
            view = zdc.ObjectView(sale)
            for item in view.keys():
                model[item] = view[item]  # ICK!
            model["owner_email"] = getattr(zikeshop,"owner_email")
            model["customer_email"] = sale.billAddress.email
            zikebase.sendmail(zebra.fetch("eml_receipt", model))
            zikebase.sendmail(zebra.fetch("eml_notify",  model))

        self.redirect("checkout.py?action=show_receipt")
        
        
if __name__=="__main__":
    CheckoutApp().act()
