##
## GENERATED FILE. DO NOT CHANGE!
##
from strongbox import *
from pytypes import *
from sixthday import AdminApp
import prototype

class Project(Strongbox):
    ID = attr(long)
    name = attr(str)
    data = attr(str)
    goals = linkset(forward, 'project')
    pass

class Goal(Strongbox):
    ID = attr(long)
    name = attr(str)
    data = attr(str)
    project = link(Project)
    tasks = linkset(forward, None)
    pass

class Task(Strongbox):
    ID = attr(long)
    name = attr(str)
    data = attr(str)
    goal = link(Goal)
    pass

class Class(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    pass

class Attr(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    type = attr(str)
    okay = attr(str)
    init = attr(str)
    size = attr(int)
    pass

class Link(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    classID = attr(int)
    otherID = attr(long)
    joinID = attr(long)
    field = attr(str)
    pass

class Join(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    classID = attr(long)
    otherID = attr(long)
    field = attr(str)
    pass

## resolve forward definitions
Goal.__attrs__["tasks"].type=Task
Project.__attrs__["goals"].type=Goal
dbmap = {
    Project: 'plan_project',
    Task: 'plan_task',
    Link: 'work_link',
    Attr: 'work_attr',
    Join: 'work_join',
    Class: 'work_class',
    Goal: 'plan_goal',
    Project.__attrs__['goals']: (Goal,'projectID'),
    Goal.__attrs__['project']: (Project,'projectID'),
    Goal.__attrs__['tasks']: (Task,'goalID'),
    Task.__attrs__['goal']: (Goal,'goalID'),
}
class MyAdminApp(AdminApp):
    def list_project(self):
        self.write(prototype.generic_list(self.clerk, Project, "work.app"))
    def list_goal(self):
        self.write(prototype.generic_list(self.clerk, Goal, "work.app"))
    def list_task(self):
        self.write(prototype.generic_list(self.clerk, Task, "work.app"))
    def list_class(self):
        self.write(prototype.generic_list(self.clerk, Class, "work.app"))
    def list_attr(self):
        self.write(prototype.generic_list(self.clerk, Attr, "work.app"))
    def list_link(self):
        self.write(prototype.generic_list(self.clerk, Link, "work.app"))
    def list_join(self):
        self.write(prototype.generic_list(self.clerk, Join, "work.app"))
    def delete_project(self):
        self.generic_delete(Project, "")
        self.redirect("?action=list&what=project")
    def save_project(self):
        # populate with data from form:
        goals = self.input.get("goals")
        if goals: del self.input["goals"]
        obj = self._getInstance(Project)
        if goals:
            obj.goals = self.clerk.fetch(Goal,ID=goals)
        self.clerk.store(obj)
        self.redirect("?action=list&what=project")
    def edit_project(self):
        obj = self._getInstance(Project)
        self.write(prototype.generic_edit(self.clerk,  obj,"work.app"))
    def edit_goal(self):
        obj = self._getInstance(Goal)
        self.write(prototype.generic_edit(self.clerk,  obj,"work.app"))
    def save_goal(self):
        # populate with data from form:
        project = self.input.get("project")
        if project: del self.input["project"]
        tasks = self.input.get("tasks")
        if tasks: del self.input["tasks"]
        obj = self._getInstance(Goal)
        if project:
            obj.project = self.clerk.fetch(Project,ID=project)
        if tasks:
            obj.tasks = self.clerk.fetch(Task,ID=tasks)
        self.clerk.store(obj)
        self.redirect("?action=list&what=goal")
    def edit_task(self):
        obj = self._getInstance(Task)
        self.write(prototype.generic_edit(self.clerk,  obj,"work.app"))
    def save_task(self):
        # populate with data from form:
        goal = self.input.get("goal")
        if goal: del self.input["goal"]
        obj = self._getInstance(Task)
        if goal:
            obj.goal = self.clerk.fetch(Goal,ID=goal)
        self.clerk.store(obj)
        self.redirect("?action=list&what=task")
    def act_(self):
        self.write("""
<ul>
<li><a href="work.app?action=list&what=project">Project</a></li>
<li><a href="work.app?action=list&what=goal">Goal</a></li>
<li><a href="work.app?action=list&what=task">Task</a></li>
<li><a href="work.app?action=list&what=class">Class</a></li>
<li><a href="work.app?action=list&what=attr">Attr</a></li>
<li><a href="work.app?action=list&what=link">Link</a></li>
<li><a href="work.app?action=list&what=join">Join</a></li>
</ul>
        """)

if __name__=="__main__":
    from arlo import Clerk
    from sqlPair import dbc
    from storage import MySQLStorage
    CLERK = Clerk(MySQLStorage(dbc), dbmap)
    print >> RES, MyAdminApp(CLERK, REQ).act()
