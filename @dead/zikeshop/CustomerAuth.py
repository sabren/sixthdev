"""
customer authentication...

$Id$
"""
import zikeshop
import zikebase
zikebase.load("UserAuth")

class CustomerAuth(zikebase.UserAuth):
    userClass = zikeshop.Customer


    def prompt(self, message, action, hidden):
        import tpl_login
        tpl_login.show({"message":message,
                        "action":action,
                        "hidden":hidden,})
    


