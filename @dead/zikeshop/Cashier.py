"""
a class to facilitate checkouts
"""
__ver__="$Id$"


##         ###############################################           ##
##         ##                                           ##           ##
##         ## WARNING: THIS IS ONE UGLY PIECE OF CODE   ##           ##
##         ##                                           ##           ##
##         ###############################################           ##


## @TODO: refactor this into a model-view-controller pattern..
## @TODO: add some better test cases..

import zikeshop
import zdc

class Cashier(zikeshop.ShopActor):
    """Class to manage the checkout process..."""
    #@TODO: this looks like a start of a Wizard class..    

    ## these should be in the order in which we want to require them.
    storedFields = [
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
        zikeshop.ShopActor.__init__(self, cart, input)

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
        for item in self.storedFields:
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
        for item in self.storedFields:
            ##print "setting %s = %s <br>" % (item, getattr(self, item))
            self.pool["__cashier_" + item] = getattr(self, item)
            
        ##print "</div>"


    def showPage(self, page):
        ## now that we know everything, do the checkout:
        if page == "receipt":
            self.act_checkout()
        else:
            exec("import %s" % self.fieldPages[page])
            exec("%s.show(self.get_model())" % self.fieldPages[page])
        


    def nextStep(self):
        """Figure out what more we need to do, and do it."""
        
        ## first, if we need more info, ask for it:
        for item in self.storedFields:
            # check has and get so that we can assign items
            # before calling act() (as we do in public/newaddress.py)
            if getattr(self, item, None) is None:
                if self.fieldPages.get(item):
                    self.showPage(item)
                else:
                    raise "don't know how to get %s" % item
                break



    def act_(self):
        """If we don't have something better to do, just show the next step"""
        self.nextStep()


    def act_update(self):
        """Update Cashier with some new information.
        This method allows you to inform the Cashier
        incrementally, if you want. Just post to the page
        with an "update" action, and it'll recognize any
        of the required fields.
        """
        for item in self.storedFields:
            if self.input.has_key(item):
                ##print "update: setting %s to %s" % (item, self.input[item])
                setattr(self, item, self.input[item])

        #@TODO: put this somewhere else.. probably in the Sale object?
        #@TODO: Sale should have a reference to a "Store" object, and
        #@TODO: "Store" should have a .hasNexus(state) for sales tax..
        
        ## calculate the sales tax
        if (self.salestax is None) and (self.billAddressID is not None):
            ## see if the store has nexus in the customer's state
            cur = zikeshop.dbc.cursor()
            cur.execute(
                """
                SELECT rate FROM shop_state
                WHERE stateCD='%s' AND storeID=%i
                """ \
                % (zikeshop.Address(ID=self.billAddressID).stateCD,
                   zikeshop.siteID)
                )

            ## if so, calculate taxes based on the data in shop_state
            if cur.rowcount:
                self.salestax = self.cart.subtotal() * \
                                (zikeshop.FixedPoint(cur.fetchone()[0])/100)

            ## otherwise, we don't charge tax..
            else:
                self.salestax = 0
        ## print "update: sales tax is now %s" % self.salestax

        ## calculate the shipping:
        if (self.shipping is None) and (self.shipAddressID is not None):
            ## find out what the merchant's address is
            fromZip = zikeshop.Store(siteID=zikeshop.siteID).address.postal
            
            ## find out what the shipping address is
            addr = zikeshop.Address(ID=self.shipAddressID)
            toZip = addr.postal
            toCountryCD = addr.countryCD
            
            ## calculate order weight by summing product weights
            ## @TODO: make totalweight a cart method
            weight = 0
            import weblib
            for item in self.cart.q_contents():
                weight = weight + \
                         (zikeshop.FixedPoint(weblib.deNone(item["extra"]
                                                            ["weight"],0))
                          * item["quantity"])

            ## UPS charges 6 grand for packages with 0 weight. :)
            if weight > 0:
                ## ask ups for the price
                import UPS
                self.shipping = zikeshop.UPS.getRate(fromZip, toZip,
                                                     toCountryCD,
                                                     weight)
            else:
                self.shipping = 0
            
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

            ## calculate how much to bill
            subtotal = self.cart.subtotal()
            total = subtotal + self.salestax + self.shipping

            ## bill the card
            if zikeshop.authorizenetmerchant:
                import payment
                theCard = zikeshop.Card(ID=self.cardID)
                pmt = payment.create("AuthorizeNet",
                                     merchant=zikeshop.authorizenetmerchant,
                                     card= theCard.number,
                                     expires= str(theCard.expMonth)+"/"+\
                                              str(theCard.expYear),
                                     )
                pmt.charge(total) # fixedpoint
                if pmt.result != payment.APPROVED:
                    raise ValueError, "charge not accepted: %s" % pmt.error

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

            #@TODO: zdc.Record seems to be relying (incorrectly) on static data
            #(otherwise, I shouldn't need the saleID temp variable)
            saleID = sale.ID

            ## Now save each item in the detail table
            ## This is NOT normalized, because we don't want the history
            ## to change if the prices or codes change.
            import zdc
            for item in self.cart.q_contents():
                r = zdc.Record(zdc.Table(zikeshop.dbc, "shop_sale_item"))
                r["saleID"] = saleID
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

                style = zikeshop.Style(ID=item["extra"]["styleID"])
                prod = zikeshop.Product(ID=style.productID)
                if rec["amount"] < prod.instock_warn:
                    #@TODO: make this template-driven
                    import weblib
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


            ## we're done, so empty the cart.
            self.cart.empty()
            self.receipt = 1
            for item in self.storedFields:
                setattr(self, item, None)

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


    def get_model(self):
        res = {}
        res["salestax"] = getattr(self, "salestax", None)
        res["shipping"] = getattr(self, "shipping", None)
        res["addressbook"] = self.cust.q_addressbook()
        res["creditcards"] = self.cust.q_creditcards()
        res["error"] = getattr(self, "error", None)
        return res


