"""
Locations (addresses that contain inventory)
"""
__ver__="$Id$"
import zdc
import zikeshop


class Location(zikeshop.Address):
    __super = zikeshop.Address
    _table = zdc.Table(zikeshop.dbc, "shop_location")
    _defaults = {'name':''}

    def _init(self):
        self._inventory = {}

    def incInventory(self, prod, quant):
        # if this were python 2.0, I'd just say...
        # self._inventory.setdefault(prod, 0) += quant
        # .. but oh well.. :)
        if self._inventory.has_key(prod):
            self._inventory[prod] = self._inventory[prod] + quant
        else:
            self._inventory[prod] = quant

    def decInventory(self, prod, quant):
        self.incInventory(prod, -quant) # aint I a stinker? :)


    def calcInventory(self, prod):
        return self._inventory.get(prod, 0)

    def delete(self):
        cur = self._table.dbc.cursor()
        cur.execute("DELETE FROM shop_inventory WHERE locationID=%s" % self.ID)
        zdc.RecordObject.delete(self)
        
