# The Contoller for the Planaconda app
from Planaconda import *

class Controller:

    def __init__(self, clerk):
        self.clerk = clerk

	# Lists the goals for the application
    def list_goal(self):
        return self.clerk.match(Goal)
		
	# Lists the tasks for the application
	def list_task(self):
		return self.clerk.match(Task)
		
	# Lists the users for the application
	def list_user(self):
		return self.clerk.match(User)
		
	# Lists the plan for the application
	def list_plan(self):
		return self.clerk.match(Plan)
	