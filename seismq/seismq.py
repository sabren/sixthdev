"""
seismq: sei's message queue
"""
__ver__="$Id$"

import sqlite3 as sqlite
import time
   
def open(filename):
    return MQ(filename)

class MQ(object):
    """
    I implement the message queue.
    """

    def __init__(self, filename):
        self.dbc = sqlite.connect(filename)
        if not self.hasTable():
            self.createTable()

    def createTable(self):
        cur = self.dbc.cursor()
        cur.execute(
            """
            CREATE TABLE queue (
               ID integer PRIMARY KEY,
               ts time_stamp,
               message text )
            """)
        self.dbc.commit()

    def hasTable(self):
        cur = self.dbc.cursor()
        cur.execute(
            """
            SELECT * FROM sqlite_master
            WHERE type='table' and name='queue'
            """)
        return bool(cur.fetchone())
    
    def send(self, msg):
        cur = self.dbc.cursor()
        cur.execute(
            """
            INSERT INTO queue (ts,message) VALUES ('%s', '%s')
            """ % (self.timestamp(), msg))
        self.dbc.commit()

    def count(self, msg):
        cur = self.dbc.cursor()
        cur.execute(
            """
            SELECT COUNT(*) FROM queue WHERE message='%s'
            """ % msg)
        return cur.fetchone()[0]

    def take(self, msg):
        cur = self.dbc.cursor()        
        now = self.timestamp()
        # The edge case is that the select runs, and then a
        # message comes in from another process, and then
        # the delete runs, deleting the new message.
        #
        # Unfortunately, pySQLite doesn't include SELECT
        # statements in its transactions. You're supposed
        # to be able to use autocommit=1, but that didn't
        # work, and neither did autocommit=0, which would
        # make more sense. Hence timestamps.
        #
        # It's probably overkill since the earlier copies
        # of the message are going to be processed anyway,
        # but by the time I'd realized that, I'd already
        # done the right thing. :)
        cur.execute(
            """
            SELECT message FROM queue
            WHERE message='%s' AND ts <= '%s'
            """ % (msg, now))
        res = [row[0] for row in cur.fetchall()]
        if res:
            cur.execute(
                """
                DELETE FROM queue
                WHERE message='%s' AND ts<='%s'
                """ % (msg, now))
            self.dbc.commit()
        return res

    def timestamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def close(self):
        self.dbc.close()
