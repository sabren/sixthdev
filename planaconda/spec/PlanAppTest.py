
from planaconda import PlanApp
import weblib
import unittest

class PlanAppTest(unittest.TestCase):
    def test_viewListProject(self):
        r = weblib.RequestBuilder().build()
        p = PlanApp(r)
        m = p.viewListProject()
        assert m['projects'] == []

if __name__=="__main__":
    unittest.main()
