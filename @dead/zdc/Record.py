"""
zdc.Record -  makes it easy to edit records in a database.

$Id$
"""


from IdxDict import IdxDict

# @TODO: much of this ought to be moved to the 'Table' class..

class Record:

    ## attributes ################################################

    table = None
    values = IdxDict()
    isNew = 0
    
    escapes = {  #@TODO: put this somewhere else? does the DB-API do this?
        chr( 0) : "\\0",      # NULL
        chr( 9) : "\\t",      # TAB
        chr(10) : "\\n",      # newline
        chr(13) : "\\r",      # carriage return
        chr(34) : '\\"',      # double quote
        chr(39) : "\\'",      # single quote
        chr(92) : "\\\\",     # backslash
        }
    
    _where = {}


    ## constructor ###############################################

    def __init__(self, table=None, **where):

        ## A record's table can be passed in the constructor or
        ## defined a subclass's definition... Most likely, you won't
        ## create records directly, but call someTable.getRecord()
               
        if table:
            self.table = table
        assert self.table is not None, "Record must have an associated Table!"

        if where:
            apply (self._fetch, (), where)
        else:
            self._new()


    ## public methods ###############################################

    def delete(self):
        """Deletes the record. """

        # and delete it
        sql = "DELETE FROM  " + self.table.name + \
              self._whereClause()
        self.table.dbc.cursor().execute(sql)


    def save(self):
        """Inserts or Updates the record."""
        if self.isNew:
            self._insert()
            self.isNew = 0
        else:
            self._update()


    ## private methods #################################################

    def _fetch(self, **where):
        if not where:
            raise "don't know which record to fetch"
        else:
            for k in where.keys():
                if not self.table.fields.has_key(k):
                    raise "no field called ", k

        self.isNew = 0
        self._where = where
        sql = "SELECT * FROM " + self.table.name + self._whereClause()

        cur = self.table.dbc.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        if row is None:
            raise "record not found where" + `where`

        for f in range(len(row)):
            # we do this to get rid of the L at the end of longs:
            if type(row[f]) == type(1L):
                self[self.table.fields[f].name]=int(row[f])
            else:
                self[self.table.fields[f].name]=row[f]


    def _new(self):
        """Prepare to add a new record. This is called by default."""
        self.isNew = 1
        for f in self.table.fields:
            self.values[f.name] = f.default



    def _sqlQuote(self, field, value=None):
        """Figures out whether to put '' around a value or not.
        field is an actual field object
        value is the value to quote, or None to quote the record's
        value for the field
        """

        res = ''
        if value is None:
            value = self[field.name]

        # but if it's STILL None, use a null..
        if value is None:
            res = "NULL"
        
        #@TODO: handle DATE types explicitly
        elif field.type == self.table.dbc_module.NUMBER:
            res = `value`
            
        # binary, text, and string are all treated the same,
        # at least for now:
        else:
            # loop through each character individually..
            # if we used string.replace, we could get in troulbe
            # by escaping things we've already escaped            
            for ch in value:
                res = res + self.escapes.get(ch, ch)
            res = "'%s'" % res
        return res



    def _whereClause(self):
        """Given a dictionary of fieldname:value pairs,
        creates a SQL where clause"""
        
        res = ""      
        for f in self._where.keys():
            res = res + "AND (" + f + "=" + \
                  self._sqlQuote(self.table.fields[f], self._where[f]) + ")"

        res = res[4:] # strip first AND           
        return " WHERE (" + res + ")"




    def _update(self):
        sql = "UPDATE " + self.table.name + " SET "
        for f in self.table.fields:
            if not f.isGenerated:
                sql = sql + f.name + "=" + self._sqlQuote(f) + ","
        sql = sql[:-1] + self._whereClause()

        cur = self.table.dbc.cursor()
        cur.execute(sql)



    def _insert(self):
        sql = "INSERT INTO " + self.table.name + " ("

        vals = ''
        # .. and the fieldnames :
        for f in self.table.fields:
            if not f.isGenerated:
                sql = sql + f.name + ","
                # let's do fields and values at once
                vals = vals + self._sqlQuote(f) + ","

        # chop off those last commas:
        sql = sql[:-1] + ") VALUES (" + vals[:-1] + ")"

        cur = self.table.dbc.cursor()
        cur.execute(sql)

        # get the auto-generated ID, if any:
        # NOTE: THIS -ONLY- WORKS WITH MYSQL!!!
        #
        # I didn't have much luck trying to get the DB-SIG
        # to incorporate autonumbers.. I'll have to try
        # again later.. (or come up with an alternative)
       
        if self.table.rowid is not None:
            # first use the newer mysql scheme:
            self.key = int(getattr(cur, "_insert_id", 0))
            if not self.key:
                try:
                    self.key = int(self.table.dbc.insert_id())
                except:
                    raise "don't yet know how to do autonumbers except MySQL"
            self[self.table.rowid] = self.key
            self._where[self.table.rowid] = self.key



    ### dictionary methods ######################################

    def __getitem__(self, fld):
        return self.values[fld]
    
    def __setitem__(self, fld, value):
        self.values[fld] = value

    def __delitem__(self, fld):
        del self.value[fld]

    def keys(self):
        return self.values.keys()

    def get(self, fld, default=None):
        return self.values.get(fld, default)
