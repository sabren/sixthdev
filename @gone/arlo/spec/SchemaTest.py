
import unittest
from strongbox import *
from arlo import Schema

class Loop(Strongbox):
    next = link(forward)
    tree = linkset(forward, "next")
Loop.next.type = Loop
Loop.tree.type = Loop

class SchemaTest(unittest.TestCase):

    def test_schema(self):
        s = Schema({
            Loop: "loop_table",
            Loop.next: "nextID",
        })
        assert s.tableForClass(Loop) == "loop_table"
        assert s.columnForLink(Loop.next) == "nextID"

        # it should be smart enough to infer these:
        assert s.tableForLink(Loop.next) == "loop_table"
        assert s.tableForLinkSet(Loop.tree) == "loop_table"
        assert s.columnForLinkSet(Loop.tree) == "nextID"


if __name__=="__main__":
    unittest.main()
