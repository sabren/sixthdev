# The test class for the controller
import unittest

from Controller import Controller
from Planaconda import *
from arlo import *

class ControllerTest(unittest.TestCase):

	def setUp(self):
		self.clerk = MockClerk()
		self.clerk.store(Goal(name="Test Goal 1"))
		self.clerk.store(Goal(name="Test Goal 2"))
		self.clerk.store(Task(name="Test Task 1"))
		self.clerk.store(Task(name="Test Task 2"))
		self.clerk.store(User(name="Durran"))
		self.clerk.store(User(name="Michal"))
		self.clerk.store(Plan())
		self.controller = Controller(self.clerk)
		
	# Test the listing of goals
	def testListGoals(self):
		g = self.controller.list_goal()
		assert len(g) == 2
		
	# Test the listing of tasks
	def testListTasks(self):
		t = self.controller.list_task()
		assert len(t) == 2
		
	# Test the user list
	def testListUsers(self):
		u = self.controller.list_user()
		assert len(u) == 2
		
	# test the plan list
	def testListPlan(self):
		p = self.controller.list_plan()
		assert len(p) == 1
	

if __name__=="__main__":
    unittest.main()