
from planaconda import PlanApp
import unittest

class PlanAppTest(unittest.TestCase):
    def test_viewListProject(self):
        p = PlanApp()
        m = p.viewListProject()
        assert m['projects'] == []

if __name__=="__main__":
    unittest.main()
