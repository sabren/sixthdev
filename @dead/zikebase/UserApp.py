"""
App to let users signup, login, request passwords, etc.
"""
__ver__="$Id$"

import weblib, zikebase, zebra
zikebase.load("User")

class UserApp(weblib.Actor):
    userClass = zikebase.User

    def act_(self):
        self.do("signup")

    ## signup process ##################################
    ## signup --> create

    def act_signup(self):
        import zdc
        self.consult(zdc.ObjectView(self.userClass()))
        zebra.show("frm_signup", self.model)

    def act_create(self):
        # create the user:
        ed = zikebase.ObjectEditor(self.userClass, input=self.input)
        ed.do("save")

        # now log in as that user:
        import weblib
        if hasattr(weblib, "auth"):
            weblib.auth.login(ed.object.ID)


    ## request password process ############################
    ## requestpass --> sendpass

    def act_requestpass(self):
        pass

    def act_sendpass(self):
        pass


    ## change password process #############################
    ## changepass --> save


    ## edit info process ###################################
    ## edit --> save

