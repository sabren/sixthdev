# Initializes the application
import Workshop

class PlanApplication(Workshop.WorkshopApp):

	# Renders the Goal List Page
    def render_list_goal(self, model):
        return zebra.fetch("../gui/goals.html", model)
		
	# Renders the Goal List Page
    def render_list_task(self, model):
        return zebra.fetch("../gui/tasks.html", model)
		
	# Renders the Goal List Page
    def render_list_user(self, model):
        return zebra.fetch("../gui/users.html", model)
		
	# Renders the Goal List Page
    def render_list_plan(self, model):
        return zebra.fetch("../gui/plans.html", model)				