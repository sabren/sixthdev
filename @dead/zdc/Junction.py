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
        self.tablename = tablename
        self.lKey=lKey
        self.rKey=rKey

    def delete(self):
        """
        delete nodes for this product. used internally.
        """
        cur = self.owner._table.dbc.cursor()
        sql =\
            """
            DELETE FROM %s
            WHERE %s=%s
            """ % (self.tablename, self.lKey, int(self.owner.ID))
        cur.execute(sql)

    def fetch(self):
        if self.owner.ID:
            cur = self.owner._table.dbc.cursor()
            sql =\
                """
                SELECT %s
                FROM %s 
                WHERE %s=%s
                ORDER BY nodeID
                """ % (self.rKey, self.tablename, self.lKey,
                       int(self.owner.ID))
            cur.execute(sql)

            # cur.execute returns a tuple of tuples, eg ((1,), (2,) ...)
            # we only want the first value (column) from each tuple.
            for row in cur.fetchall():
                self << self.rClass(ID=row[0])

    def IDs(self):
        #@TODO: do I really need .IDs? (maybe for the edit product form?)
        return tuple(map( lambda robj: robj.ID, self))
                
    def save(self):
        # handle the nodes:
        cur = self.owner._table.dbc.cursor()        
        self.delete()
        for robj in self:
            sql =\
                """
                INSERT INTO %s (%s, %s)
                VALUES (%s, %s)
                """ % (self.tablename, self.lKey, self.rKey,
                       int(self.owner.ID), robj.ID)
            cur.execute(sql)

