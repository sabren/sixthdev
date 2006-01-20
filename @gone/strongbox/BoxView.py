
# note: this was moved here from zdc. It's useful for
# zebra templates, but it's not really integrated
# with strongbox yet.

class BoxView:
    """
    Builds a view (dict/list data structure) from a Box
    """
    __ver__="$Id$"

    def __init__(self,object):
        self.object = object

    def __getitem__(self, name):
        # this used to have a try..except block, but it made it
        # very hard to debug!
        try:
            res = getattr(self.object, name)
        except AttributeError:
            raise AttributeError("couldn't read attribute '%s'" % name)
        try:
            hasLen = 1
            len(res)
        except:
            hasLen = 0
        if (hasLen) and (type(res) != str):
            lst = []
            for item in res:
                lst.append(BoxView(item))
            return lst
        else:
            return res

    def __getattr__(self, name):
        if name=="object":
            return getattr(super(BoxView, self), name)
        else:
            return getattr(self.object, name)

    def get(self, name, default=None):
        return getattr(self.object, name, default)

    def keys(self):
        return self.object.__slots__
        #@TODO: ObjectView.keys() only works with RecordObjects
        #map(lambda fld: fld.name, self.object._table.fields) \
        #return self.object.__values__.keys() \
        #       + self.object._links.keys()
               # NOTE: i was only doing the tuple thing
               #       because of zikeshop.Product

