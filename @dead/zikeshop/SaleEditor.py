"""
SaleEditor - an ObjectEditor with special magic for sales.
"""
__ver__="$Id$"

import zikebase
zikebase.load("ObjectEditor")

class SaleEditor(zikebase.ObjectEditor):
    __super = zikebase.ObjectEditor
    
    def mergeCollections(self):
        """
        overrides ObjectEditor.mergeCollections
        to filter out lines that have no quantity..
        This is used on the new sale admin page.
        """
        for fld in self._newData.keys():
            for i in self._newData[fld].keys():
                if (fld == "details") \
                   and self._newData[fld][i].quantity in ("","0"):
                    continue
                getattr(self.object, fld) << self._newData[fld][i]


