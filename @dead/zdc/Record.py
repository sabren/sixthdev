# zdc.Record
#
# makes it easy to edit records in a database.

import IdxDict

class Record:

    def __init__(self, dbc, table, module=None, autoNum='ID'):
        self.dbc = dbc
        self.table = table
        self.autoNum = autoNum  # this is the 'autoNumber' field, if any (MYSQL ONLY!)
        self.key = None     # either a numeric value for an "autoNum" field, or a dict
        self.fields = self._getFields()
        self.values = IdxDict.IdxDict()
        for f in self.fields:
            self.values[f.name] = None
            
        self.quoteEscape = "'"
        if module:
            self.dbcModule = module
        else:
            try:
                module = dbc.__class__.__module__
                exec('import ' + module)
                self.dbcModule = eval(module)
            except:
                raise "Couldn't guess DB-API module. Pass module as 3rd parameter to Record()"

 
    ##############################
    # PUBLIC METHODS             #
    ##############################

    def fetch(self, keyID=None, **hash):
        if keyID:
            self.key = keyID
        else:
            self.key = hash

        sql = "SELECT * FROM " + self.table + \
              self._whereClause()

        cur = self.dbc.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        for f in range(len(row)):
            self[self.fields[f].name]=row[f]


    def new(self):
        """Prepare to add a new record."""
        self.key = None
        for f in self.fields:
            self.values[f.name] = f.default


    def delete(self, key=None):
        """Deletes the specified (default is current) record. """
        if key is not None:
            self.key = key
        else:
            pass  # because we'll just delete the current record.

        # and delete it
        sql = "DELETE FROM  " + self.table + \
              self._whereClause()
        self.dbc.cursor().execute(sql)


    def save(self):
        """Inserts or Updates the record."""
        if self.key is None:
            self._insert()
        else:
            self._update()


    ##############################
    # PRIVATE METHODS            #
    ##############################

    def _sqlQuote(self, field, value=None):
        """Figures out whether to put '' around a value or not.
        field is an actual field object
        value is the value to quote, or None to quote the record's value for the field
        """

        res = ''
        if value is None:
            value = self[field.name]

        # but if it's STILL None, use a null..
        if value is None:
            res = "NULL"
        
        #@TODO: handle BINARY/DATE types explicitly
        elif field.type == self.dbcModule.NUMBER:
            res = `value`
        else: # should be elif ... STRING
            res = "'"
            for c in value:
                # escape quotes:
                if c == "'":
                    res = res + self.quoteEscape + c
                else:
                    res = res + c
            res = res + "'"
        
        return res

    def _whereClause(self):
        res = ""
        if type(self.key) == type(1):
            res = self.autoNum + "=" + `self.key`
        elif type(self.key) == type(1L):
            res = self.autoNum + "=" + `self.key`[:-1]
        elif type(self.key) == type({}):
            for f in self.key.keys():
                res = res + "AND (" + f + "=" + self._sqlQuote(self.fields[f], self.key[f]) + ")"
            res = res[4:] # strip first AND
        else:
            raise "Invalid key: " + `self.key`
        return " WHERE (" + res + ")"


    def _getFields(self):
        """Called internally to create .fields"""
        import Field
        flds = IdxDict.IdxDict()
        # select a blank record:
        # @TODO: more sophisticated schema checking to get defaults, keys, etc?
        cur = self.dbc.cursor()
        cur.execute("SELECT * FROM " + self.table + " WHERE 1=0")
        for f in cur.description:
            flds[f[0]] = Field.Field(f[0],               # name
                                     f[1],  #@TODO: make typeCode a string
                                     f[2],               # displaySize
                                     f[3],               # internalSize
                                     f[4],               # precision
                                     f[5],               # scale
                                     f[6],               # allowNull
                                     None)               # default
        return flds

    def _update(self):
        sql = "UPDATE " + self.table + " SET "
        for f in self.fields:
            if f.name != self.autoNum:
                sql = sql + f.name + "=" + self._sqlQuote(f) + ","
        sql = sql[:-1] + self._whereClause()

        cur = self.dbc.cursor()
        cur.execute(sql)


    def _insert(self):
        sql = "INSERT INTO " + self.table + " ("

        vals = ''
        # .. and the fieldnames :
        for f in self.fields:
            # if autoNum is none, all columns show up:
            if f.name != self.autoNum:
                sql = sql + f.name + ","
                # let's do fields and values at once
                vals = vals + self._sqlQuote(f) + ","

        # chop off those last commas:
        sql = sql[:-1] + ") VALUES (" + vals[:-1] + ")"

        cur = self.dbc.cursor()
        cur.execute(sql)                    

        # get the auto-generated ID, if any:
        # NOTE: THIS ONLY WORKS WITH MYSQL!!!
        if self.autoNum:
            self.key = self.dbc.insert_id()
            self[self.autoNum] = self.key


    ##############################
    # DICTIONARY METHODS         #
    ##############################

    def __getitem__(self, fld):
        return self.values[fld]
    
    def __setitem__(self, fld, value):
        self.values[fld] = value

    def __delitem__(self, fld):
        del self.value[fld]

