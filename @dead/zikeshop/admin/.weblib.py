## print "content-type: text/plain"
## print 
## import sys
## sys.stderr = sys.stdout
import sys
sys.path.append("d:/python20/PIL/") # for them.

import zikeshop
import weblib

class CartAuth(weblib.Auth):
    def prompt(self, message, action, hidden):
        import zebra
        model = {"message":message,
                 "action":action,
                 "hidden":hidden}
        zebra.show("frm_login",model)
                
auth = CartAuth({"racing2001":"emig3296"})
auth.check()
