from storage import MockStorage, where
import unittest

class MockStorageTest(unittest.TestCase):

    def setUp(self):
        self.s = MockStorage()

    def check_store_insert(self):
        row = self.s.store("test_person", name="fred")
        assert row == {"ID":1, "name":"fred"}

        row = self.s.store("test_person", name="wanda")
        assert row == {"ID":2, "name":"wanda"}

        assert self.wholedb()==[{"ID":1, "name":"fred"},
                                {"ID":2, "name":"wanda"}]

    def check_store_insertExtra(self):
        self.check_store_insert()
        self.s.store("test_person", name="rick")
        self.s.store("test_person", name="bob")
        self.s.store("test_person", name="jack")
        assert self.wholedb()==[{"ID":1, "name":"fred"},
                                {"ID":2, "name":"wanda"},
                                {"ID":3, "name":"rick"},
                                {"ID":4, "name":"bob"},
                                {"ID":5, "name":"jack"}]


    def check_oldmatch(self):
        self.check_store_insertExtra()
        match = self.s.match("test_person", where("ID")==2)
        assert match[0]["name"] == "wanda", "new style broke"
        match = self.s.match("test_person", ID=2)
        assert match[0]["name"] == "wanda", "old style broke"


    def check_querybuilder_matches(self):
        self.check_store_insertExtra()
        match = self.s.match("test_person", where("ID")==5 )
        assert match[0]['name'] == 'jack'

        match = self.s.match("test_person", ( ( where("name")=="fred" )
                                         |  ( where("name")=="bob" ) ), "name")
        self.assertEquals([u['name'] for u in match],
                          ['bob','fred'])
            
        
        
        match = self.s.match("test_person", ((where("ID") > 1)
                                             &(where("ID") <= 4))
                                           |(where("name").endswith('ck')),
                                         'name desc')
        self.assertEquals( [u['name'] for u in match],
                           ['wanda', 'rick', 'jack', 'bob'] )



    def check_querybuilder_sorting(self):
        self.check_store_insertExtra()
        assert [p['name'] for p in self.s.match("test_person", orderBy='name')] == ['bob', 'fred', 'jack', 'rick', 'wanda']

    def populate(self):
        self.check_store_insert()

    def wholedb(self):
        return self.s.match("test_person")

    def check_store_update(self):
        self.populate()
        row = self.s.fetch("test_person", 1)
        row["name"] = "frood"
        self.s.store("test_person", **row)
        assert self.wholedb() == [{"ID":1, "name":"frood"},
                                  {"ID":2, "name":"wanda"}]        

    def check_match(self):
        assert self.wholedb() == []
        self.populate()
        results = self.s.match("test_person", where("ID") == 1)
        assert results == [{"ID":1, "name":"fred"}], str(results)

    def check_fetch(self):
        self.check_store_insert()
        wanda = self.s.fetch("test_person", 2)
        assert wanda["name"]=="wanda"

    def check_delete(self):
        self.check_store_insert()
        self.s.delete("test_person", 1)
        people = self.s.match("test_person")
        assert people == [{"ID":2, "name":"wanda"}]
        self.s.delete("test_person", ID=2)
        people = self.s.match("test_person")
        assert people == []

    def check_delete_with_long_id(self):
        self.check_store_insert()
        self.s.delete("test_person", 1L)
