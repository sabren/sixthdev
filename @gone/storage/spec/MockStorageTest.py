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

    def check_store_update(self):
        row = self.s.store("test_person", name="frid")
        assert len(self.s.match("test_person")) == 1

        row["name"] = "fred"
        self.s.store("test_person", **row)
        assert len(self.s.match("test_person")) == 1, "didn't update"

    def check_match(self):
        self.check_store_insert()
        results = self.s.match("test_person", ID=1)
        assert len(results) == 1, results
        fred = results[0]
        assert fred["name"] == "fred"

    def check_fetch(self):
        self.check_store_insert()
        wanda = self.s.fetch("test_person", 2)
        assert wanda["name"]=="wanda"

    def check_delete(self):
        self.check_store_insert()
        self.s.delete("test_person", 1)
        people = self.s.match("test_person")
        assert people == [{"ID":2, "name":"wanda"}]
