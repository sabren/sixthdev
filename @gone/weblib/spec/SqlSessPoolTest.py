
import weblib
import unittest

#@TODO: put sqlTest in the directory
#import sqlTimesheet as sqlTest

class SqlSessPoolTest(unittest.TestCase):

    def testPutSess(self):
        sp = weblib.SessPool.SqlSessPool(sqlTest.dbc)
        cur = sqlTest.dbc.cursor()
        cur.execute("delete from web_sess")
        for x in range(500):
            sp.putSess("name", "sid", "frozensess")
            cur.execute("select * from web_sess")
            assert cur.rowcount == 1, "expected one row, got:\n%s" \
                   % str(cur.fetchall())

if __name__=="__main__":
    unittest.main()



