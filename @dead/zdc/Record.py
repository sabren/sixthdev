# zdc.Record
#
# makes it easy to edit records in a database.

class Record:

    def __init__(self, dbc, table):
        self.dbc = dbc
        self.table = table
        self.key = None
        self.fields = self._getFields()
        self._values = {}
        self._defaults = {}

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
        self.key = ''
        self.values = {}


    def delete(self, key=''):
        """Deletes the specified (defaultis current) record. """
        if key != '':
            self.key = key
        else:
            pass  # we'll delete the current record.

        # and delete it
        sql = "DELETE FROM  " + self.table + \
              "WHERE " + self._whereClause()
        self.dbc.cursor().execute(sql)


    def save(self):
        """Inserts or Updates the record."""
        if self.key == '':
            self._insert()
        else:
            self._update()


    ##############################
    # PRIVATE METHODS            #
    ##############################

    def _sqlQuote(self, field, value):
        """Figures out whether to put '' around a value or not."""
        #@TODO: add quotes for strings..
        #@TODO: make it escape quotes inside of strings
        return value

    def _whereClause(self):
        res = ""
        if type(self.key) == type(1):
            res = "ID=" + self.key
        elif type(self.key) == type({}):
            #@TODO: handle quotes for strings, etc..
            for f in self.key.keys():
                res = res + "AND " + f + "=" + self.keys[f]
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
        pass


    ##############################
    # DICTIONARY METHODS         #
    ##############################

    def __getitem__(self, key):
        return self._values[key]
    
    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.value[key]


