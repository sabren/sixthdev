"""
zdc.Table - a module representing a single table in a database.
"""
__ver__="$Id$"

import zdc

class Table(zdc.Object):

    ## constructor ##############################################
                       
    def __init__(self, dbc, name, rowid="ID"):
        super(Table,self).__init__()       
        self._data["dbc"] = dbc
        self._data["name"] = name
        self._data["fields"] = self.dbc.fields(self.name)
        self._data["rowid"] = rowid

    ## public methods ###########################################

    def new(self):
        return zdc.Record(self)

    def select(self, where=None, **wdict):
        """
        returns a list of record objects.. matching either a where
        clause (if supported) or dictionary
        """
        ## get the matching records from the connection..
        rows = apply(self.dbc.select, (self.name, where), wdict)

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
            if key:
                raise LookupError, \
                      "record not found in table %s for key %s" \
                      % (self.name, key)
            else:
                raise LookupError, "record not found in table %s where %s" \
                      % (self.name, where)
        elif len(recs) > 1:
            raise LookupError, "mulitple records found for single key!!"
        return recs[0]

    def delete(self, key):
        self.dbc.delete(self.name, {self.rowid:key})


    def update(self, key, data):
        self.dbc.update(self.name, key, data)


    def insert(self, data):
        self.dbc.insert(self.name, data)
