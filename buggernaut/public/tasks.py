"""
task administrator
"""
__ver__="$Id$"

import weblib, zebra
import sixthday

from strongbox import BoxView
from buggernaut import Task

class TaskAdminApp(sixthday.AdminApp):

    ## home page ########################################

    def act_(self):
        self.list_task()

    def enter(self):
        task = Task()
        self.model["opt_status"]=Task.__attrs__["status"].okay
        self.model["opt_priority"]=Task.__attrs__["status"].okay
        self.model["opt_risk"]=Task.__attrs__["risk"].okay
        self.model["opt_owner"]=Task.__attrs__["owner"].okay
        self.model["opt_project"]=Task.__attrs__["project"].okay
        
    def exit(self):
        global RES
        if self.errors:
            print >> RES, self.errors

    ## actions ##########################################

    def list_task(self):
        self.model["project"]=self.input.get("project")
        self.model["status"]=self.input.get("status","open")
        self.model["owner"]=self.input.get("owner")
        self.model["targetDate"]=self.input.get("targetDate")

        wc = "1=1 "
        if self.model["project"] in self.model["opt_project"]:
            wc += "AND project='%s' " % self.model["project"]
        if self.model["status"] in self.model["opt_status"]:
            wc += "AND status='%s' " % self.model["status"]
        if self.model["owner"] in self.model["opt_owner"]:
            wc += "AND owner='%s' " % self.model["owner"]

        # @TODO: validate targetdate is real date..
        if self.model["targetDate"]:
            wc += "AND targetDate<='%s' " \
                  % date.us2sql(self.model["targetDate"])
            
        whereClause = wc
        return map(BoxView, self.clerk.match(Task))

if __name__=="__main__":
    print >> RES, TaskAdminApp(CLERK, REQ).act()
