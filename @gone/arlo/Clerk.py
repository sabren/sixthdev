from arlo import LinkInjector
from pytypes import IdxDict
from strongbox import attr

class ClerkError(Exception): pass

class Clerk:
    """
    Clerk is an object-relational mapper, responsible
    for storing strongbox-style objects in storage
    systems defined with the 'storage' module.

    Constructor is: Clerk(storage) or Clerk(storage, dbmap)
    where dbmap is a dictionary mapping classes to table names.
    """
   
    def __init__(self, storage, dbmap=None):
        self.storage = storage
        self.dbmap = dbmap or {}

    ## public interface ##############################################
        
    def store(self, obj):
        d = self._object_attrs_as_dict(obj)
        klass = obj.__class__
        tablename = self._unmap_class(klass)

        # now we update obj because of db-generated values
        # (such as autonumbers or timestamps)
        data_from_db = self.storage.store(tablename, **d)
        relevant_columns = self._attr_columns(klass, data_from_db)
        obj.update(**relevant_columns)
        return obj
        

    def fetch(self, klass, ID):
        attrs, othercols = self._fetch_attr_and_other_columns(klass, ID)
        obj = klass(**attrs)
        for name,link in klass.__get_links__():
            fclass, column = self._unmap_link(klass, link, name)
            fID = othercols.get(column)
            if fID:
                inj = LinkInjector(obj, name, self, fclass, fID)
        return obj


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


    ### private stuff ###############################################

    def _unmap_class(self, klass):
        if klass in self.dbmap:
            return self.dbmap[klass]
        else:
            return klass.__name__

    def _object_attrs_as_dict(self, obj):
        #@TODO: should this be on all strongboxen?
        d = {}
        for attrName, attrObject in obj.__attrs__.items():
            # we only want attrs, not links or linksets:
            if type(attrObject) == attr:
                d[attrName] = getattr(obj, attrName)
        return d
        
    def _unmap_link(self, klass, link, name):
        try:
            return self.dbmap[link]
        except KeyError:
            raise ClerkError, "no mapping found for %s.%s" \
                  % (klass.__name__, name)

    def _attr_columns(self, klass, rec):
        return self._attr_and_other_columns(klass, rec)[0]

    def _attr_and_other_columns(self, klass, rec):
        attrs, others = {}, {}
        for item in rec.keys():
            if item in klass.__attrs__:
                attrs[item]=rec[item]
            else:
                others[item]=rec[item]
        return attrs, others

    def _fetch_attr_and_other_columns(self, klass, ID):
        rec = self.storage.fetch(self._unmap_class(klass), ID)
        return self._attr_and_other_columns(klass, rec)



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
