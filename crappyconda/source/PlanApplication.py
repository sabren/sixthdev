# Initializes the application
import Workshop

class PlanApplication(Workshop.WorkshopApp):

	# Renders the Goal List Page
    def render_list_goal(self, model):
        return "rendering list goals..."
		
	# Renders the Task List Page
	def render_list_task(self, model):
		return "rendering task list..."
	
	# Renders the User List Page
	def render_list_user(self, model):
		return "rendering user list..."
	
	# Renders the Plan Page
	def render_plan_list(self, model):
		return "rendering plan..."
	