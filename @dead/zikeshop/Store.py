"""
class to represent the actual store
"""
__ver__="$Id$"

import zdc, zikeshop, zikebase

class Store(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_store")

    ## zdc init  ##########################################

    def _init(self):
        self._onHold = {}
        self._address = None


    ## magic zdc properties ###############################

    def set_address(self, value):
        self._address = value
        
    def get_address(self):
        # @TODO: allow getting the address without saving first
        if self._address:
            return self._address
        elif self.addressID:
            return zikebase.Contact(ID=self.addressID)
        else:
            return zikebase.Contact()


    ## collections ########################################

    def get_products(self):
        #@TODO: get rid of this?
        return zikeshop.dbc.select(zikeshop.Product._table.name, "class='product'", orderBy="code")

    ## calculations #######################################

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
            res = zdc.FixedPoint(
                zikeshop.UPS.getRate(fromZip, toZip, toCountryCD, weight))

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
        #@TODO: allow multi-state nexus
        #for item in self._locations:
        #    if item.stateCD == stateCD:
        #        return 1
        if stateCD and (self.address.stateCD == stateCD):
            return 1

