"""
zdc driver for python DB-API 2.0 database modules.
"""
__ver__="$Id$"
import zdc

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


    def select(self, table, wclause=None, **wdict):
        """
        returns a list of records for the given table..
        if a sql/prql where-clause or value dictionary is
        given, only records that match it will be returned.
        """
        ## build a where clause
        if not ((wclause is None) ^ (wdict=={})): # xor
            ## no criteria specified: get it all..
            where = ""
        elif wdict:
            ## keywords specified: search for 'em
            for k in wdict.keys():
                if not table.fields.has_key(k):
                    raise "no field called ", k
            where = self._whereClause(table, wdict)
        else:
            ## sql where clause specified
            where = " WHERE " + wclause
        
        ## run the query..
        sql = "SELECT * FROM " + table.name + where
        cur = self.dbc.cursor()
        cur.execute(sql)
        return cur.fetchall()


    def update(self, table, key, data):
            
        sql = "UPDATE " + table.name + " SET "
        for f in table.fields:
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
                              + self._sqlQuote(table, f, data[f.name]) + ","
        sql = sql[:-1] + " WHERE %s=%s" % (table.rowid, key)
        cur = self.dbc.cursor()
        cur.execute(sql)
        

    def insert(self, table, data):
        sql = "INSERT INTO " + table.name + " ("

        vals = ''
        # .. and the fieldnames :
        for f in table.fields:
            # a hack to handle initialtimestamps:
            if f.name in data.insertStamps:  #<------ @TODO: fix!
                sql = sql + f.name + ","
                vals = vals + "now(),"
            # this is the normal case:
            elif not f.isGenerated:
                sql = sql + f.name + ","
                # let's do fields and values at once
                vals = vals + self._sqlQuote(table, f, data[f.name]) + ","

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
       
        if table.rowid is not None:
            # first try the newer mysqldb scheme:
            key = int(getattr(cur, "_insert_id", 0))
            if not key:
                try:
                    # but if that didn't work, try the old way:
                    key = int(self.dbc.insert_id())
                except:
                    # and if THAT didn't work, we're out of luck for now
                    raise "don't yet know how to do autonumbers except MySQL"

            # @TODO: this probably ought to just return the key?
            data[table.rowid] = key



        

    def delete(self, table, wheredict):
        sql = "DELETE FROM %s %s" \
              % (table.name, self._whereClause(table, wheredict))
        cur = self.dbc.cursor()
        cur.execute(sql)


    def _whereClause(self, table, where):
        """Given a dictionary of fieldname:value pairs,
        creates a SQL where clause"""
        res = ""      
        for f in where.keys():
            res = res + "AND (" + f + "=" + \
                  self._sqlQuote(table, table.fields[f], where[f]) + ")"

        res = res[4:] # strip first AND
        return " WHERE (" + res + ")"

    def _sqlQuote(self, table, field, value):
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


