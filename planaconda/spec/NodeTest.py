
from planaconda import Node, Comment
from planaconda.config import DBMAP
from arlo import MockClerk
import unittest

class NodeTest(unittest.TestCase):

    def test_comments(self):
        n = Node()
        c = Comment(content="blah blah blah")
        n.comments << c
        assert n.comments == [c]


    def test_path(self):
        t = Node(name="top")
        n = Node(name="asdf", parent=t)
        n.name = "asdf" # @TODO: this line should not be required!!
        assert n.path=="/top/asdf", n.path
        raise "skip"


    def test_recursion_bug(self):
        p = Node(name="project")
        g = Node(name="goal")
        p.children << g

        m = MockClerk(DBMAP)
        m.store(p)

        n = m.fetch(Node, g.ID)
        assert len(n.crumbs) == 1, len(n.crumbs)
        
        
if __name__=="__main__":
    unittest.main()
