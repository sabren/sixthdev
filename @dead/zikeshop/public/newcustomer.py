"""
add a customer to zikeshop

$Id$
"""

import zikebase; zikebase.load("ObjectEditor")
import zikeshop
import weblib

assert weblib.request.get("ID") is None, \
       "New customers can't already have an ID"

if weblib.request.get("action") == "save":

    ## first create the customer
    ed = zikebase.ObjectEditor(zikeshop.Customer)
    ed.act()

    ## log 'em in:
    weblib.auth.login(ed.object.ID)
    
    weblib.request.form["customerID"] = ed.object.ID
    weblib.request.form["isPrimary"] = 1
    ed = zikebase.ObjectEditor(zikeshop.Address)
    ed.act()

    print "thanks for joining us!"
    print "[logged in as: %s]" % weblib.auth.user.email

    cash = zikeshop.Cashier(zikeshop.Cart(), weblib.auth.user)
    cash.nextStep()

else:
    print "nothing to do."




