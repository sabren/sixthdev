"""
a class to facilitate checkouts
"""
__ver__="$Id$"

## @TODO: refactor this into a model-view-controller pattern..
## @TODO: add some better test cases..

#######################################################################
# 0923.2000 refactorings:

def calcSalesTax(addressID, subtotal):
    import zikeshop    

    #@TODO: put this somewhere else.. probably in the Sale object?
    #@TODO: Sale should have a reference to a "Store" object, and
    #@TODO: "Store" should have a .hasNexus(state) for sales tax..
    
    ## see if the store has nexus in the customer's state
    cur = zikeshop.dbc.cursor()
    cur.execute(
        """
        SELECT rate FROM shop_state
        WHERE stateCD='%s' AND storeID=%i
        """ \
        % (zikeshop.Address(ID=addressID).stateCD,
           zikeshop.siteID)
        )
    
    ## if so, calculate taxes based on the data in shop_state
    if cur.rowcount:
        return subtotal * \
               (zikeshop.FixedPoint(cur.fetchone()[0])/100)
        
    ## otherwise, we don't charge tax..
    else:
        return 0



def calcShipping(addr, weight):
    import zikeshop
    res = 0
    ## find out what the merchant's address is
    fromZip = zikeshop.Store(siteID=zikeshop.siteID).address.postal

    ## find out what the shipping address is
    toZip = addr.postal
    toCountryCD = addr.countryCD
    
    ## UPS charges 6 grand for packages with 0 weight. :)
    if weight > 0:
        ## ask ups for the price
        import zikeshop.UPS
        res = zikeshop.UPS.getRate(fromZip, toZip, toCountryCD, weight)

        ## it also occasionally charges 6 grand for invalid
        ## shipping options..
        if res >= 6000:
            res = 0
        
    return res


def chargeCard(theCard, amount):
    import payment, zikeshop
    
    ## bill the card
    if getattr(zikeshop, "authorizenetmerchant", None):
        import payment
        pmt = payment.create("AuthorizeNet",
                             merchant=zikeshop.authorizenetmerchant,
                             card= theCard.number,
                             expires= str(theCard.expMonth)+"/"+\
                                      str(theCard.expYear),
                             )
        pmt.charge(amount) # fixedpoint
        if pmt.result != payment.APPROVED:
            raise ValueError, "charge not accepted: %s" % pmt.error


def alertNewSale(sale):
    import zikeshop, weblib
    msg = weblib.trim(
        """
        Subject: new order.

        you have a new order in zikeshop. click here
        to see it:

        https://www.zike.net/zike/admin/zikeshop/sale.py?saleID=%i

        """ % int(sale.ID))
    zikeshop.sendmail("salebot@zike.net", zikeshop.owneremail,
                      "new order.", msg)
    zikeshop.sendmail("salebot@zike.net", "info@zike.net",
                      "new order.", msg)


#######################################################################


import zikeshop
import zdc

class Cashier(zikeshop.Wizard):
    """Class to manage the checkout process..."""
    #@TODO: this looks like a start of a Wizard class..    

    ## these should be in the order in which we want to require them.
    steps = [
        "shipAddressID",
        "billAddressID",
        "salestax",
        "shipping",
        "cardID",
        "receipt",
        "alldone"
        ]

    fieldPages = {
        "shipAddressID": "tpl_get_ship",
        "billAddressID": "tpl_get_bill",
        "cardID": "tpl_get_card",
        "receipt": "tpl_receipt",
        "alldone": "tpl_alldone",
        }


    def __init__(self, cart, cust, input=None, pool=None):
        zikeshop.Wizard.__init__(self, cart, input)

        self.cust = cust # a Customer object
        assert self.cust is not None, \
               "Cashier requires a valid Customer."

        if pool is None:
            import weblib
            try:
                self.pool = weblib.sess
            except:
                raise "if no pool given, weblib.sess must be defined"
        else:
            self.pool = pool
            

    def enter(self):
        """Before we start, fetch state from the pool (session)."""
        
        zikeshop.ShopActor.enter(self) # fetch cart info
        for item in self.steps:
            if not hasattr(self, item):
                setattr(self, item, self.pool.get("__cashier_" + item))
                ## print "setting %s to %s" % (item, getattr(self, item))

        assert not self.cart.isEmpty(), \
               "Cannot check out because cart is empty."

        self.error = "" # assume no errors...

        ##print "<div style='background:red'>"


    def exit(self):
        """Afterwards, store our state in the pool."""
        zikeshop.ShopActor.exit(self) # store the cart
        for item in self.steps:
            ##print "setting %s = %s <br>" % (item, getattr(self, item))
            self.pool["__cashier_" + item] = getattr(self, item)
            
        ##print "</div>"


    def showPage(self, page):
        if page == "receipt":
            self.act_checkout()
        else:
            zikeshop.Wizard.showPage(self, page)


    def act_update(self):
        """
        Update Cashier with some new information.  This method allows
        you to inform the Cashier incrementally, if you want. Just
        post to the page with an 'update' action, and it'll recognize
        any of the required fields.
        """
        for item in self.steps:
            if self.input.has_key(item):
                setattr(self, item, self.input[item])
        
        ## calculate the sales tax
        if (self.salestax is None) and (self.billAddressID is not None):
            self.salestax = calcSalesTax(self.billAddressID, self.cart.subtotal())

        ## calculate the shipping:
        if (self.shipping is None) and (self.shipAddressID is not None):
            self.shipping = calcShipping(zikeshop.Address(ID=self.shipAddressID),
                                         self.cart.calcWeight())
        self.nextStep()


    def act_addcard(self):
        """Add a new card to the database"""
        card = zikeshop.Card()
        card.customerID = self.cust.ID
        card.name = self.input["name"]
        card.number = self.input["number"]
        card.expMonth = self.input["expMonth"]
        card.expYear = self.input["expYear"]
        card.addressID = self.billAddressID
        card.save()

        self.cardID = card.ID
        self.nextStep()


    def act_checkout(self):
        """Records a sale in the database."""

        try:

            ## @TODO: move totalling to Sale class
            subtotal = self.cart.subtotal()
            total = subtotal + self.salestax + self.shipping

            chargeCard(zikeshop.Card(ID=self.cardID), total)

            ## now, save the main sale record.
            sale=zikeshop.Sale()
            sale.customerID= self.cust.ID
            sale.ship_addressID = self.shipAddressID
            sale.bill_addressID = self.billAddressID
            sale.cardID = self.cardID
            sale.subtotal = str(subtotal) # it's a fixedpoint
            sale.salestax = str(self.salestax)
            sale.shipping = self.shipping
            sale.total = str(total) # also a fixedpoint
            sale.statusID = zikeshop.Status(status="new").ID # mark it 'new'
            sale.siteID = zikeshop.siteID
            sale.save()

            #@TODO: better initial-timestamp support
            zikeshop.dbc.cursor().execute(
                "UPDATE shop_sale set tsSold=now() where ID=%i" % sale.ID)

            ## Now save each item in the detail table
            ## This is NOT normalized, because we don't want the history
            ## to change if the prices or codes change.
            import zdc
            for item in self.cart.q_contents():
                r = zdc.Record(zdc.Table(zikeshop.dbc, "shop_sale_item"))
                r["saleID"] = sale.ID
                r["styleID"] = item["extra"]["styleID"]
                r["item"] = item["label"]
                r["quantity"] = item["quantity"]
                r["price"] = str(item["price"]) # because its a FixedPoint!
                r.save()

                ## also: update the inventory...
                ## @TODO: handle decreasing inventory when multiple locations
                ## @TODO: move this into its own routine or whatever..
                rec = zdc.Record(zdc.Table(zikeshop.dbc, "shop_inventory"),
                                 styleID=item["extra"]["styleID"])
                rec["amount"] = rec["amount"] - item["quantity"]
                rec.save()

                import weblib
                style = zikeshop.Style(ID=item["extra"]["styleID"])
                prod = zikeshop.Product(ID=style.productID)
                if rec["amount"] < prod.instock_warn:
                    #@TODO: make this template-driven
                    msg = weblib.trim(
                        """
                        Subject: inventory alert
                        
                        Zikeshop Warning:

                        Inventory for %s [%s] {%s} has dropped below %s.
                        """ \
                        % (prod.name, prod.code, style.style, rec["amount"] ))
                    zikeshop.sendmail("inventorybot@zike.net",
                                      zikeshop.owneremail,
                                      "inventory alert",
                                      msg)
            alertNewSale(sale)
            
        except ValueError, e:
            import sys
            self.error = e
            self.showPage("cardID")
            sys.exit()

        except Exception, e:
            import weblib, traceback
            weblib.response.contentType="text/plain"
            traceback.print_exc(file=weblib.response)
            weblib.response.end()

        else:
            exec("import %s" % self.fieldPages["receipt"])
            exec("%s.show(self.get_model())" % self.fieldPages["receipt"])

            ## we're done, so empty the cart.
            self.cart.empty()
            self.receipt = 1
            for item in self.steps:
                setattr(self, item, None)

    def get_model(self):
        res = {}
        res["salestax"] = zikeshop.FixedPoint(getattr(self, "salestax", 0) or 0)
        res["shipping"] = zikeshop.FixedPoint(getattr(self, "shipping", 0) or 0)
        res["addressbook"] = self.cust.q_addressbook()
        res["creditcards"] = self.cust.q_creditcards()
        res["error"] = getattr(self, "error", None)
        res["products"] = self.cart.q_contents()
        res["adjustment"] = zikeshop.FixedPoint(0)
        res["total"] = self.cart.subtotal() + res["salestax"] + res["shipping"]
        import time
        res["date"] = time.asctime(time.localtime(time.time()))[:10] \
                      + ", " + time.asctime(time.localtime(time.time()))[-4:]
        return res
