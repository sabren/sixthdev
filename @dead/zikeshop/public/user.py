"""
authentication / signup process for zikeshop
"""
__ver__="$Id$"

import weblib, zebra
import zikebase
zikebase.load("UserApp")

class ZSUserApp(zikebase.UserApp):
    __super = zikebase.UserApp

    def act_create(self):
        self.__super.act_create(self)

        #@TODO: allow (optionally) selecting shipping methods?
        next = "action=get_shipping"
        if self.input.get('isSame'):
            next = "action=set_shipping&use_billing=true"
        self.next = ("jump", next)


##     def act_login(self):
##         weblib.auth.check()
##         self.onLogin()

##     def onLogin(self):
##         print "logged in ... jump to next page.."

if __name__=="__main__":
    ZSUserApp().act()
