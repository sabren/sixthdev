"""
"""
__ver__="$Id$"

import weblib, zebra, zikebase, zikeplan
zikebase.load("AdminApp")

class ZikePlanAdminApp(zikebase.AdminApp):
    __super = zikebase.AdminApp

    ## constructor page ##################################
    
    def __init__(self, input=None):
        self.__super.__init__(self, input)
        self.what = {
            "goal":zikeplan.Goal,
            "status":zikeplan.Status,
            "type":zikeplan.Type,
            }


    ## home page ########################################

    def act_(self):
        self.do("list", what="goal")

    def enter(self):
        import zebra
        print zebra.fetch("dsp_head")
        
    def exit(self):
        if self.errors:
            print self.errors

    ## actions ##########################################

    def qry_goal(self):
        return map(zdc.ObjectView, zikebase.dbc.select(zikeplan.Goal))

    def qry_status(self):
        return map(zdc.ObjectView, zikebase.dbc.select(zikeplan.Status))

    def qry_type(self):
        return map(zdc.ObjectView, zikebase.dbc.select(zikeplan.Type))

##         pass # for generic_list, which calls this and then lst_XXX.zb
# -- OR: --
##     def list_XXX(self):
##         pass # usually consult something, call zebra..

##     def show_XXX(self):
##         pass # consult an objectview, call zebra
    
##     def create_XXX(self):
##         self.generic_create("XXX") # show form for creating

##     def save_XXX(self):
##         self.generic_save("XXX")


if __name__=="__main__":
    ZikePlanAdminApp().act()
