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
        if self.storage.has_key(str(name)+str(sid)):
            return self.storage[str(name)+str(sid)]
        else:
            return None

    def putSess(self, name, sid, frozensess):
        """stores a frozen sess with the specified name and id"""
        self.storage["newkey"]="newval"
        self.storage[str(name)+str(sid)] = frozensess


    def drain(self, name, beforewhen):
        """(should) performs garbage collection to kill off old sesses"""
        # 'cept this is just a dummy version, and it don't do nuttin. :)
        pass

    def done(self):
        self.storage.close()

class InMemorySessPool(SessPool):
    """
    Just uses a dictionary.
    
    **NOTE**: this WON'T WORK with, eg, mod_python unless you only
    use a single instance of apache, because the dictionary is
    local to a single python interpreter, and apache wants to have
    several...
    """
    def __init__(self, dict=None):
        if dict:
            self.storage = dict
        else:
            self.storage = {}

    def done(self):
        pass


class SqlSessPool:
    """
    This uses a DB-API 2.0 compliant Connection object to store Sessions.
    It expects a table like:

    CREATE TABLE web_sess (
        name varchar(32),
        sid varchar(64),
        sess blob,
        tsUpdate timestamp,
        primary key (name, sid)
    );
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
        
	frozen = string.replace(frozensess, "'", "''")

        cur = self.dbc.cursor()
        sql = "REPLACE " + self.table + " " + \
              "set sess='" + frozen + "', tsUpdate=now(), " + \
              "name='" + name + "', sid='" + sid + "'"
        cur.execute(sql)


    def drain(self, name, beforeWhen):
        cur = self.dbc.cursor()
        #@TODO: cleanup beforeWhen (garbage collection)
        sql =\
            """
            DELETE FROM %s WHERE name='%s' and tsUpdate < '%s'
            """ % (self.table, name, `beforeWhen`)
        cur.execute(sql)

    def done(self):
        pass
