from storage import Storage, QueryBuilder
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
        sql = ["SELECT * FROM %s" % table]
        if where is not None:
            sql.append(" WHERE %s" % str(where))
        if orderBy is not None:
            sql.append(" ORDER BY %s" % orderBy)
        sql = ''.join(sql)
        self._execute(sql)
        return self._dictify(self.cur)
        

    def delete(self, table, where):
        if isinstance(where, QueryBuilder):
            self._execute("DELETE FROM %s WHERE %s" % (table, str(where)))
        else:
            # might be a string, int, or long
            self._execute("DELETE FROM %s WHERE ID=%s" % (table, where))

    def _execute(self, sql):
        import MySQLdb
        self.maxAttempts = 3
        attempt = 0
        while attempt < self.maxAttempts:
            # trap for OperationalError: usually means the db is down.
            try:
                self.cur.execute(sql)
                break
            except MySQLdb.OperationalError:
                attempt += 1
            except Exception, e:
                raise Exception, str(e) + ":" + sql
        else:
            raise Exception, "couldn't connect after %s tries" % attempt
