
from arlo import LinkInjector
from pytypes import IdxDict
from strongbox import attr

class ClerkError(Exception): pass


class Clerk:
    def __init__(self, storage, dbmap=None):
        self.storage = storage
        self.dbmap = dbmap or {}

    def _unmap_class(self, klass):
        if klass in self.dbmap:
            return self.dbmap[klass]
        else:
            return klass.__name__
        
    def store(self, obj):
        d = {}
        for item in obj.__attrs__:
            # the "if" here filters out links and linksets
            if type(obj.__attrs__[item]) == attr:
                d[item] = getattr(obj, item)
        newdata = self.storage.store(self._unmap_class(obj.__class__), **d)
        obj.update(**newdata)
        return obj

    def _unmap_link(self, klass, link, name):
        try:
            return self.dbmap[link]
        except KeyError:
            raise ClerkError, "no mapping found for %s.%s" \
                  % (klass.__name__, name)
        

    def fetch(self, klass, ID):
        attrs, othercols = self._fetch_grouped_columns(klass, ID)
        obj = klass(**attrs)
        for name,link in klass.__get_links__():
            fclass, column = self._unmap_link(klass, link, name)
            fID = othercols.get(column)
            if fID:
                inj = LinkInjector(obj, name, self, fclass, fID)
        return obj

    def _fetch_grouped_columns(self, klass, ID):
        attrs, links = {}, {}
        rec = self.storage.fetch(self._unmap_class(klass), ID)
        for item in rec.keys():
            if item in klass.__attrs__:
                attrs[item]=rec[item]
            else:
                links[item]=rec[item]
        return attrs, links

    def fetch_or_new(self, klass, ID):
        if ID:
            return self.fetch(klass, ID)
        else:
            return klass()

    def match(self, klass, **where):
        return [klass(**row) for row
                in self.storage.match(self._unmap_class(klass), **where)]

    def delete(self, klass, ID):
        self.storage.delete(self._unmap_class(klass), ID)
        return None

    def upsert(self, klass, ID, **vals):
        """
        update or insert a single row...
        """
        obj = self.fetch_or_new(klass, ID)
        obj.update(**vals)
        return self.store(obj)




##### OLD STUFF - NO LONGER IMPLEMENTED ###############
# @TODO: this is just here for reference until all tests pass

    def new(self, klass):
        raise NotImplementedError, "just use the constructor"
##         if issubclass(klass, zdc.RecordObject):
##             raise "zdc.RecordObject is deprecated"
##         else:
##             inst = klass()
##             if hasattr(klass, "_links"):
##                 raise "klass should not have _links!"
##                 #for item in klass._links:
##                 #    inst.__dict__[item]=IdxDict()
##             return inst

    def load(self, klass, **where):
        raise NotImplementedError, "use fetch instead"
##         assert where # (if no where clause, call new() instead)
##         if issubclass(klass, zdc.RecordObject):
##             raise "zdc.RecordObject is deprecated"
##             return klass(self.storage, **where)

    def select(self, klass, **wargs):
        raise NotImplementedError #, "use match instead"
##        return self.storage.select(self._unmap_class(klass), **wargs)

    def save(self, obj):
        raise NotImplementedError, "use store instead"
##         # just delegate for now:
##         if isinstance(obj, zdc.RecordObject):
##             obj.save()
##         else:
##             #@TODO: put persistence here!
##             raise NotImplementedError


"""
from duckbill.Customer:
    def save(self):
        super(Customer,self).save()
        for acct in self.accounts:
            acct.customerID = self.ID
        self.accounts.save()

from duckbill.Account:
    def save(self):
        super(Account, self).save()
        self.events.save()
        self.subscriptions.save()

from duckbill.Subscription:
    def save(self):
        super(Subscription, self).save()
        for e in self.events:
            e.accountID = self.accountID
        self.events.save()       
"""
