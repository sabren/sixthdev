"""
Customer class for zikeshop
"""
__ver__="$Id$"

import zdc
import zikebase
import zikeshop
zikebase.load("User")
zikebase.load("Rot13Password")

class Customer(zikebase.User):
    _tuples = ['cards']
    
    passwordClass = zikebase.Rot13Password

    def _new(self):
        import weblib
        zikebase.User._new(self)
        self.uid = weblib.uid()
        self.username = ""


    ## addressbook:
    
    def q_addressbook(self):
        cur = zikeshop.dbc.cursor()
        cur.execute(
            """
            SELECT *
            FROM shop_address
            WHERE customerID=%i
            """ % self.ID)
        return zdc.toListDict(cur)


    ## credit cards

    def get_cards(self):
        return map(lambda c: zikeshop.Card(ID=c['ID']),
                   self.q_creditcards())
    
    def q_creditcards(self):
        cur = zikeshop.dbc.cursor()
        cur.execute(
            """
            SELECT *
            FROM shop_card
            WHERE customerID=%i
            """ % self.ID)
        res = zdc.toListDict(cur)
        # maskedNumber has the xxxxxxxx1234 form of the card number:
        for item in res:
            item["maskedNumber"] = ("x" * (len(item["number"])-4)) \
                                   + item["number"][-4:]
        return res
