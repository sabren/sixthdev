
## SessPool : for holding frozen Sesses :) ##########################

class DumbSessPool:

    """The default SessPool uses a dumbdb file.
    You should subclass this, or just build your own object with the
    same interface (getSess(), setSess(), and drain())..."""
    
    def __init__(self, filename):
        import dumbdbm
        self.storage = dumbdbm.open(filename,"c")
        
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



class DBSessPool:
    """This class uses a DB-API 2.0 compliant Connection object."""

    def __init__(self, dbc, table='web_sess'):
        self.dbc = dbc
        self.table = table


    def getSess(self, name, sid):
        cur = self.dbc.cursor()
        cur.execute("select sess from " + self.table + \
                    " where name='" + name + "' and sid='" + sid + "'")
        row = cur.fetchone()
        if row is None:
            return row
        else:
            return row[0]


    def putSess(self, name, sid, frozensess):
        cur = self.dbc.cursor()
        cur.execute("update " + self.table + \
                    "set sess='" + frozensess + "', tsWhen=now() " + \
                    "where name='" + name + "' and sid='" + sid "'")
        if cur.rowcount == 0:
            cur.execute("insert into " + self.table + " (sid, name, sess, tsWhen) " + \
                        "values ('" + sid + "', '" + name + "', '" + sess + "')")
            

    def drain(self, name, beforeWhen):
        cur = self.dbc.cursor()
        cur.execute("delete from " + self.table + \
                    " where name='" + name + "' and tsWhen < '" + beforeWhen + "'")
