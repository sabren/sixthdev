
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

    def test_viewNode(self):
        n = self.c.store(Node(name="abc"))
        self.p.input["ID"] = n.ID
        m = self.p.viewNode()
        assert m["name"] == "abc"
        
        
if __name__=="__main__":
    unittest.main()
