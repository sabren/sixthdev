"""
zdc.Table - a module representing a single table in a database.
"""
__ver__="$Id$"

import zdc
#@TODO: handle keys, defaults, autonumbers, etc..

class Table(zdc.Object):
    __super = zdc.Object

    escapes = {  #@TODO: put this somewhere else? does the DB-API do this?
        chr( 0) : "\\0",      # NULL
        chr( 9) : "\\t",      # TAB
        chr(10) : "\\n",      # newline
        chr(13) : "\\r",      # carriage return
        chr(34) : '\\"',      # double quote
        chr(39) : "\\'",      # single quote
        chr(92) : "\\\\",     # backslash
        }
    
    ## constructor ##############################################
                       
    def __init__(self, dbc, name, rowid="ID"):
        self.__super.__init__(self)
        self._data["dbc"] = dbc
        self._data["name"] = name
        self._data["fields"] = self._getFields()
        self._data["rowid"] = rowid

    ## public methods ###########################################

    def new(self):
        return zdc.Record(self)

    def select(self, wclause=None, **wdict):
        """
        returns a list of records.. matching either a where
        clause (if supported) or dictionary
        """
        ## build a where clause
        if not ((wclause is None) ^ (wdict=={})): # xor
            ## no criteria specified: get it all..
            where = ""
        elif wdict:
            ## keywords specified: search for 'em
            for k in wdict.keys():
                if not self.fields.has_key(k):
                    raise "no field called ", k
            where = self._whereClause(wdict)
        else:
            ## sql where clause specified
            where = " WHERE " + wclause
        
        ## run the query..
        sql = "SELECT * FROM " + self.name + where
        cur = self.dbc.cursor()
        cur.execute(sql)

        ## loop through and build records..
        res = []
        for row in cur.fetchall():
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
            recs = self.select("%s=%s" \
                               % (self.rowid,
                                  self._sqlQuote(self.fields[self.rowid], key)
                                  ))
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
        #@TODO: TEST THIS! I just spent almost an hour tracking down a
        #@TODO: bug where this simply wasn't executing the sQL!
        #                                                      
        #                   ####### 
        #                  #########
        #                  #########
        #                  #########
        #                   ####### 
        #                   #######
        #                   #######
        #                    ##### 
        #                    #####
        #                    #####
        #                     ### 
        #                     ### 
        #                     ### 
        #                         
        #                     ### 
        #                    #####
        #                    #####
        #                     ### 
        #
        #
        sql = "DELETE FROM %s WHERE %s=%s" % (self.name, self.rowid, key)
        cur = self.dbc.cursor()
        cur.execute(sql)


    def update(self, key, data):
        sql = "UPDATE " + self.name + " SET "
        for f in self.fields:
            #@TODO: allow support for datetimes!!!!
            # here's the issue: for some reason, MySQL gives me a
            # nasty warning... but I haven't been able to figure out
            # what the warning actually IS because of problems with
            # MySQLdb.. and I can't seem to duplicate it outside of
            # python. So right now, until I fix this, you just have to
            # cope with datetimes/timestamps by yourself. :/ :/ :/
            #
            # actually, I think that it works with some dates and not
            # with others... but not sure..
            if not f.type == zdc.TIMESTAMP:
                if not f.isGenerated:
                    if data.has_key(f.name):
                        sql = sql + f.name + "=" \
                              + self._sqlQuote(f, data[f.name]) + ","
        sql = sql[:-1] + " WHERE %s=%s" % (self.rowid, key)
        cur = self.dbc.cursor()
        cur.execute(sql)
        

    def insert(self, data):
        sql = "INSERT INTO " + self.name + " ("

        vals = ''
        # .. and the fieldnames :
        for f in self.fields:
            # a hack to handle initialtimestamps:
            if f.name in data.insertStamps:  #<------ @TODO: fix!
                sql = sql + f.name + ","
                vals = vals + "now(),"
            # this is the normal case:
            elif not f.isGenerated:
                sql = sql + f.name + ","
                # let's do fields and values at once
                vals = vals + self._sqlQuote(f, data[f.name]) + ","

        # chop off those last commas:
        sql = sql[:-1] + ") VALUES (" + vals[:-1] + ")"

        cur = self.dbc.cursor()
        cur.execute(sql)

        # get the auto-generated ID, if any:
        # NOTE: THIS -ONLY- WORKS WITH MYSQL!!!
        #
        # I didn't have much luck trying to get the DB-SIG
        # to incorporate autonumbers.. I'll have to try
        # again later.. (or come up with an alternative)
        #
        # @TODO: generate our own autonumbers with max(ID)
       
        if self.rowid is not None:
            # first try the newer mysqldb scheme:
            key = int(getattr(cur, "_insert_id", 0))
            if not key:
                try:
                    # but if that didn't work, try the old way:
                    key = int(self.dbc.insert_id())
                except:
                    # and if THAT didn't work, we're out of luck for now
                    raise "don't yet know how to do autonumbers except MySQL"
            data[self.rowid] = key


    def _whereClause(self, where):
        """Given a dictionary of fieldname:value pairs,
        creates a SQL where clause"""
        res = ""      
        for f in where.keys():
            res = res + "AND (" + f + "=" + \
                  self._sqlQuote(self.fields[f], where[f]) + ")"

        res = res[4:] # strip first AND
        return " WHERE (" + res + ")"


    def _sqlQuote(self, field, value):
        """Figures out whether to put '' around a value or not.
        field is an actual field object
        value is the value to quote, or None to quote the record's
        value for the field
        """
        if value is None:
            res = "NULL"
        
        #@TODO: handle DATE types explicitly
        elif field.type == zdc.NUMBER:
            res = `value`
            
        # binary, text, and string are all treated the same,
        # at least for now:
        else:
            # loop through each character individually..
            # if we used string.replace, we could get in troulbe
            # by escaping things we've already escaped            
            res = ''
            for ch in value:
                res = res + self.escapes.get(ch, ch)
            res = "'%s'" % res
        return res




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

