"""
Junction - *:* relationships
"""
__ver__="$Id$"

import zdc

class Junction(zdc.IdxDict):
    __super = zdc.IdxDict
    """
    This does the grunt work for working with
    foreign keys in a *:* relationship.

    @TODO: clarify this documentation.. it even confuses me.
    lKey is local (or left hand) key fieldname (ON THE FOREIGN TABLE!)
    rKey is remote (or right-hand) key fieldname
    lID is the actual value for the local key
    """

    def __init__(self, owner, rClass, tablename, lKey, rKey):
        self.__super.__init__(self)
        self.owner = owner
        self.rClass = rClass
        self.table = zdc.Table(self.owner._table.dbc, tablename)
        self.lKey=lKey
        self.rKey=rKey


    def clear(self):
        self.__super.clear(self)
        # if owner is saved, it may already be linked in db..
        if self.owner.ID:
            self.delete()

    def delete(self):
        """
        Delete the records in the junction, breaking the *:* join.
        """
        for row in self._getRows():
            row.delete()
            
    def fetch(self):
        """
        load the junction data..
        """
        for obj in self._getRows():
            self << obj

    def save(self):
        """
        Save the records in the junction.
        """
        self.delete()
        for robj in self:
            row = self.table.new()
            row[self.lKey] = int(self.owner.ID)
            row[self.rKey] = robj.ID
            row.save()

    def IDs(self):
        #@TODO: do I really need .IDs? (maybe for the edit product form?)
        return tuple(map( lambda robj: robj.ID, self))
                

    def _getRows(self):
        if self.owner.ID:
            res = self.table.select("%s=%s" % (self.lKey, int(self.owner.ID)))
            #@TODO: #orderBy=self.rKey)
        else:
            res = []
        return res
