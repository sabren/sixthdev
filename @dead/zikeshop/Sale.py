"""
zikeshop.Sale - for representing Sale events
"""
__ver__="$Id$"

import zdc
import zikeshop

class Sale(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_sale")
    _defaults = {}
    _tuples = []

    def get_shipAddress(self):
        return zikeshop.Address(ID=self.ship_addressID)

    def get_billAddress(self):
        return zikeshop.Address(ID=self.bill_addressID)

    def get_customer(self):
        return zikeshop.Customer(ID=self.customerID)

    def get_card(self):
        return zikeshop.Card(ID=self.cardID)

    def get_status(self):
        return zikeshop.Status(ID=self.statusID).status
    
    def set_shipAddress(self):
        raise "shipAddress is read only."

    def set_billAddress(self):
        raise "billAddress is read only."

    def set_customer(self):
        raise "customer is read only."

    def set_card(self):
        raise "card is read only."

    def set_status(self):
        raise "status is read only."

    def save(self):
        # @TODO: add support for timestamps to ZDC directly.
        doTS = not(self.ID)
        self.__super.save(self)
        if doTS:
            cur = self._table.dbc.cursor()
            cur.execute("UPDATE shop_sale set tsSold=now() WHERE ID=%i" \
                        % self.ID)

