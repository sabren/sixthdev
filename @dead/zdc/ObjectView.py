"""
ObjectView
"""
__ver__="$Id$"

import zdc
class ObjectView:

    def __init__(self,object):
        self.object = object

    def __getitem__(self, name):
        # this used to have a try..except block, but it made it
        # very hard to debug!
        res = getattr(self.object, name)
        if (type(res) == type([])) or isinstance(res, zdc.LinkSet):
            lst = []
            for item in res:
                lst.append(zdc.ObjectView(item))
            return lst
        else:
            return res

    def get(self, name, default=None):
        return getattr(self.object, name, default)

    def keys(self):
        #@TODO: ObjectView.keys() only works with RecordObjects
        #map(lambda fld: fld.name, self.object._table.fields) \
        return self.object.getEditableAttrs() \
               + self.object._links.keys() \
               + self.object._tuples #@TODO: get rid of _tuples!!!
               # NOTE: i was only doing the tuple thing
               #       because of zikeshop.Product

