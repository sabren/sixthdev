"""
SessPool.py : classes for holding frozen Sesses :)
"""
__ver__="$Id$"

class SessPool:
    """
    The default SessPool uses an anydbm file.
    You should subclass this, or just build your own object with the
    same interface (getSess(), setSess(), and drain())...
    """

    #@TODO: this isn't backed up with test cases..
    
    def __init__(self, filename):
        import anydbm
        self.storage = anydbm.open(filename,"c")
        
    def getSess(self, name, sid):
        """returns the sess with the specified name and id, or None"""
        if self.storage.has_key(`name`+`sid`):
            return self.storage[`name` + `sid`]
        else:
            return None

    def putSess(self, name, sid, frozensess):
        """stores a frozen sess with the specified name and id"""
        self.storage[`name` + `sid`] = frozensess

    def drain(self, name, beforewhen):
        """(should) performs garbage collection to kill off old sesses"""
        # 'cept this is just a dummy version, and it don't do nuttin. :)
        pass



class SqlSessPool:
    """
    This uses a DB-API 2.0 compliant Connection object to store Sessions.
    """

    def __init__(self, dbc, table='web_sess'):
        self.dbc = dbc
        self.table = table


    def getSess(self, name, sid):
        cur = self.dbc.cursor()
        cur.execute("select sess from " + self.table + \
                    " where name='" + name + "' and sid='" + sid + "'")

        try:
            ## GRR.. the win32 mysql has a problem with this..
            #@TODO: find a way to isolate stuff like this..
            row = cur.fetchone()
        except:
            row = None
            
        if row is None:
            return row
        else:
            return row[0]


    def putSess(self, name, sid, frozensess):
        import string
        
        frozen = string.replace(frozensess, "'", "\\'")

        cur = self.dbc.cursor()
        sql = "update " + self.table + " " + \
              "set sess='" + frozen + "', tsUpdate=now() " + \
              "where name='" + name + "' and sid='" + sid + "'"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur.execute(
                """
                INSERT INTO %s (sid, name, sess, tsUpdate) 
                VALUES ('%s', '%s', '%s', now())
                """ % (self.table, sid, name, frozen))
            

    def drain(self, name, beforeWhen):
        cur = self.dbc.cursor()
        #@TODO: cleanup beforeWhen (garbage collection)
        sql =\
            """
            DELETE FROM %s WHERE name='%s' and tsUpdate < ''
            """ % (self.table, name, `beforeWhen`)
        cur.execute(sql)
