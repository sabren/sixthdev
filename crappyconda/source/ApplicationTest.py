# Testing for procedures relating to the entire application
import handy
import unittest
import zebra

from arlo import *
from Planaconda import *
from Workshop import WorkshopApp
from Controller import Controller
from PlanApplication import PlanApplication

class ApplicationTest(unittest.TestCase):

	# Create the dummy Goals, Tasks, Users, Plan
    def setUp(self):
        self.clerk = MockClerk()
        self.clerk.store(Goal(name="goal_1"))
        self.clerk.store(Goal(name="goal_2", note="note"))
        self.clerk.store(Task(name="task_1"))
        self.clerk.store(Task(name="task_2", note="note"))
        self.clerk.store(Task(name="task_3"))
        self.clerk.store(User(name="Durran Jordan", login="djordan"))
        self.clerk.store(User(name="Michal Wallace"))
        self.clerk.store(Plan())		
		
		
	# Testing the listing of goals in the Controller
    def testListGoals(self):
        g = Controller(self.clerk).list_goal()
        assert len(g) == 2
		
	# Test the rendering of the goal list
	def testRenderListGoals(self):
		assert hasattr(PlanApplication, "render_list_goal"), \
               "PlanApp should have render_list_goal method"
        
        class TestPlanApplication(PlanApplication):
            def render_list_goal(self, model):
                template = zebra.old_parse(handy.trim(
                    """
                    * for each:
                        {:name:}
                    """))
                return template.fetch(model)
        
        a = TestPlanApplication(Controller(self.clerk),
                    {"action":"list", "what":"goal"})
       
        html = a.act()
        self.assertEquals(html.strip(), "goal_1\ngoal_2")
		
		
	# Testing for listing of tasks in the Controller
	def testListTasks(self):
		t = Controller(self.clerk).list_task()
		assert len(t) == 3
		
	# Test the rendering of the task list
	def testRenderListGoals(self):
		assert hasattr(PlanApplication, "render_list_task"), \
               "PlanApp should have render_list_task method"
        
        class TestPlanApplication(PlanApplication):
            def render_list_task(self, model):
                template = zebra.old_parse(handy.trim(
                    """
                    * for each:
                        {:name:}
                    """))
                return template.fetch(model)
        
        a = TestPlanApplication(Controller(self.clerk),
                    {"action":"list", "what":"task"})
       
        html = a.act()
        self.assertEquals(html.strip(), "task_1\ntask_2\ntask_3")		
		
		
	# Testing for listing of Users in the Controller
	def testListUsers(self):
		u = Controller(self.clerk).list_user()
		assert len(u) == 2
		
	# Test the rendering of the user list
	def testRenderListGoals(self):
		assert hasattr(PlanApplication, "render_list_user"), \
               "PlanApp should have render_list_user method"
        
        class TestPlanApplication(PlanApplication):
            def render_list_user(self, model):
                template = zebra.old_parse(handy.trim(
                    """
                    * for each:
                        {:name:}
                    """))
                return template.fetch(model)
        
        a = TestPlanApplication(Controller(self.clerk),
                    {"action":"list", "what":"user"})
       
        html = a.act()
        self.assertEquals(html.strip(), "Durran Jordan\nMichal Wallace")	
		
		
	# Testing the Plan list.
	def testListPlan(self):
		p = Controller(self.clerk).list_plan()
		assert len(p) == 1
		

if __name__=="__main__":
    unittest.main()
