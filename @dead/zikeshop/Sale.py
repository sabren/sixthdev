"""
zikeshop.Sale - for representing Sale events
"""
__ver__="$Id$"

import zikeshop
from zikeshop import Card
from zikeshop import Contact
from pytypes import FixedPoint
from pytypes import DateTime
from strongbox import *

class Sale(Strongbox):
    customer= link(Contact)
    customerID = attr(long, default=0)
    shipAddress = link(Contact)
    ship_addressID = attr(long, default=0)
    billAddress = link(Contact)
    bill_addressID = attr(long, default=0)
    shiptypeID = attr(long, default=0)
    card = link(Card)
    cardID = attr(long, default=0)
    status = attr(str, default="new",
                  okay=["new", "cancelled", "complete", "pending"])
    tsSold = attr(DateTime, default="now")

    subtotal = attr(FixedPoint, default=0)
    shipping = attr(FixedPoint, default=0)
    salestax = attr(FixedPoint, default=0)
    adjustment = attr(FixedPoint, default=0)
    total = attr(FixedPoint, default=0)


    #@TODO: recalculate subtotal here, too...
    def get_subtotal(self):
        res = FixedPoint('0.00')
        for item in self.details:
            if item.productID:
                if item.subtotal is not None:
                    res = res + item.subtotal
        return res

    
##     def save(self):
##         # @TODO: where should this go, and when should
##         # it be updated?
##         self.total = FixedPoint('0.00') \
##                      + self.subtotal \
##                      + self.shipping \
##                      + self.salestax \
##                      + self.adjustment
##         super(Sale,self).save()
##         self.details.save()
