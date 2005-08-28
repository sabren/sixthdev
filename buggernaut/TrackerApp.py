
import sixthday
import zebra
from buggernaut import Task
from strongbox import *

class TrackerApp(sixthday.AdminApp):

    def act_(self):
        self.list_task()

    def create_task(self):
        self.model["opt_area"] = []
        self.model["opt_status"] = ['open','urgent','active','closed']
        self.generic_show(Task, "frm_task")

    def save_task(self):
        self.generic_save(Task)
        self.redirect("tracker.app")
        
    def list_task(self):
        #self.model["status"] = "*"
        tasks = map(BoxView,
                    self.clerk.match(Task)) #, status='open'))
        self.model["list"] = tasks
        self.model["opt_area"] = ['asdf']
        self.model["opt_status"] = ['open','urgent','active','closed']
        print >> self, zebra.fetch("lst_task", self.model)

