
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
        assert m["ntype"] == "task"
        
if __name__=="__main__":
    unittest.main()
