
import unittest
import zikebase.test

from zikebase import Content

## @TODO: first make sure this really is the test database.

class ContentTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("DELETE FROM base_content")

    def check_add(self):
        cont = Content()
        cont.title = "a simple test"
        cont.save()
        del cont

        self.cur.execute("SELECT title FROM base_content WHERE ID=1")
        row = self.cur.fetchone()

        assert row is not None, "adding content failed!"
        assert row[0]=="a simple test", "title wasn't saved!"
        

    def tearDown(self):
	pass
