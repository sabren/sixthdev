# Generates all the objects for use in the Planaconda project.
import Workshop

# Generate the code for the Goal class
# Valid attributes are: id, name, note, parent goal, sort order
# associated sub goals, associated tasks
_goal = Workshop.ProtoClass(name="Goal")
_goal.attrs << Workshop.ProtoAttr(name="ID", type="long")
_goal.attrs << Workshop.ProtoAttr(name="name", type="str")
_goal.attrs << Workshop.ProtoAttr(name="note", type="str")
_goal.attrs << Workshop.ProtoAttr(name="parent", type="str")
_goal.attrs << Workshop.ProtoAttr(name="order", type="int")
_goal.attrs << Workshop.ProtoAttr(name="subgoals", type="str")
_goal.attrs << Workshop.ProtoAttr(name="tasks", type="str")

# Generate the code for the User class
# Valid attributes are: id, user's name, login, password,
# role, assigned tasks
_user = Workshop.ProtoClass(name="User")
_user.attrs << Workshop.ProtoAttr(name="ID", type="long")
_user.attrs << Workshop.ProtoAttr(name="name", type="str")
_user.attrs << Workshop.ProtoAttr(name="login", type="str")
_user.attrs << Workshop.ProtoAttr(name="password", type="str")
_user.attrs << Workshop.ProtoAttr(name="role", type="str")
_user.attrs << Workshop.ProtoAttr(name="tasks", type="str")

# Generate the code for the Task class
# Valid attribtues are: id, name, note, goal, original estimate, 
# actual estimate, actual hours worked, owner of the task, status
_task = Workshop.ProtoClass(name="Task")
_task.attrs << Workshop.ProtoAttr(name="ID", type="long")
_task.attrs << Workshop.ProtoAttr(name="name", type="str")
_task.attrs << Workshop.ProtoAttr(name="note", type="str")
_task.attrs << Workshop.ProtoAttr(name="goal", type="str")
_task.attrs << Workshop.ProtoAttr(name="originalEstimate", type="int")
_task.attrs << Workshop.ProtoAttr(name="currentEstimate", type="int")
_task.attrs << Workshop.ProtoAttr(name="actualHours", type="int")
_task.attrs << Workshop.ProtoAttr(name="owner", type="str")
_task.attrs << Workshop.ProtoAttr(name="status", type="str")

# Generate the code for the Plan Class
# Valid attribtues are: id, tasks
_plan = Workshop.ProtoClass(name="Plan")
_plan.attrs << Workshop.ProtoAttr(name="ID", type="long")
_plan.attrs << Workshop.ProtoAttr(name="tasks", type="str")

# Create the model and add all the classes to it
_model = Workshop.Model()
_model.add(_goal)
_model.add(_user)
_model.add(_task)
_model.add(_plan)

# Open a new file, and send the generated code to that file for
# use with the rest of the application
out = open("Planaconda.py", "w")
print >> out, _model.asCode()
out.close()