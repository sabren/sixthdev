# Test Class for the Task object
import unittest

from Planaconda import Task

class TaskTest(unittest.TestCase):

	def setUp(self):
		self.task = Task(ID=1000, name="Task", note="Task Note", goal="Goal", originalEstimate=10, currentEstimate=5, actualHours=8, owner="Durran Jordan", status="Open")
		
	# Test the name setter
	def testGetName(self):
		self.assertEquals(self.task.name, "Task")
		
	# Test the note setter
	def testGetNote(self):
		self.assertEquals(self.task.note, "Task Note")
		
	# Test the Goal setter
	def testGetGoal(self):
		self.assertEquals(self.task.goal, "Goal")
		
	# Test the Original Estimate setter
	def testGetOriginalEstimate(self):
		self.assertEquals(self.task.originalEstimate, 10)
		
	# Test the Current Estimate setter
	def testGetCurrentEstimate(self):
		self.assertEquals(self.task.currentEstimate, 5)
		
	# Test the Actual Hours Worked setter
	def testGetActualHours(self):
		self.assertEquals(self.task.actualHours, 8)
		
	# Test the Owner setter
	def testGetOwner(self):
		self.assertEquals(self.task.owner, "Durran Jordan")
	
	# test the status setter
	def testGetStatus(self):
		self.assertEquals(self.task.status, "Open")
		
	# Test the id setter
	def testGetId(self):
		self.assertEquals(self.task.ID, 1000)
	

if __name__=="__main__":
    unittest.main()