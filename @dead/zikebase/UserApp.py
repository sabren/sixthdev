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

    def sendmail(self, address, mail):
        zikebase.sendmail(address, mail)

    def act_(self):
        self.do("signup")

    ## signup process ##################################
    ## signup --> create

    def act_signup(self):
        self.consult(zdc.ObjectView(self.userClass()))
        zebra.show("frm_signup", self.model)

    def act_create(self):
        # create the user:
        ed = self.editorClass(self.userClass, input=self.input)
        ed.do("save")

        # now log in as that user:
        import weblib
        if hasattr(weblib, "auth"):
            weblib.auth.login(ed.object.ID)


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
            self.sendmail(user.email, msg)
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

    def act_save(self):
        # save the user:
        ed = self.editorClass(self.userClass,
                              self.input["ID"],
                              input=self.input)
        ed.do("save")
