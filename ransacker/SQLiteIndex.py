
__ver__="$Id$"

import anydbm
import ransacker


class SQLiteIndex(ransacker.Index):
    """
    An index that uses SQLite as the backend.
    """

    def _esc(self, s):
        return s.replace("'","''")

    def __init__(self, path):
        import sqlite, os
        new = not os.path.exists(path)
        self.dbc = sqlite.connect(path)
        self.cur = self.dbc.cursor()
        if new:
            self._makeTables()

    def _registerPage(self, name):
        self.cur.execute(
            """
            INSERT OR IGNORE INTO idx_page (page) VALUES ('%s')
            """ % self._esc(name))

    def _doIndexing(self, name, text):
        self._registerPage(name)
        super(SQLiteIndex, self)._doIndexing(name, text)
        self.dbc.commit()

    def _makeTables(self):
        self.cur.execute(
            """           
            create table idx_page (
               ID integer primary key,
               page varchar(32) unique
            )
            """)
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
               pageID integer,
               wordID integer,
               count  integer
            )
            """)
        self.dbc.commit()
        
    def _storeFreq(self, pageID, word, count):
        self.cur.execute(
            """
            INSERT OR IGNORE INTO idx_word (word) VALUES ('%s')
            """ % self._esc(word))
        self.cur.execute(
            """
            INSERT INTO idx_freq (pageID, wordID, count)
            VALUES (%s,
                    (SELECT ID FROM idx_word WHERE word='%s'),
                    %s)
            """ % (pageID, self._esc(word), count))

    def _getPageID(self, name):
        self.cur.execute("SELECT ID FROM idx_page WHERE page='%s'"
                         % self._esc(name))
        res = self.cur.fetchone()
        if res:
            return res[0]
        else:
            return None
        
        
    def remove(self, name):
        id = self._getPageID(name)
        self.cur.execute("DELETE FROM idx_freq where pageID=%s" % id)
        self.cur.execute("DELETE FROM idx_page where ID=%s" % id)
        self.dbc.commit()

    def score(self, word):        
        sql =(
            """
            SELECT page, count
            FROM idx_freq f, idx_word w, idx_page p
            WHERE f.wordID=w.ID and f.pageID=p.ID and w.word='%s'
            ORDER BY count DESC
            """ % self._esc(word))
        self.cur.execute(sql)
        #print sql
        #res = self.cur.fetchall()
        #for row in res:
        #    print ">>", row
        #return tuple(row)
        return tuple(self.cur.fetchall())
   

    def contains(self, name):
        return self._getPageID(name) is not None


    def close(self):
##         self.cur.execute("select * from idx_word")
##         for row in self.cur.fetchall():
##             print row
##         self.cur.execute("select * from idx_freq")
##         for row in self.cur.fetchall():
##             print row
        self.dbc.close()
        
