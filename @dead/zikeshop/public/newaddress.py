"""
add an address to zikeshop

$Id$
"""

import zikebase; zikebase.load("ObjectEditor")
import zikeshop
import weblib
weblib.auth.check()

weblib.request.form["customerID"] = weblib.auth.user.ID
ed = zikebase.ObjectEditor(zikeshop.Address)
ed.act()


if weblib.request.get("context") == "checkout":
    assert weblib.request.has_item("whichone"), \
           "checkout context requires a whichone item.."
    cash = zikeshop.Cashier(zikeshop.Cart(), weblib.auth.user)
    setattr(cash, weblib.request("whichone")+'AddressID', ed.object.ID,
            input = {})
    cash.act()
    
