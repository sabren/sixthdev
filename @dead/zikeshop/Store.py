"""
class to represent the actual store
"""
__ver__="$Id$"

import zdc
import zikeshop

class Store(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_store")

    ## zdc init  ##########################################

    def _init(self):
        self._locations = []
        self._onHold = {}


    ## magic zdc properties ###############################
        
    def get_address(self):
        # @TODO: allow getting the address without saving first
        return zikeshop.Address(ID=self.addressID)


    ## collections ########################################
    def addLocation(self, loc):
        if loc not in self._locations:
            self._locations.append(loc)


    ## calculations #######################################

    def calcInventory(self, prod):
        res = 0
        for loc in self._locations:
            res = res + loc.calcInventory(prod)
        return res

    
    def calcAvailable(self, prod):
        return self.calcInventory(prod) - self._onHold.get(prod, 0)


    def calcShipping(self, addr, weight):
        import zikeshop
        res = 0
        ## find out what the merchant's address is
        fromZip = self.address.postal

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


    def calcSalesTax(self, addr, amount):
        import zikeshop
        if self.hasNexus(addr.stateCD):
            state = zikeshop.State(CD=addr.stateCD)
            return (state.salestax * amount) / 100
        else:
            return 0


    def hasNexus(self, stateCD):
        for item in self._locations:
            if item.stateCD == stateCD:
                return 1


    ## other routines #########################################

    def hold(self, prod, amount):
        """
        Put a certain amount of inventory on hold.
        Eg, when someone adds it to their cart.
        """
        #@TODO: check availability
        if self._onHold.has_key(prod):
            self._onHold[prod] = self._onHold[prod] + amount
        else:
            self._onHold[prod] = amount



    ## these two factory methods return new events and sales
    ## use them instead of just creating objects to make
    ## sure that the links work correctly.

    def newEvent(self):
        event = zikeshop.Event()
        #@TODO: make this read "event.store = self"
        event.storeID = self.ID
        return event

    def newSale(self):
        sale = zikeshop.Sale()
        sale.saleID = self.ID
        return sale
