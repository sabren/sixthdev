# zdc.Record
#
# makes it easy to edit records in a database.

class Record:

    def __init__(self, dbc, table, module=None, rowid='ID'):
        self.dbc = dbc
        self.table = table
        self.rowid = "ID"   # this is the 'autonumber' field, if any
        self.key = None     # either a numeric value for an "ID" field, or a dict
        self.fields = self._getFields()
        self.values = {}
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

    def fetch(self, key):
        self.key = key
        sql = "SELECT * FROM " + self.table + \
              "WHERE " + self._whereClause()
        cur = self.dbc.cursor()
        cur.execute(sql)

        #@TODO: fill in the values hash..


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
              "WHERE " + self._whereClause()
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
        
        #@TODO: handle BINARY/DATE types explicitly
        if field.type == self.dbcModule.NUMBER:
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
            res = "ID=" + self.key
        elif type(self.key) == type({}):
            #@TODO: handle quotes for strings, etc..
            for f in self.key.keys():
                print "#######F: ", f
                res = res + "AND " + f + "=" + _sqlQuote(self.fields[f], self.keys[f])
            res = "(" + res[4:] + ")"
        else:
            raise "Invalid key."


    def _getFields(self):
        """Called internally to create .fields"""
        import IdxDict
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
        pass


    def _insert(self):
        sql = "INSERT INTO " + self.table + " ("

        vals = ''
        # .. and the fieldnames :
        for f in self.fields:
            # @TODO: fix this to handle non-"ID"-style schemas (see _whereClause)
            if f.name != "ID":
                sql = sql + f.name + ","
                # let's do fields and values at once
                vals = vals + self._sqlQuote(f) + ","

        # chop off those last commas:
        sql = sql[:-1] + ") VALUES (" + vals[:-1] + ")"

        cur = self.dbc.cursor()
        self.dbc.insert_id()
        cur.execute(sql)                    


    ##############################
    # DICTIONARY METHODS         #
    ##############################

    def __getitem__(self, fld):
        return self.values[fld]
    
    def __setitem__(self, fld, value):
        self.values[fld] = value

    def __delitem__(self, fld):
        del self.value[fld]

