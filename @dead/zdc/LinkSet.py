"""
LinkSet - 1:* relationships.
"""
__ver__="$Id$"

from pytypes import IdxDict

class LinkSet(IdxDict):
    """
    This does the grunt work for working with
    foreign keys in a 1:* relationship.

    @TODO: clarify this documentation.. it even confuses me.
    lKey is local (or left hand) key fieldname (ON THE FOREIGN TABLE!)
    rKey is remote (or right-hand) key fieldname
    lID is the actual value for the local key
    """
    __super = IdxDict

    def __init__(self, owner, rClass, lKey=None, rKey="ID"):
        self.__super.__init__(self)
        self.owner = owner
        self.rClass = rClass
        self.lKey = lKey
        self.rKey = rKey
        self._loaded = 0


    def load(self):
        lID = getattr(self.owner, "ID", None)
        if lID is not None:
            rows = self.owner._ds.select(self.rClass._tablename, "%s=%i"
                                         % (self.lKey, int(lID)))
            for row in rows:
                #@TODO: unhardcode primary key for right hand class
                self << self.rClass(self.owner._ds, "ok", ID=row["ID"])
        self._loaded = 1


    def save(self):
        for item in self:
            setattr(item, self.lKey, getattr(self.owner, "ID", None))
            item.save()

    def new(self):
        return self.rClass(self.owner._ds, "ok")

    def __len__(self):
        if not self._loaded:
            self.load()
        return self.__super.__len__(self)
        
    def __getitem__(self, key):
        if not self._loaded:
            self.load()
        return self.__super.__getitem__(self, key)
        
    def __lshift__(self, other):
        if isinstance(other, self.rClass):
            self.__super.__lshift__(self, other)
        else:
            raise TypeError, "can't add %s to this LinkSet" \
                  % other.__class__.__name__
