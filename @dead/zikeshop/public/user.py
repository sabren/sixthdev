"""
authentication / signup process for zikeshop
"""
__ver__="$Id$"

import weblib, zebra
import zikebase
zikebase.load("UserApp")

class ZSUserApp(zikebase.UserApp):
    __super = zikebase.UserApp

    def __init__(self, input=None):
        self.__super.__init__(self, input)
        self.where["get_shipping"]="checkout.py?action=get_shipping"
        self.where["set_shipping"]="checkout.py?action=set_shipping&shipToBilling=1"

    
    def act_create(self):
        self.__super.act_create(self)

        #@TODO: allow (optionally) selecting shipping methods?
        next = "get_shipping"
        if self.input.get('isSame'):
            next = "set_shipping"
        self.next = ("jump", {"where":next})


##     def act_login(self):
##         weblib.auth.check()
##         self.onLogin()

##     def onLogin(self):
##         print "logged in ... jump to next page.."

if __name__=="__main__":
    ZSUserApp().act()
