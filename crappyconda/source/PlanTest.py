# Test Class for the Plan object
import unittest

from Planaconda import Plan

class UserTest(unittest.TestCase):

	def setUp(self):
		self.user = Plan(ID=1000, tasks="Tasks")
		
	# Test the tasks setter
	def testGetTasks(self):
		self.assertEquals(self.user.tasks, "Tasks")
		
	# Test the id setter
	def testGetId(self):
		self.assertEquals(self.user.ID, 1000)
	

if __name__=="__main__":
    unittest.main()