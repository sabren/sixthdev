# 0307.2001 more/better tests for checkout.. but not a pyunit testcase..  :/
__ver__="$Id$"

import zikebase,zikebase.config
zikebase.dbc = zikebase.config.test_dbc
import zikeshop
from zikeshop.public.checkout import CheckoutApp

import weblib
weblib.request = weblib.Request()
weblib.sess = {}


myCart = zikeshop.Cart()
myCart.add("something")

app = CheckoutApp(cart=myCart)

# check for xxxData
app.enter()
assert app.billData["fname"]=="", "didn't create blank bill address"
assert app.shipData["fname"]=="", "didn't create blank ship address"
assert app.cardData["number"] is None, "didn't create blank card"

# just call get_billing to  make sure no error.
import sys, StringIO
stdout, sys.stdout = sys.stdout, StringIO.StringIO()
import os; os.chdir("../public")
app.do("get_billing")
sys.stdout = stdout

# try adding a bad address
app.input = {
    "context":"bill",
    "fname":"michal",
    "lname":"wallace",
    "email":"INVALID_EMAIL",
    "address1":"123 easy street",
    "city":"slsakdjflkjresville",
    "stateCD":"TX",
    "countryCD":"US",
    "postal":"76126",
    }
app.do("add_address")
assert app.model["errors"], \
       "didn't get errors with invalid email: %s" % str(app.model["errors"])
assert app.next=="get_billing", "didn't redirect to billing page"

# fix the error, try again:
app.model["errors"] = []
app.input["email"]="sabren@manifestation.com"
app.do("add_address")
assert not app.model["errors"], \
       "STILL got error: %s" % str(app.model["errors"])



#import pdb; pdb.set_trace()
#app.act()

