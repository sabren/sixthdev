# Test Class for the Goal object
import unittest

from Planaconda import Goal

class GoalTest(unittest.TestCase):

	def setUp(self):
		self.goal = Goal(name="Test Goal", note="Test Goal Note", parent="Parent", ID=1000, order=4, subgoals="Sub Goals", tasks="Tasks")
		
	# Test the name setter
	def testGetName(self):
		self.assertEquals(self.goal.name, "Test Goal")
		
	# Test the note setter
	def testGetNote(self):
		self.assertEquals(self.goal.note, "Test Goal Note")
	
	# Test the Parent setter
	def testGetParent(self):
		self.assertEquals(self.goal.parent, "Parent")
		
	# Test the ID Setter
	def testGetId(self):
		self.assertEquals(self.goal.ID, 1000)
		
	# Test the priority/sort order
	def testGetOrder(self):
		self.assertEquals(self.goal.order, 4)
		
	# Test the Sub Goals setter
	def testGetSubGoals(self):
		self.assertEquals(self.goal.subgoals, "Sub Goals")
		
	# Test the Task setter
	def testGetTasks(self):
		self.assertEquals(self.goal.tasks, "Tasks")
	

if __name__=="__main__":
    unittest.main()