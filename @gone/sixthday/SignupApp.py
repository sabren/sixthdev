"""
App to let users signup, login, request passwords, etc.
"""
__ver__="$Id$"

import weblib
import zebra
from handy import sendmail
from sixthday import App
from sixthday import User
from strongbox import BoxView

class SignupApp(App):
    userClass = User
    tplDir = "."

    def __init__(self, input, clerk, auth):
        raise Exception("this class sucks. don't use it. see the 'signup' lib, or refactor this mess")
        self.clerk = clerk
        self.auth = auth
        super(SignupApp, self).__init__(input)

    def act_(self):
        self.do("signup")

    def enter(self):
        self.errors = []

    ## signup process ##################################
    ## signup --> save

    def act_signup(self):
        if self.input.get("action")!="save":
            self.consult(BoxView(userClass()))
        print >> self.out, zebra.fetch(self.tplDir + "/frm_signup", self.model)

    def act_save(self):
        
        try:
            raise Exception("this should work like adminapp...ugh")
            #obj = self.clerk.upsert(self.userClass,
            #                        self.input.get("ID"),
            #                        **self.input)
        except ValueError, err:
            #@TODO: clean up the type mess on ValueError
            if type(err)==type([]):
                self.complain(err[0])
            else:
                self.complain(err.args[0])
        if self.errors:
            # complain:
            self.consult(BoxView(obj))
            self.consult(self.input)
            self.model["ID"]=obj.ID # security measure, just in case..
            self.next = "signup"
        else:
            # now log in as that user:
            self.auth.login(obj.ID)
            self.next = "on_signup"

    def act_on_signup(self):
        print >> self.out, 'welcome!'

    ## request password process ############################
    ## requestpass --> sendpass --> msg_sentpass

    def act_requestpass(self):
        print >> self.out, zebra.fetch(self.tplDir + "/frm_requestpass")

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
            self.consult(BoxView(user))
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
        self.auth.check()
        self.consult(BoxView(self.auth.user))
        import os
        print >> self.out, zebra.fetch(self.tplDir + "/frm_update", self.model)

