"""
zdc driver for python DB-API 2.0 database modules.
"""
__ver__="$Id$"

import zdc
from pytypes import IdxDict

class DBAPI2Driver:

    # some escape codes used with SQL..
    escapes = {
        chr( 0) : "\\0",      # NULL
        chr( 9) : "\\t",      # TAB
        chr(10) : "\\n",      # newline
        chr(13) : "\\r",      # carriage return
        chr(34) : '\\"',      # double quote
        chr(39) : "\\'",      # single quote
        chr(92) : "\\\\",     # backslash
        }
    

    def __init__(self, dbc):
        self.dbc = dbc
        self._fieldcache = {}


    def execSQL(self, sql):
        """
        Executes SQL and traps errors.
        """
        cur = self.dbc.cursor()
        try:
            cur.execute(sql)
        except Exception, e:
            raise Exception, 'ERROR: %s \nexecSQL("%s")' % (str(e.args), sql)
        return cur
    

    def select(self, tablename, wclause=None, orderBy=None, **wdict):
        """
        returns a list of records for the given table..
        if a sql/prql where-clause or value dictionary is
        given, only records that match it will be returned.
        """
        import string
        fnames = string.join(map(lambda f: f.name,
                                 self.fields(tablename))
                             , ",")
        sql =\
            """
            SELECT %s FROM %s
            """ % (fnames, tablename)
        
        sql = sql + self._whereClause(tablename, wclause, wdict)
        if orderBy:
            sql = sql + " ORDER BY " + orderBy
        return zdc.toListDict(self.execSQL(sql))


    def update(self, tablename, key, data):
            
        sql = "UPDATE " + tablename + " SET "
        for f in self._fields(tablename):
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
            if not f.isGenerated:
                if data.has_key(f.name):
                    sql = sql + f.name + "=" \
                          + self._sqlQuote(tablename, f.name, data[f.name]) + ","
        #@TODO: unhardcode "ID" without coupling this to table..
        sql = sql[:-1] + self._whereClause(tablename, None, {"ID":key})
        self.execSQL(sql)
        

    def insert(self, tablename, data):
        sql = "INSERT INTO " + tablename + " ("

        vals = ''
        # .. and the fieldnames :
        for f in self._fields(tablename):
            # this is the normal case:
            if not f.isGenerated:
                sql = sql + f.name + ","
                # let's do fields and values at once
                vals = vals + self._sqlQuote(tablename, f.name,
                                             data.get(f.name))
                vals = vals + ","

        # chop off those last commas:
        sql = sql[:-1] + ") VALUES (" + vals[:-1] + ")"

        cur = self.execSQL(sql)

        # get the auto-generated ID, if any:
        # NOTE: THIS -ONLY- WORKS WITH MYSQL!!!
        #
        # I didn't have much luck trying to get the DB-SIG
        # to incorporate autonumbers.. I'll have to try
        # again later.. (or come up with an alternative)
        #
        # @TODO: generate our own autonumbers with max(ID)
       
        #@TODO: UNHARDCODE "ID"
        rowid="ID"
        # first try the newer mysqldb scheme:
        key = int(getattr(cur, "_insert_id", 0))
        if not key:
            try:
                # but if that didn't work, try the old way:
                key = int(self.dbc.insert_id())
            except:
                # and if THAT didn't work, we're out of luck for now
                pass

        # @TODO: this probably ought to just return the key?
        data[rowid] = key


    def delete(self, tablename, wheredict):
        sql = "DELETE FROM %s %s" \
              % (tablename, self._whereClause(tablename, None, wheredict))
        self.execSQL(sql)


    def _whereClause(self, tablename, wclause, wdict):
        """
        Given a dictionary of fieldname:value pairs,
        creates a SQL where clause
        """
        res = ""      
        if wclause:
            res = " WHERE " + wclause
        if wdict:
            ## build a where clause from the specified keywords: 
            for f in wdict.keys():
                if not self._fields(tablename).has_key(f):
                    raise "no field called ", f
                res = res + "AND (" + f + "=" + \
                      self._sqlQuote(tablename, f, wdict[f]) + ")"

            res = res[4:] # strip first AND
            res = " WHERE (" + res + ")"
        return res
    
    def _sqlQuote(self, tablename, fieldname, value):
        """Figures out whether to put '' around a value or not.
        field is an actual field object
        value is the value to quote, or None to quote the record's
        value for the field
        """
        field = self._fields(tablename)[fieldname]
        if value is None:
            res = "NULL"
        elif field.type == zdc.NUMBER:
            res = `value`
            if res[-1]=="L": res = res[:-1]
            
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


    def fields(self, tablename):
        """
        returns an IdxDict of fieldnames and types for a table name
        """
        return self._fields(tablename)

    def _fields(self, tablename):
        """
        same as fields, but this is the one we actually use for
        inserts and deletes..
        
        This is so you can override fields() to add, hide,
        or reorder fields, in select(), while using _fields
        to actually deal with the database..
        
        (I needed to do this in a subclass outside of ZDC)
        """
        if self._fieldcache.has_key(tablename):
            res = self._fieldcache[tablename]
        else:
            res = IdxDict()
            # @TODO: get defaults, keys, etc?
            # select a blank record:
            cur = self.execSQL("SELECT * FROM " + tablename + " WHERE 1=0")
            for f in cur.description:
                res[f[0]] = zdc.Field(f[0],               # name
                                      f[1],  #@TODO: make typeCode a string
                                      f[2],               # displaySize
                                      f[3],               # internalSize
                                      f[4],               # precision
                                      f[5],               # scale
                                      f[6],               # allowNull
                                      None)               # default
            self._fieldcache[tablename] = res
        return res

