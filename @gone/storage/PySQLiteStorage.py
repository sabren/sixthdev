from storage import Storage
from pytypes import Date
from storage import MySQLStorage

class PySQLiteStorage(MySQLStorage):

    def _getInsertID(self):
        return self.cur.con.db.sqlite_last_insert_rowid()
    def _execute(self, sql):
        super(PySQLiteStorage, self)._execute(sql)
        self.cur.con.commit()

    def _insert_main(self, table, **row):
        id = super(PySQLiteStorage, self)._insert_main(table, **row)
        self._execute("UPDATE %s SET ID=%s where ID IS NULL"
                      % (table, id))
        return id
      
