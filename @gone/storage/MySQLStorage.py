from storage import Storage

class MySQLStorage(Storage):

    def __init__(self, dbc):
        self.dbc = dbc
        self.cur = dbc.cursor()


    def _dictify(self, cur):
        """converts cursor.fetchall() results into a list of dicts"""
        res = []
        for row in cur.fetchall():
            d = {}
            for i in range(len(cur.description)):
                d[cur.description[i][0]] = row[i]
            res.append(d)
        return res


    def _insert(self, table, **row):

        # generate column/value lists for INSERT
        cols, vals = "", ""
        for col,val in row.iteritems():
            cols += col + ","
            # ok for numbers in mysql
            vals += "'" + str(val) + "',"

        # strip off last commas:
        cols = cols[:-1]
        vals = vals[:-1]

        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, vals)
        self._execute(sql)

        # we read from DB in case of timestamps, etc:
        ID = self.cur._insert_id
        return self.fetch(table, ID)
        

    def _update(self, table, **row):

        sql = "UPDATE " + table + " SET"
        for col,val in row.iteritems():
            sql += " " + col + "='" + str(val) + "',"
        sql = sql[:-1]

        # whoops! thanks to Andy Todd for this line:
        sql += " WHERE ID = %d" % row["ID"]

        self._execute(sql)
        return self.fetch(table, row["ID"])
        

    def match(self, table, **where):
        criteria = []
        for col,val in where.iteritems():
            criteria.append(col + "='" + str(val) + "'")

        sql = "SELECT * FROM " + table
        if criteria:
            sql += " WHERE " + " AND ".join(criteria)
            
        self._execute(sql)
        return self._dictify(self.cur)
        

    def delete(self, table, ID):
        self._execute("DELETE FROM %s WHERE ID=%s" % (table, ID))

    def _execute(self, sql):
        try:
            self.cur.execute(sql)
        except Exception, e:
            raise sql
