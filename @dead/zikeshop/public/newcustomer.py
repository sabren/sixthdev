"""
add a customer to zikeshop
"""
__ver__="$Id$"

import zikebase; zikebase.load("ObjectEditor")
import zikeshop
import weblib

assert weblib.request.get("ID") is None, \
       "New customers can't already have an ID"

if weblib.request.get("action") == "save":

    ## @TODO: make email duplication checking an option
    checkDuplicateEmails = 0
    if checkDuplicateEmails:
        ## make sure this customer doesn't already exist
        if weblib.request.get("email") is None:
            raise ValueError, "Email Address is Required!"
        try:
            existing = zikeshop.Customer(email=weblib.request["email"])
        except:
            existing = None

        if existing:
            print "There is already a user with this email address."
            print '<a href="password.py">click here</a> if you\'ve forgotten'
            print 'your password, or click your browser\'s back button to '
            print 'use a different email address.'
            weblib.response.end()

    ## first create the customer
    ed = zikebase.ObjectEditor(zikeshop.Customer)
    ed.act()

    ## log 'em in:
    weblib.auth.login(ed.object.ID)
    
    weblib.request.form["customerID"] = ed.object.ID
    weblib.request.form["isPrimary"] = 1
    ed = zikebase.ObjectEditor(zikeshop.Address)
    ed.act()

    cash = zikeshop.Cashier(zikeshop.Cart(), weblib.auth.user)
    cash.nextStep()

else:
    print "nothing to do."

