# Test Class for the User object
import unittest

from Planaconda import User

class UserTest(unittest.TestCase):

	def setUp(self):
		self.user = User(ID=1000, name="Durran Jordan", password="password", role="Developer", tasks="Tasks")
		
	# Test the name setter
	def testGetName(self):
		self.assertEquals(self.user.name, "Durran Jordan")
		
	# Test the password setter
	def testGetPassword(self):
		self.assertEquals(self.user.password, "password")
	
	# Test the role setter
	def testGetRole(self):
		self.assertEquals(self.user.role, "Developer")
		
	# Test the tasks setter
	def testGetTasks(self):
		self.assertEquals(self.user.tasks, "Tasks")
		
	# Test the id setter
	def testGetId(self):
		self.assertEquals(self.user.ID, 1000)
	

if __name__=="__main__":
    unittest.main()