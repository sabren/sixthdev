"""
zikeshop.Sale - for representing Sale events
"""
__ver__="$Id$"

import zdc
import zikeshop
from zikeshop import Contact

class Sale(zdc.RecordObject):
    _tablename = "shop_sale"
    _links = {
        "details": [zdc.LinkSet, zikeshop.Detail, "saleID"],
        }
    _tuples = ['details']

    def _new(self):
        super(Sale,self)._new()

        self.customerID = 0
        self.ship_addressID = 0
        self.bill_addressID = 0
        self.shiptypeID = 0
        self.cardID = 0 
        self.status = "new"
        self.tsSold = zdc.TIMESTAMP
        
        self.subtotal = 0
        self.shipping = 0
        self.salestax = 0
        self.adjustment = 0
        self.total = 0


    #@TODO: replace all this crap with generic stuff from ZDC...
    def get_shipAddress(self):
        if self.ship_addressID:
            return Contact(self._ds, ID=self.ship_addressID)
        else:
            return Contact(self._ds)

    def get_billAddress(self):
        if self.bill_addressID:
            return Contact(self._ds, ID=self.bill_addressID)
        else:
            return Contact(self._ds)

    def get_customer(self):
        if self.customerID:
            return Contact(self._ds, ID=self.customerID)
        else:
            return Contact(self._ds)

    def get_card(self):
        if self.cardID:
            return zikeshop.Card(self._ds, ID=self.cardID)
        else:
            return zikeshop.Card(self._ds)
   
    def set_shipAddress(self, value):
        self.ship_addressID = value.ID

    def set_billAddress(self, value):
        self.bill_addressID = value.ID

    def set_customer(self, value):
        self.customerID = value.ID

    def set_card(self, value):
        self.cardID = value.ID


    def set_status(self, value):
        if value not in ["new", "cancelled", "complete", "pending"]:
            raise ValueError, value
        else:
            self._data['status']=value


    def get_subtotal(self):
        res = zdc.FixedPoint('0.00')
        for item in self.details:
            if item.productID:
                if item.subtotal is not None:
                    res = res + item.subtotal
        return res

    
    def save(self):
        
        # @TODO: where should this go, and when should
        # it be updated?
        self.total = zdc.FixedPoint('0.00') \
                     + self.subtotal \
                     + self.shipping \
                     + self.salestax \
                     + self.adjustment

        super(Sale,self).save()
        self.details.save()
