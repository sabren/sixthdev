from arlo import LinkInjector, LinkSetInjector
from pytypes import IdxDict
from strongbox import *

class ClerkError(Exception): pass

class Clerk(object):
    __ver__="$Id$"
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
        self.memo = {} # used so we get the same object on multiple fetch

    ## public interface ##############################################
        
    def store(self, obj, _others={}):
        # we do this the first time to prevent recursion
        obj.private.isDirty = 0
                
        d = self._object_attrs_as_dict(obj)
        d.update(_others)
        klass = obj.__class__
        tablename = self._unmap_class(klass)

        # we need to save links first, because we depend on them:
        for name, lnk in klass.__get_slots_of_type__(link):
            fclass, column = self._unmap_link(klass, lnk, name)
            ref = getattr(obj, name)
            if (ref):
                if ref.private.isDirty:
                    ref = self.store(ref)
                d[column] = ref.ID
            else:
                d[column] = None

        # now we update obj because of db-generated values
        # (such as autonumbers or timestamps)
        if hasattr(obj, "ID"): old_id = obj.ID
        data_from_db = self.storage.store(tablename, **d)
        relevant_columns = self._attr_columns(klass, data_from_db)
        obj.update(**relevant_columns)
        id_has_changed = hasattr(obj,"ID") and (obj.ID != old_id)

        # we've got the clean data, but we called update
        # with the new primary key,  so we need to reset
        # isDirty. We have to do it before linkset stuff
        # to prevent infinite recursion on cyclic data
        # structures.
        obj.private.isDirty = 0

        # linkSETS, on the other hand, depend on us, so they go last:
        for name, lnk in klass.__get_slots_of_type__(linkset):
            fclass, column = self._unmap_link(klass, lnk, name)
            for item in obj.__values__[name]:
                if id_has_changed or item.private.isDirty:
                    self.store(item, _others={column:obj.ID})

        return obj


    def classToTable(self, klass):
        return self._unmap_class(klass)

    def rowToInstance(self, row, klass):
        attrs, othercols = self._attr_and_other_columns(klass, row)
        uid = (klass, attrs.get("ID"))
        if ("ID" in attrs) and (uid in self.memo):
            obj = self.memo[uid]
        else:
            obj = klass(**attrs)
            self._add_injectors(obj, othercols)
            obj.private.isDirty = 0
            if ("ID" in attrs):
                self.memo[uid]=obj
        return obj


    def match(self, klass, **where):
        res = []
        for row in self.storage.match(self._unmap_class(klass), **where):
            res.append(self.rowToInstance(row, klass))
        return res
   
    def fetch(self, klass, __ID__=None, **kw):
        if __ID__:
            res = self.match(klass, ID=__ID__)
        else:
            res = self.match(klass, **kw)
        if len(res)==0:
            raise LookupError("fetch(%s, %s, **%s) didn't match anything!"
                              % (klass, __ID__, kw))
        elif len(res)>1:
            raise LookupError("fetch(%s) matched multiple values!"
                              % (klass, __ID__, kw))
        return res[0]

    def fetch_or_new(self, klass, ID):
        if ID:
            return self.fetch(klass, ID)
        else:
            return klass()

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


    def _add_injectors(self, obj, othercols):
        klass = obj.__class__
        ## linkinjectors:
        for name,lnk in klass.__get_slots_of_type__(link):
            fclass, column = self._unmap_link(klass, lnk, name)
            fID = othercols.get(column)
            if fID:
                stub = fclass(ID = fID)
                stub.private.isDirty = 0
                setattr(obj, name, stub)
                stub.attach(LinkInjector(self, fclass, fID),
                            onget="inject")
        ## linksetinjectors:
        for name,lnk in klass.__get_slots_of_type__(linkset):
            fclass, column = self._unmap_link(klass, lnk, name)
            #@TODO: there can just be one LSI instance per linkset attribute
            #(since it no longer keeps its own reference to the object)
            obj.attach(LinkSetInjector(name, self, fclass, column),
                       onget="inject")


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
        
    def _unmap_link(self, klass, lnk, name):
        try:
            return self.dbmap[lnk]
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

    def _hasInjectors(self, thing):
        """
        if a thing has injectors attached to it, it
        hasn't been loaded from the database yet, so
        it probably hasn't changed, and thus we don't
        need to update it.    
        """
        if thing is None: return 0
        if not hasattr(thing, "private"): return 0
        for item in thing.private.observers:
            # @TODO: this originally said (LinkInjector, item)
            # @TODO: which could not EVER have worked. Why did it
            # @TODO: take months before this threw an error??!?
            try:
                if isinstance(item[0], LinkInjector):
                    return 1
                if isinstance(item[0], LinkSetInjector):
                    return 1
            except Exception, e:
                raise Exception, "'%s' is invalid injector(??): %s" \
                      % (item[0], e)
        return 0
        
