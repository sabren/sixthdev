"""
zdc.Table - a module representing a single table in a database.
"""
__ver__="$Id$"

import zdc
#@TODO: handle keys, defaults, autonumbers, etc..

class Table(zdc.Object):
    __super = zdc.Object

    ## constructor ##############################################
                       
    def __init__(self, dbc, name, rowid="ID"):
        self.__super.__init__(self)
        self._data["dbc"] = dbc
        self._data["name"] = name
        self._data["fields"] = self._getFields()
        self._data["rowid"] = rowid
        import zdc.drivers.DBAPI2Driver
        self._data["driver"] = zdc.drivers.DBAPI2Driver.DBAPI2Driver(dbc)

    ## public methods ###########################################

    def new(self):
        return zdc.Record(self)

    def select(self, wclause=None, **wdict):
        """
        returns a list of record objects.. matching either a where
        clause (if supported) or dictionary
        """
        ## get the matching records from the driver..
        rows = apply (self.driver.select, (self, wclause), wdict)

        ## loop through and build record objects
        res = []
        for row in rows:
            rec = zdc.Record(self)
            rec.isNew = 0 #@TODO: should happen by default, if i pass data in
            for f in range(len(row)):
                # we do this to get rid of the L at the end of longs:
                if type(row[f]) == type(1L):
                    rec[self.fields[f].name]=int(row[f])
                else:
                    rec[self.fields[f].name]=row[f]
            res.append(rec)
        return res



    def fetch(self, key=None, **where):
        """
        fetch a single Record, given the key.
        """
        ## make sure they supply key xor where:
        if not ((key is None) ^ (where=={})):
            raise TypeError, \
                  "fetch() requires either a key or a set of field-value pairs"
        ## either convert key into a where clause for select()..
        if key:
            recs = apply(self.select, (), {self.rowid:key})
        ## ... or just pass the dict on to select()
        else:
            recs = apply(self.select, (), where)

        ## ensure exactly one record was returned:
        if recs == []:
            raise LookupError, "record not found for key %s" % key
        elif len(recs) > 1:
            raise LookupError, "mulitple records found for single key!!"
        return recs[0]

    def delete(self, key):
        self.driver.delete(self, {self.rowid:key})


    def update(self, key, data):
        self.driver.update(self, key, data)

    def insert(self, data):
        self.driver.insert(self, data)


    ## private methods ###########################################
       
    def _getFields(self):
        """Called internally to create .fields"""

        flds = zdc.IdxDict()
        # select a blank record:
        # @TODO: more sophisticated schema checking to get defaults, keys, etc?
        cur = self.dbc.cursor()
        cur.execute("SELECT * FROM " + self.name + " WHERE 1=0")
        for f in cur.description:
            flds[f[0]] = zdc.Field(f[0],               # name
                                   f[1],  #@TODO: make typeCode a string
                                   f[2],               # displaySize
                                   f[3],               # internalSize
                                   f[4],               # precision
                                   f[5],               # scale
                                   f[6],               # allowNull
                                   None)               # default
        return flds

