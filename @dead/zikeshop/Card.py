

import zdc
import zikeshop

class Card(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_card")
    _defaults = {}

    def getEditableAttrs(self):
        #@TODO: getEditableAttrs should return a tuple, if anything
        return self.__super.getEditableAttrs(self) + ['masked']

    def get_masked(self):
        return ("x" * (len(self.number)-4)) + self.number[-4:]
