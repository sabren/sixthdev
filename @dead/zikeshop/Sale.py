"""
zikeshop.Sale - for representing Sale events
"""
__ver__="$Id$"

import zikeshop, zikebase, zdc

class Sale(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_sale")
    _links = {
        "details": [zdc.LinkSet, zikeshop.Detail, "saleID"],
        }
    _tuples = ['details']

    def _new(self):
        self.__super._new(self)

        self.customerID = 0
        self.ship_addressID = 0
        self.bill_addressID = 0
        self.shiptypeID = 0
        self.cardID = 0 
        self.status = "new"

        self.subtotal = 0
        self.shipping = 0
        self.salestax = 0
        self.adjustment = 0
        self.total = 0


    #@TODO: replace all this crap with generic stuff from ZDC...
    def get_shipAddress(self):
        if self.ship_addressID:
            return zikebase.Contact(ID=self.ship_addressID)
        else:
            return zikebase.Contact()

    def get_billAddress(self):
        if self.bill_addressID:
            return zikebase.Contact(ID=self.bill_addressID)
        else:
            return zikebase.Contact()

    def get_customer(self):
        if self.customerID:
            return zikebase.Contact(ID=self.customerID)
        else:
            return zikebase.Contact()

    def get_card(self):
        if self.cardID:
            return zikeshop.Card(ID=self.cardID)
        else:
            return zikeshop.Card()
   
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
        doTS = not(self.ID)

        # @TODO: where should this go, and when should
        # it be updated?
        self.total = zdc.FixedPoint('0.00') \
                     + self.subtotal \
                     + self.shipping \
                     + self.salestax \
                     + self.adjustment

        self.__super.save(self)
        for det in self.details:
            det.saleID = self.ID
            det.save()

        # @TODO: add support for timestamps to ZDC directly.
        if doTS:
            cur = self._table.dbc.cursor()
            cur.execute("UPDATE shop_sale set tsSold=now() WHERE ID=%i" \
                        % self.ID)
