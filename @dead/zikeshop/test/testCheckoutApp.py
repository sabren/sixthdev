"""
test cases for CheckoutApp
"""
__ver__ = "$Id$"

import unittest
import zikeshop

import sys, os
from zikeshop.public.checkout import CheckoutApp

class CheckoutAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.ds = zikeshop.test.dbc
        
        # wipe the database clean.
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("DELETE FROM shop_sale")
        self.cur.execute("DELETE FROM shop_detail")
        
        self.sess = {}
        self.app = CheckoutApp({}, zikeshop.Cart({}), self.ds, self.sess)

        self.cwd = os.getcwd()
        os.chdir("public")
        
    def tearDown(self):
        os.chdir(self.cwd)

    def check_checkout(self):
        ## THIS IS ONE *LONG* TEST...............
        
        import zikebase,zikebase.config
        zikebase.dbc = zikebase.config.test_dbc
        import zikeshop
        from zikeshop.public.checkout import CheckoutApp

        import weblib
        weblib.request = weblib.Request()


        myCart = zikeshop.Cart({})
        myCart.add("super-evil-destructo-ray")

        app = CheckoutApp({}, myCart, self.ds, self.sess)

        # check for xxxData
        app.enter()
        assert app.billData["fname"]=="", "didn't create blank bill address"
        assert app.shipData["fname"]=="", "didn't create blank ship address"
        assert app.cardData["number"] is None, "didn't create blank card"

        # just call get_billing to  make sure no error.
        # @TODO: compare this to an expected version..

        RES = weblib.Response()

        app.do("get_billing")

        # try adding a bad address
        app.input = {
            "context":"bill",
            "fname":"michal",
            "lname":"wallace",
            "email":"INVALID_EMAIL",
            "address1":"123 easy street",
            "city":"Atlanta",
            "stateCD":"GA",
            "countryCD":"US",
            "postal":"76126",
            }
        app.do("add_address")
        assert app.model["errors"], \
               "didn't get errors with invalid email: %s" \
               % str(app.model["errors"])
        
        assert app.next=="get_billing", "didn't redirect to billing page"

        # fix the error, try again:
        app.model["errors"] = []
        app.input["email"]="sabren@manifestation.com"
        app.do("add_address")
        assert not app.model["errors"], \
               "STILL got error: %s" % str(app.model["errors"])
        assert app.where['gohere'][:20]=="?action=get_shipping",\
               "didn't redirect to shipping page when no shipToBilling: %s" \
               % app.where['gohere'][:20]

        # try showing the get_shipping form:
        # @TODO: compare this to an expected version..
        app.do("get_shipping")

        # ship to billing box..
        app.input["shipToBilling"]="1"
        app.do("add_address")
        assert app.where['gohere'][:16]=="?action=get_card",\
               "didn't redirect to card page when shipToBilling: %s" \
               % app.where['gohere'][:16]
        assert app.billData == app.shipData, "didn't copy billing data"
        assert app.shipData["fname"]=="michal", \
               "REALLY didn't copy billing data"


        # send that super-evil-destructo-ray to my mom instead:
        app.input["context"]="ship"
        app.input["fname"]="cathy" 
        app.input["city"]="benbrook"
        app.input["stateCD"]="TX"
        app.do("add_address")
        assert app.shipData["fname"]=="cathy", "didn't set ship data"
        assert app.billData["fname"]=="michal", "overwrote bill data"
        assert app.where['gohere'][:16]=="?action=get_card",\
               "didn't redirect to card page after shipping: %s" \
               % app.where['gohere'][:16]

        # credit card form
        # @TODO: compare this to an expected version..
        app.do("get_card")
        assert app.cardData["name"]=="michal wallace", \
               "didn't guess name from billing"

        # submit a card:
        fakeCard = "4111111111111119"
        goodCard = "4111111111111111"

        from zikeshop.Card import validate
        assert validate(fakeCard)==0, "didn't catch fake card"
        assert validate(goodCard)==1, "didn't pass good card"


        import time
        nowYear, nowMonth = time.localtime(time.time())[0:2]
        app.input = {
            "name": "Michal J Wallace",
            "number": fakeCard,
            "expMonth": str(nowMonth+1),
            "expYear": str(nowYear),
            }

        #import pdb; pdb.set_trace()
        app.do("add_card") #@TODO: these ought not be called "add"_XXX anymore
        #@TODO: app.errors ought to jump automatically into model["errors"]
        assert app.model["errors"]==[{"error":"Invalid credit card number."}],\
               "didn't catch invalid card: %s" % str(app.model["errors"])
        assert app.next == "get_card", "didn't cue get_card after bad card"


        # expired card:
        app.model["errors"]=[]
        app.input["number"]=goodCard
        app.input["expYear"]=str(nowYear-1)
        app.do("add_card")
        assert app.model["errors"]==[{"error":"Expired card."}],\
               "didn't catch expired card: %s" % str(app.model["errors"])

        # finally, get it all right...
        app.model["errors"]=[]
        app.input["expYear"]=nowYear+1
        app.do("add_card")
        assert app.model["errors"]==[], \
               "STILL got error after everything is right"
        assert app.where["gohere"][:15]=="?action=confirm", \
               "didn't redirect to confirmation page: %s" \
               % app.where["gohere"][:15]


        # show the confirmation page
        #@TODO: compare to expected
        app.do("confirm")

        #assert app.where["gohere"][:16]=="?action=checkout", \
        #       "didn't redirect to checkout page: %s" \
        #       % app.where["gohere"][:16]


        #import pdb; pdb.set_trace()
        #app.act()
        
