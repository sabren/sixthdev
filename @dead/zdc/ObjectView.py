"""
ObjectView
"""
__ver__="$Id$"

import zdc
class ObjectView:
    def __init__(self,object):
        self.object = object
    def __getitem__(self, name):
        notfound = "**NOTFOUND**"
        res = getattr(self.object, name, notfound)
        if res is notfound:
            raise KeyError, name
        else:
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

