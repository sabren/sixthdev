import sqlTest
from MockStorageTest import *
from storage import MySQLStorage

class MySQLStorageTest(MockStorageTest):

    def setUp(self):
        self.s = MySQLStorage(sqlTest.dbc)
        cur = sqlTest.dbc.cursor()
        try:
            cur.execute("DELETE FROM test_person")
        except:
            cur.execute(
                """
                CREATE TABLE test_person (
                    ID int not null auto_increment primary key,
                    name varchar(32)
                )
                """)
