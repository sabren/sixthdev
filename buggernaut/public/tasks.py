"""
task administrator
"""
__ver__="$Id$"

import weblib, zebra, zikebase, zikeplan
zikebase.load("AdminApp")

class TaskAdminApp(zikebase.AdminApp):
    __super = zikebase.AdminApp

    ## constructor page ##################################
    
    def __init__(self, input=None):
        self.__super.__init__(self, input)
        self.what = {
            "task":zikeplan.Task
            }


    ## home page ########################################

    def act_(self):
        self.do("list", what="task")

    def enter(self):
        task = zikeplan.Task()
        self.model["opt_status"]=task.opt_status()
        self.model["opt_priority"]=task.opt_priority()
        self.model["opt_risk"]=task.opt_risk()
        self.model["opt_owner"]=task.opt_owner()
        self.model["opt_project"]=task.opt_project()
        
    def exit(self):
        if self.errors:
            print self.errors

    ## actions ##########################################

    def qry_task(self):
        if self.input.get("project") in self.model["opt_project"]:
            whereClause = "project='%s'" % self.input["project"]
        else:
            whereClause = None
        return map(zdc.ObjectView,
                   zikebase.dbc.select(zikeplan.Task,
                                       where=whereClause,
                                       order="priority DESC, risk DESC"))

if __name__=="__main__":
    TaskAdminApp().act()
