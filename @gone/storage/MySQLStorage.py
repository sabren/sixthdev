from storage import Storage
from pytypes import Date

#from SQLQueryBuilder import *

class MySQLStorage(Storage):
    #qb = SQLQueryBuilder
    #q = SQLQueryBuilder()

    def __init__(self, dbc):
        self.dbc = dbc
        self.cur = dbc.cursor()


    def _dictify(self, cur):
        """
        converts cursor.fetchall() results into a list of dicts
        """
        res = []
        for row in cur.fetchall():
            d = {}
            for i in range(len(cur.description)):
                d[cur.description[i][0]] = row[i]
            res.append(d)
        return res


    def _toSQLString(self, val):
        """
        Turns a value into a quoted string suitable for MySQL
        """
        if isinstance(val, Date) and str(val)=='0-0-0':                
            return "NULL"
        elif val is None:
            return "NULL"
        else:
            return "'" + "''".join(str(val).split("'")) + "'"
            

    def _insert_main(self, table, **row):
        # generate column/value lists for INSERT
        cols = ', '.join(row.keys())
        vals = ', '.join([self._toSQLString(v) for v in row.values()])

        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, vals)
        self._execute(sql)

        return self._getInsertID()

    def _insert(self, table, **row):
        id = self._insert_main(table, **row)
        return self.fetch(table, id)

    def _getInsertID(self):
        # new way:
        if hasattr(self.cur, "insert_id"):
            return self.cur.insert_id()
        elif hasattr(self.cur, "_insert_id"):
            return self.cur._insert_id
        else:
            raise Exception("insert_id not found!") 


    def _update(self, table, **row):

        sql = "UPDATE " + table + " SET"
        for col,val in row.iteritems():
            sql += " " + col + "=" + self._toSQLString(val) + ","
        sql = sql[:-1]

        # whoops! thanks to Andy Todd for this line:
        sql += " WHERE ID = %d" % row["ID"]

        self._execute(sql)
        return self.fetch(table, row["ID"])
        

    def _match(self, table, where=None, orderBy=None):
        # RICK: building query not needed with QueryBuilder obj
        sql = ["SELECT * FROM %s" % table]
        
        # RICK: changed to use QueryBuilder obj
        if where is not None:
            sql.append(" WHERE %s" % str(where))
        if orderBy is not None:
            sql.append(" ORDER BY %s" % orderBy)
        sql = ''.join(sql)
        self._execute(sql)
        return self._dictify(self.cur)
        

    def delete(self, table, ID):
        # RICK: allows deleting by criteria or ID
        if type(ID) == int:
            self._execute("DELETE FROM %s WHERE ID=%s" % (table, ID))
        else:
            self._execute("DELETE FROM %s WHERE %s" % (table, str(ID)))

    def _execute(self, sql):
        try:
            self.cur.execute(sql)
        except Exception, e:
            raise Exception, str(e) + ":" + sql
