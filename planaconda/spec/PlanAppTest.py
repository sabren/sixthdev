
from planaconda import PlanApp, Node
from planaconda.config import DBMAP
import weblib
import unittest
import arlo

class PlanAppTest(unittest.TestCase):

    def setUp(self):
        self.c = arlo.MockClerk(DBMAP)
        self.r = weblib.RequestBuilder().build()
        self.p = PlanApp(self.c, self.r)

    def test_viewListProject(self):
        m = self.p.viewListProject()
        assert m['projects'] == []
        self.c.store(Node(name="top", ntype="project"))
        m = self.p.viewListProject()
        assert len(m["projects"]) == 1
        assert m['projects'][0]["name"] == "top"

    def test_formEditNode(self):
        m = self.p.formEditNode()
        assert m["nodes"] == [(0, "/")]
        assert m["ntype"] == "task"

    def test_postSaveNode(self):
        assert len(self.c.match(Node)) == 0
        self.p.input["name"] = "post me"
        self.p.input["parent"] = 0
        self.assertRaises(weblib.Redirect, self.p.postSaveNode)
        nodes = self.c.match(Node)
        assert len(nodes) == 1
        self.assertEquals("post me", nodes[0].name)

    def test_viewNode_root(self):
        
        self.p.input["ID"] = 0
        m = self.p.viewNode()
        self.assertEquals("root", m["name"])
        self.assertEquals(0, len(m["children"]))
        
        n = self.c.store(Node(name="abc"))

        self.p.input["ID"] = 0
        m = self.p.viewNode()
        self.assertEquals("root", m["name"])
        self.assertEquals(1, len(m["children"]))

    def test_viewNode_node(self):
        n = self.c.store(Node(name="abc"))
        self.p.input["ID"] = n.ID
        m = self.p.viewNode()
        assert m["name"] == "abc"
        self.assertEquals([], m["crumbs"])

    def test_viewPlate(self):
        # mmm... vowels...
        self.c.store(Node(name="a", isOnPlate=True, importance=6))
        self.c.store(Node(name="b"))
        self.c.store(Node(name="c"))
        self.c.store(Node(name="d"))
        self.c.store(Node(name="e", isOnPlate=True, importance=3))
        self.c.store(Node(name="f"))
        self.c.store(Node(name="g"))
        self.c.store(Node(name="h"))
        self.c.store(Node(name="i", isOnPlate=True, importance=9))

        m = self.p.viewPlate()
        assert len(m["nodes"]) == 3
        self.assertEquals(["e","a","i"],
                          [n["name"] for n in m["nodes"]])
        
        
if __name__=="__main__":
    unittest.main()
