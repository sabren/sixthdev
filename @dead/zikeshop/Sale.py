"""
zikeshop.Sale - for representing Sale events
"""
__ver__="$Id$"

import zdc
import zikeshop

class Sale(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_sale")
    _links = {
        "details": (zdc.LinkSet, zikeshop.Detail, "saleID")
        }
    _defaults = {
        "customerID": 0,
        "ship_addressID": 0,
        "bill_addressID": 0,
        "shiptypeID": 0,
        "cardID": 0,
        "status": "new",
        "siteID":0, #@TODO: remove this!
        }
    _tuples = []


    #@TODO: replace all this crap with generic stuff from ZDC...
    def get_shipAddress(self):
        return zikeshop.Address(ID=self.ship_addressID)

    def get_billAddress(self):
        return zikeshop.Address(ID=self.bill_addressID)

    def get_customer(self):
        return zikeshop.Customer(ID=self.customerID)

    def get_card(self):
        return zikeshop.Card(ID=self.cardID)
   
    def set_shipAddress(self):
        raise "shipAddress is read only."

    def set_billAddress(self):
        raise "billAddress is read only."

    def set_customer(self):
        raise "customer is read only."

    def set_card(self):
        raise "card is read only."



    def set_status(self, value):
        if value not in ["new", "cancelled", "complete", "pending"]:
            raise ValueError, value
        else:
            self._data['status']=value


    def get_subtotal(self):
        res = zikeshop.FixedPoint('0.00')
        for item in self.details:
            if item.productID:
                if item.subtotal is not None:
                    res = res + item.subtotal
        return res

    
    def addDetail(self, det):
        """
        This method adds a detail to the event.
        """
        if type(det) == type(0):
            det = zikeshop.Detail(ID=det)
        if not det in self.details:
            det.saleID = self.ID
            self.details << det

    def save(self):
        doTS = not(self.ID)
        self.__super.save(self)
        for det in self.details:
            det.saleID = self.ID
            det.save()

        # @TODO: add support for timestamps to ZDC directly.
        if doTS:
            cur = self._table.dbc.cursor()
            cur.execute("UPDATE shop_sale set tsSold=now() WHERE ID=%i" \
                        % self.ID)
