
from MockStorageTest import *
from storage import MySQLStorage

class MySQLStorageTest(MockStorageTest):

    def setUp(self):
        try:
            import sqlTest
        except ImportError:
            raise "skip"
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


    def check_store_quotes(self):
        self.populate()
        row = self.s.fetch("test_person", 1)
        row["name"] = "j'mo\"cha's'ha''ha"
        self.s.store("test_person", **row)
        assert self.wholedb() == [{"ID":1, "name":"j'mo\"cha's'ha''ha"},
                                  {"ID":2, "name":"wanda"}]        
        




    # other test are inherited from MockStorage...
