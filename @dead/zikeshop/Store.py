"""
class to represent the actual store
"""
__ver__="$Id$"

import zdc
import zikeshop

class Store(zdc.Object): #(zdc.RecordObject):

    ## zdc init  ##########################################

    def __init__(self, clerk):
        super(Store, self).__init__()
        self.__dict__['clerk'] = clerk

    def _init(self):
        self._onHold = {}
        self._address = None


    ## collections ########################################

    def get_products(self):
        #@TODO: get rid of this?
        #@TODO: improper use of clerk.store!
        return self.clerk.store.select(zikeshop.Product,
                              "class='product'",
                              orderBy="code")

    ## calculations #######################################

    def calcShipping(self, addr, weight):
        return 0

##     def calcShipping(self, addr, weight):
##         import zikeshop
##         res = 0
##         ## find out what the merchant's address is
##         fromZip = self.address.postal

##         ## find out what the shipping address is
##         toZip = addr.postal
##         toCountryCD = addr.countryCD

##         ## UPS charges 6 grand for packages with 0 weight. :)
##         if weight > 0:
##             ## ask ups for the price
##             import zikeshop.UPS
##             res = zdc.FixedPoint(
##                 zikeshop.UPS.getRate(fromZip, toZip, toCountryCD, weight))

##             ## it also occasionally charges 6 grand for invalid
##             ## shipping options..
##             if res >= 6000:
##                 res = 0
##         return res


    def calcSalesTax(self, addr, amount):
        import zikeshop
        if self.hasNexus(addr.stateCD):
            state = zikeshop.State(self._ds, CD=addr.stateCD)
            return (state.salestax * amount) / 100
        else:
            return 0


    def hasNexus(self, stateCD):
        #@TODO: allow multi-state nexus
        #for item in self._locations:
        #    if item.stateCD == stateCD:
        #        return 1
        #@TODO: this is a really crappy function, since it's duplicated above.
        try:
            s = zikeshop.State(self._ds, CD=stateCD)
            foundIt = 1
        except:
            foundIt = 0
        return foundIt

