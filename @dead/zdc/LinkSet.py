"""
LinkSet
"""
import zdc

class LinkSet(zdc.IdxDict):
    """
    This does the grunt work for working with
    foreign keys in a 1:* relationship.

    @TODO: does this work unchanged for *:* relationships?

    lKey is local (or left hand) key fieldname
    rKey is remote (or right-hand) key fieldname
    lID is the actual value for the local key
    """
    __super = zdc.IdxDict

    def __init__(self, owner, rClass, lKey, rKey="ID"):
        self.__super.__init__(self)
        self.owner = owner
        self.rClass = rClass
        self.lKey = lKey
        self.rKey = rKey
        self._loaded = 0

    def load(self):
        table = self.rClass._table
        lID = self.owner.ID
        if lID is not None:
            cur = table.dbc.cursor()
            sql = 'SELECT %s from %s where %s=%i' \
                  % (self.rKey, table.name, self.lKey, int(lID))
            cur.execute(sql)
            for row in cur.fetchall():
                #@TODO: unhardcode ID
                self << self.rClass(ID=row[0])
        self._loaded = 1


    def new(self):
        return self.rClass()

    def __len__(self):
        if not self._loaded:
            self.load()
        return self.__super.__len__(self)
        
    def __getitem__(self, key):
        if not self._loaded:
            self.load()
        return self.__super.__getitem__(self, key)
        
