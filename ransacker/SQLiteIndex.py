
__ver__="$Id$"

import anydbm
import metakit
import ransacker

def esc(s):
    return s.replace("'","''")


class SQLiteIndex(ransacker.Index):
    """
    An index that uses SQLite as the backend.
    """

    def __init__(self, path):
        import sqlite, os
        new = not os.path.exists(path)
        self.dbc = sqlite.connect(path)
        self.cur = self.dbc.cursor()
        if new:
            self._makeTables()

    def addDocument(self, name, text):
        super(SQLiteIndex, self).addDocument(name, text)
        self.dbc.commit()

    def _makeTables(self):
        self.cur.execute(
            """           
            create table idx_word (
               ID integer primary key,
               word varchar(32) unique
            )
            """)
        self.cur.execute(
            """           
            create table idx_freq (
               name  varchar(32),
               wordID integer,
               count integer
            )
            """)
        self.dbc.commit()
        
    def _storeFreq(self, name, word, count):
        self.cur.execute(
            """
            INSERT OR IGNORE INTO idx_word (word) VALUES ('%s')
            """ % esc(word))
        self.cur.execute(
            """
            INSERT INTO idx_freq (name, wordID, count)
            VALUES ('%s', (SELECT ID FROM idx_word WHERE word='%s'), %s)
            """ % (esc(name), esc(word), count))

    def score(self, word):        
        sql =(
            """
            SELECT name, count from idx_freq f, idx_word w
            WHERE f.wordID=w.ID and w.word='%s'
            ORDER BY count DESC
            """ % esc(word))
        self.cur.execute(sql)
        #print sql
        #res = self.cur.fetchall()
        #for row in res:
        #    print ">>", row
        #return tuple(row)
        return tuple(self.cur.fetchall())
   

    def contains(self, name):
        self.cur.execute("select name from idx_freq where name='%s'"
                         % esc(name))
        return self.cur.fetchone() is not None

    def close(self):
##         self.cur.execute("select * from idx_word")
##         for row in self.cur.fetchall():
##             print row
##         self.cur.execute("select * from idx_freq")
##         for row in self.cur.fetchall():
##             print row
        self.dbc.close()
        
