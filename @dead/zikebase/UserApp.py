"""
App to let users signup, login, request passwords, etc.
"""
__ver__="$Id$"

import weblib, zikebase, zebra, zdc
zikebase.load("User")
zikebase.load("ObjectEditor")

class UserApp(weblib.Actor):
    userClass = zikebase.User
    editorClass = zikebase.ObjectEditor

    def act_(self):
        self.do("signup")

    def enter(self):
        self.errors = []

    ## signup process ##################################
    ## signup --> save

    def act_signup(self):
        if self.input.get("action")!="save":
            self.consult(zdc.ObjectView(self.userClass()))
        zebra.show("frm_signup", self.model)

    def act_save(self):
        try:
            ed = zikebase.ObjectEditor(self.userClass, input=self.input)
            ed.do("save")
        except ValueError, err:
            #@TODO: clean up the type mess on ValueError
            if type(err)==type([]):
                self.complain(err[0])
            else:
                self.complain(err.args[0])
        if self.errors:
            # complain:
            self.consult(zdc.ObjectView(ed.object))
            self.consult(self.input)
            self.model["ID"]=ed.object.ID # security measure, just in case..
            self.next = "signup"
        else:
            # now log in as that user:
            import weblib
            if hasattr(weblib, "auth"):
                weblib.auth.login(ed.object.ID)
            self.next = "on_signup"

    def act_on_signup(self):
        print 'welcome!'

    ## request password process ############################
    ## requestpass --> sendpass --> msg_sentpass

    def act_requestpass(self):
        zebra.show("frm_requestpass")

    def act_sendpass(self):
        try:
            user = self.userClass(email=self.input["email"])
        except:
            self.complain(
                '''
                The email address, <b>%s</b>,
                wasn\'t found in our database.<br>
                You can
                  <a href="user.py?action=signup">create a new account</a>,<br>
                or you can try a different email address below.
                ''' % weblib.request["email"])
            self.next = "requestpass"
        else:
            self.consult(zdc.ObjectView(user))
            msg = zebra.fetch("eml_sendpass", self.model)
            zikebase.sendmail(msg)
            self.msg_sentpass()

    def msg_sentpass(self):
        """
        You probably should override this with a template.
        """
        print '''\
        Your password has been sent to your email address. <br>
        When you receive it, <a href="login.py">click here to login</a>.
        '''

    ## change password process #############################
    ## changepass --> save


    ## update info process ###################################
    ## update --> save

    def act_update(self):
        weblib.auth.check()
        self.consult(zdc.ObjectView(weblib.auth.user))
        zebra.show("frm_update", self.model)

