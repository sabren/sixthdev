"""
UserAdminApp - manages zike users...
"""
__ver__="$Id$"

import weblib, zebra, zikebase, zdc
zikebase.load("AdminApp")
zikebase.load("User")

class ZUserAdminApp(zikebase.AdminApp):
    __super = zikebase.AdminApp
    userClass = zikebase.User

    ## constructor page ##################################
    
    def __init__(self, input=None):
        self.__super.__init__(self, input)
        self.what = {"user":self.userClass}

    ## home page ########################################

    def act_(self):
        self.do("list", what="user")

    ## actions ##########################################

    def qry_user(self):
        return map(zdc.ObjectView, zikebase.dbc.select(zikebase.User))

    def save_user(self):
        ed = zikebase.ObjectEditor(self.userClass, self.input.get("ID"))
        ed.do("update")
        if self.input.get("new_password","") != "":
            ed.object.password = self.input["new_password"]
        ed.object.save()

##     def show_XXX(self):
##         pass # consult an objectview, call zebra
    
##     def create_XXX(self):
##         self.generic_create("XXX") # show form for creating


if __name__=="__main__":
    ZUserAdminApp().act()
