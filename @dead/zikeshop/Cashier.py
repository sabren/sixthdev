"""
a class to facilitate checkouts

$Id$
"""
import zikeshop
import zdc

class Cashier(zikeshop.ShopActor):
    """Class to manage the checkout process..."""
    #@TODO: this looks like a start of a Wizard class..    

    ## these should be in the order in which we want to require them.
    storedFields = [
        "shipAddressID",
        "billAddressID",
        #"shiptypeID",
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

        assert not self.cart.isEmpty(), \
               "Cannot check out because cart is empty."

        print "<div style='background:red'>"


    def exit(self):
        """Afterwards, store our state in the pool."""
        zikeshop.ShopActor.exit(self) # store the cart
        for item in self.storedFields:
            print "setting %s = %s <br>" % (item, getattr(self, item))
            self.pool["__cashier_" + item] = getattr(self, item)

        print "</div>"


    def nextStep(self):
        """Figure out what more we need to do, and do it."""
        
        ## first, if we need more info, ask for it:
        for item in self.storedFields:
            # check has and get so that we can assign items
            # before calling act() (as we do in public/newaddress.py)
            if not (hasattr(self, item) and getattr(self, item)):
                if self.fieldPages.get(item):
                    exec("import %s" % self.fieldPages[item])
                    exec("%s.model = self.get_model()" % self.fieldPages[item])
                    exec("%s.show()" % self.fieldPages[item])
                else:
                    raise "don't know how to get %s" % item
                break

        ## now that we know everything, do the checkout:
        if item == "receipt":
            self.act_checkout()


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
                setattr(self, item, self.input[item])

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

        ## first, save the main sale record.
        sale=zikeshop.Sale()
        sale.customerID= self.cust.ID
        sale.ship_addressID = self.shipAddressID
        sale.bill_addressID = self.billAddressID
        sale.cardID = self.cardID
        ##sale["shiptypeID = self.shiptypeID
        sale.subtotal = str(self.cart.subtotal()) # for FixedPoint
        sale.total = 0
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
        for item in self.cart.q_contents():
            r = zdc.Record(zdc.Table(zikeshop.dbc, "shop_sale_item"))
            r["saleID"] = saleID
            r["styleID"] = item["extra"]["styleID"]
            r["item"] = item["label"]
            r["quantity"] = item["quantity"]
            r["price"] = str(item["price"]) # because its a FixedPoint!
            r.save()

        ## we're done, so empty the cart.
        self.cart.empty()
        self.receipt = 1
        for item in self.storedFields:
            setattr(self, item, None)


    def get_model(self):
        class Model: pass
        res = Model()
        res.addressbook = self.cust.q_addressbook()
        res.creditcards = self.cust.q_creditcards()
        return res


