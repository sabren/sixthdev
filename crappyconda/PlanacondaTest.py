
import handy
import unittest
from arlo import *
from planaconda import Goal, PlanSession, PlanApp
from workshop import WorkshopApp
import zebra


class PlanacondaTest(unittest.TestCase):

    def setUp(self):
        self.clerk = MockClerk()
        self.clerk.store(Goal(name="goal1"))
        self.clerk.store(Goal(name="goal2", note="note"))        

    def test_sesion(self):
        g = PlanSession(self.clerk).list_goal()
        assert len(g) == 2

    def test_app(self):

        assert hasattr(PlanApp, "render_list_goal"), \
               "PlanApp should have render_list_goal method"
        
        class TestPlanApp(PlanApp):
            def render_list_goal(self, model):
                template = zebra.old_parse(handy.trim(
                    """
                    * for each:
                        {:name:}
                    """))
                return template.fetch(model)
        
        a = TestPlanApp(PlanSession(self.clerk),
                    {"action":"list", "what":"goal"})
       
        html = a.act()
        self.assertEquals(html.strip(), "goal1\ngoal2")






if __name__=="__main__":
    unittest.main()
