"""
(credit) Card object for zikeshop
"""
__ver__="$Id$"

import zdc
import zikeshop

class Card(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_card")
    __members__= [
        'masked'
        ]

    def get_masked(self):
        return ("x" * (len(self.number)-4)) + self.number[-4:]
