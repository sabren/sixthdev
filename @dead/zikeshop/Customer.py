
import zdc
import zikebase
import zikeshop
zikebase.load("User")
zikebase.load("Rot13Password")

class Customer(zikebase.User):

    
    passwordClass = zikebase.Rot13Password

    def _new(self):
        import weblib
        zikebase.User._new(self)
        self.uid = weblib.uid()
        self.siteID = zikeshop.siteID
        self.username = ""


    ## primary address:

    def get_address(self):
        """cart.address returns primary address"""
        return zikeshop.Address(customerID=self.ID, isPrimary=1)

    
    def set_address(self, value):
        """this makes the address attribute read-only"""
        raise TypeError, ".address is readonly."


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
    
    def q_creditcards(self):
        cur = zikeshop.dbc.cursor()
        cur.execute(
            """
            SELECT *
            FROM shop_card
            WHERE customerID=%i
            """ % self.ID)
        return zdc.toListDict(cur)
