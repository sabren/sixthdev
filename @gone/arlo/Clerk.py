from arlo import LinkInjector, LinkSetInjector
from pytypes import IdxDict
from strongbox import *
from storage import where
from __future__ import generators
import operator

class ClerkError(Exception): pass

def getSlotsOfType(klass, t):
    for slot in klass.__attrs__:
        attr = getattr(klass, slot)
        if isinstance(attr, t):
            yield (slot, attr)


class BoxInspector(object):
    def __init__(self, box):
        self.box = box
    def plainValues(self):
        """
        returns a dict of name:value pairs
        with one enty per plain attribute
        """
        res = {}
        for item in self.plainAttributes():
            res[item] = getattr(self.box, item)
        return res
    def plainAttributes(self):
        """
        returns a list of plain attribute
        names  on the box:  Attributes, but not
        links, linksets, or virtual properties
        """
        return [
            name
            for (name,value) in self.box.__attrs__.items()
            if type(value) == attr
        ]
    def linkNames(self):
        return getSlotsOfType(self.box.__class__, link)
    

class Schema(object):
    def __init__(self, dbmap=None):
        """
        optionally takes a dict that maps
        strongbox.*Box classes to tables
        and strongbox.Link instances to 
        columns
        """
        self.dbmap = {}
        if dbmap:
            self.dbmap.update(dbmap)

    # these two are given explictly:
    def tableForClass(self, klass):
        return self.dbmap[klass]
    def columnForLink(self, ln):
        return self.dbmap[ln]

    # the rest are inferred:
    def tableForLink(self, ln):
        return self.tableForClass(ln.type)
    def tableForLinkSet(self, ls):
        return self.tableForClass(ls.type)
    def columnForLinkSet(self, ls):
        return self.columnForLink(getattr(ls.type, ls.back))


## class AutoSchema(object): # @TODO: make this class
##     """
##     Automatically maps objects to tables,
##     and Links to foreign key names.
##     """
##     def __getitem__(self, item):
##         if isinstance(item, link):
##             return item.type, item.__name__ + "ID"
##         elif isinstance(item, linkset):
##             assert item.back, "no .back found for %s.%s" \
##                    % (item.__owner__.__name__ , item.__name__)
##             return item.back.__name__ + "ID"
##         else:
##             return item.__name__

## @TODO: need to put item.__name__ on links
## ... also see if the keyerror throws the
## classname so I don't have to do "no mapping found for ..."
        
##     def _unmap_class(self, klass):
##         if klass in self:
##             return self[klass]
##         else:
##             return klass.__name__

##     def _unmap_link(self, klass, lnk, name):
##         try:
##             return self[lnk]
##         except KeyError:
##             raise ClerkError, "no mapping found for %s.%s" \
##                   % (klass.__name__, name)
    
        
    

class Clerk(object):
    __ver__="$Id$"
    """
    Clerk is an object-relational mapper, responsible
    for storing strongbox-style objects in storage
    systems defined with the 'storage' module.

    Constructor is: Clerk(storage) or Clerk(storage, dbmap)
    where dbmap is a dictionary mapping classes to table names.
    """

    def __init__(self, storage, schema):
        self.storage = storage
        self.schema = schema
        
        # so we always return same instance for same row:
        # @TODO: WeakValueDictionary() doesn't work with strongbox. Why?!
        self.cache = {} 

    ## public interface ##############################################
        
    def store(self, obj):
        # we do this the first time to prevent recursion
        obj.private.isDirty = 0

        insp = BoxInspector(obj)
                
        vals = insp.plainValues()
        klass = obj.__class__

##         print
##         print "storing %s" % obj.__class__.__name__
##         print "1: %s" % vals.keys()

        # we need to save links first, because we depend on them:
        for name, lnk in insp.linkNames():
            column = self.schema.columnForLink(lnk)
            ref = getattr(obj, name)
            if (ref):
                if ref.private.isDirty:
                    ref = self.store(ref)
                vals[column] = ref.ID
            else:
                vals[column] = 0

##         print "2. %s" % vals.keys()

        # now we update obj because of db-generated values
        # (such as autonumbers or timestamps)
        if hasattr(obj, "ID"): old_id = obj.ID
        data_from_db = self.storage.store(self.schema.tableForClass(klass), **vals)
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
        for name, ls in getSlotsOfType(klass,linkset):
            column = self.schema.columnForLinkSet(ls)
            for item in getattr(obj.private, name):
                if id_has_changed or item.private.isDirty:
                    assert getattr(item, ls.back) is obj, \
                           "getattr(%s, %s) was not (this) %s" \
                           % (item.__class__.__name__,
                              ls.back,
                              obj.__class__.__name__)
                    self.store(item)

        self._makeMemo(obj)
        return obj


    def rowToInstance(self, row, klass):
        attrs, othercols = self._attr_and_other_columns(klass, row)
        obj = self._get_memo(klass, attrs.get("ID"))
        if not obj:
            obj = klass(**attrs)
            self.addInjectors(obj, othercols)
            obj.private.isDirty = 0
            self._makeMemo(obj)
        return obj


    def match(self, klass, *args, **kwargs):
        return [self.rowToInstance(row, klass)
                for row in self.storage.match(self.schema.tableForClass(klass),
                                              *args, **kwargs)]

    def matchOne(self, klass, *args, **kwargs):
        res = self.match(klass, *args, **kwargs)
        if len(res)==0:
            raise LookupError("matchOne(%s, *%s, **%s) didn't match anything!"
                              % (klass, args, kw))
        elif len(res)>1:
            raise LookupError("matchOne(%s, *%s, **%s) matched %s objects!"
                              % (klass, args, kw, len(res)))
        return res[0]
        
   
    def fetch(self, klass, __ID__=None, **kw):
        if __ID__:
            return self.matchOne(klass, ID=__ID__)
        else:
            return self.matchOne(klass, **kw)

    def delete(self, klass, ID):
        self.storage.delete(self.schema.tableForClass(klass), ID)
        return None


    ### private stuff ###############################################

    def _get_memo(self, klass, key):
        uid = (klass, key)
        return self.cache.get(uid)

    def _makeMemo(self, obj):
        if hasattr(obj, "ID"):
            self.cache[(obj.__class__, obj.ID)]=obj
        else:
            raise Warning("couldn't memo %s because it had no ID attribute" % obj)


    def addInjectors(self, obj, othercols):
        klass = obj.__class__
        ## linkinjectors:
        for name,lnk in getSlotsOfType(klass,link):
            fclass = lnk.type
            column = self.schema.columnForLink(lnk)
            fID = othercols.get(column)
            if fID:
                stub = fclass(ID = fID)
                stub.private.isDirty = 0
                setattr(obj, name, stub)
                stub.addInjector(LinkInjector(self, fclass, fID).inject)

        ## linksetinjectors:
        for name,ls in getSlotsOfType(klass,linkset):
            fclass = ls.type
            column = self.schema.columnForLinkSet(ls)
            #@TODO: there can just be one LSI instance per linkset attribute
            #(since it no longer keeps its own reference to the object)
            obj.addInjector(LinkSetInjector(name, self, fclass, column).inject)



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

