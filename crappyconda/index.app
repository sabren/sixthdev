

from strongbox import *
from pytypes import *

class Node(Strongbox):
    name = attr(str)
    data = attr(str)
    posted = link(DateTime)
    notes = linkset(forward)

class User(Strongbox):
    username = attr(str)
    password = attr(str)
    fname = attr(str)
    lname = attr(str)
    email = attr(str)
    url = attr(str)

class Note(Node):
    author = link(User)

class Project(Node):
    goals = linkset(forward)

class Goal(Node):
    tasks = linkset(forward)

class Task(Node):
    pass

Node.__attrs__["notes"].type=Note
Goal.__attrs__["tasks"].type=Task
Project.__attrs__["goals"].type=Goal


from sixthday import AdminApp

class PlanacondaApp(AdminApp):
   def act_(self):
      self.list_project()
      
   def list_note(self):
      self.generic_list(Note, 'lst_note')
      return
   def show_note(self):
      self.generic_show(Note, 'sho_note')
      return
   def edit_note(self):
      self.generic_show(Note, 'frm_note')
      return
   def save_note(self):
      self.generic_save(Note)
      return
   def delete_note(self):
      self.generic_delete(Note, 'frm_note')
      return
   
   def list_project(self):
      self.generic_list(Project, 'lst_project')
      return
   def show_project(self):
      self.generic_show(Project, 'sho_project')
      return
   def edit_project(self):
      self.generic_show(Project, 'frm_project')
      return
   def save_project(self):
      self.generic_save(Project)
      return
   def delete_project(self):
      self.generic_delete(Project, 'frm_project')
      return
   
   def list_task(self):
      self.generic_list(Task, 'lst_task')
      return
   def show_task(self):
      self.generic_show(Task, 'sho_task')
      return
   def edit_task(self):
      self.generic_show(Task, 'frm_task')
      return
   def save_task(self):
      self.generic_save(Task)
      return
   def delete_task(self):
      self.generic_delete(Task, 'frm_task')
      return
   
   def list_user(self):
      self.generic_list(User, 'lst_user')
      return
   def show_user(self):
      self.generic_show(User, 'sho_user')
      return
   def edit_user(self):
      self.generic_show(User, 'frm_user')
      return
   def save_user(self):
      self.generic_save(User)
      return
   def delete_user(self):
      self.generic_delete(User, 'frm_user')
      return
   
   def list_goal(self):
      self.generic_list(Goal, 'lst_goal')
      return
   def show_goal(self):
      self.generic_show(Goal, 'sho_goal')
      return
   def edit_goal(self):
      self.generic_show(Goal, 'frm_goal')
      return
   def save_goal(self):
      self.generic_save(Goal)
      return
   def delete_goal(self):
      self.generic_delete(Goal, 'frm_goal')
      return


class NewApp(AdminApp):

   def act_(self):
      print >> self, "X"
      for c in self.clerk.dbmap:
         print "X"
         print >> self, c
   
   

import shelve
from arlo import MockClerk
shv = shelve.open("data.shlv")
app = NewApp(MockClerk(shv), REQ)
app.debug = 1
print >> RES, app.act()
shv.close()

