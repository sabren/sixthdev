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
        self.model["project"]=self.input.get("project")
        self.model["status"]=self.input.get("status","open")
        self.model["owner"]=self.input.get("owner")
        self.model["targetDate"]=self.input.get("targetDate")

        wc = "1=1 "
        if self.model["project"] in self.model["opt_project"]:
            wc = wc + "AND project='%s' " % self.model["project"]
        if self.model["status"] in self.model["opt_status"]:
            wc = wc + "AND status='%s' " % self.model["status"]
        if self.model["owner"] in self.model["opt_owner"]:
            wc = wc + "AND owner='%s' " % self.model["owner"]

        # @TODO: validate targetdate is real date..
        if self.model["targetDate"]:
            from buggernaut import date
            wc = wc + "AND targetDate<='%s' " % date.us2sql(self.model["targetDate"])
            
        whereClause = wc
        return map(zdc.ObjectView,
                   zikebase.dbc.select(zikeplan.Task,
                                       where=whereClause,
                                       orderBy="isnull(targetDate), targetDate, " \
                                              +"priority DESC, risk DESC"))

if __name__=="__main__":
    TaskAdminApp().act()
