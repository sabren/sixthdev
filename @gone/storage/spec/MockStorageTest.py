from storage import MockStorage
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
        results = self.s.match("test_person",ID=1)
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
