##
## GENERATED FILE. DO NOT CHANGE!
##
from strongbox import *
from pytypes import *
from sixthday import AdminApp
import workshop

class Project(Strongbox):
    ID = attr(long)
    name = attr(str)
    data = attr(str)
    goals = linkset(forward)
    pass

class Goal(Strongbox):
    ID = attr(long)
    name = attr(str)
    data = attr(str)
    tasks = linkset(forward)
    pass

class Task(Strongbox):
    ID = attr(long)
    name = attr(str)
    data = attr(str)
    pass

## resolve forward definitions
Goal.__attrs__["tasks"].type=Task
Project.__attrs__["goals"].type=Goal
dbmap = {
    Project: 'plan_project',
    Task: 'plan_task',
    Goal: 'plan_goal',
    Project.__attrs__['goals']: (Goal,'projectID'),
    Goal.__attrs__['tasks']: (Task,'goalID'),
}
class MyAdminApp(AdminApp):
    def list_project(self):
        self.write(workshop.generic_list(self.clerk, Project))
    def list_goal(self):
        self.write(workshop.generic_list(self.clerk, Goal))
    def list_task(self):
        self.write(workshop.generic_list(self.clerk, Task))
    def act_(self):
        self.write("""
<ul>
<li><a href="work.app?action=list&what=project">Project</a></li>
<li><a href="work.app?action=list&what=goal">Goal</a></li>
<li><a href="work.app?action=list&what=task">Task</a></li>
</ul>
        """)

if __name__=="__main__":
    from arlo import Clerk
    from sqlPair import dbc
    from storage import MySQLStorage
    CLERK = Clerk(MySQLStorage(dbc), dbmap)
    print >> RES, MyAdminApp(CLERK, REQ).act()
