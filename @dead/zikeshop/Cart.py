"""
Cart.py - a cart class for zikeshop

$Id$
"""

import weblib

class Cart:

    ## attributes ############################################

    name = None
    pool = None
    key = None

    _contents = []

    ## constructor ###########################################

    def __init__(self, pool=None, name=""):

        # pool is so we can tell where to store the data
        # it's just another hash, and most likey, the
        # weblib.sess object:

        if pool is None:
            self.pool = weblib.sess
        else:
            self.pool = pool


        # Originally, I prevented a site from creating more
        # than one cart. Would you ever need two carts?
        # This is probably a case of YouArentGoingToNeedIt,
        # but it's about the same amount of code to not allow
        # it: If we *don't* name carts, we have to check that
        # you don't load two carts at once because they'll
        # trash each others data. This problem remains
        # with the named cart scheme, but at least we
        # give the developer a way out.
        #
        # I thought about just generating a unique name for
        # the cart, but that's messy because then you have
        # to remember a generated name from page to page,
        # which probably means storing it in the session
        # under a name anyway. So I figure just put the name
        # directly on the Cart and leave it at that.

        self.name = name
        self.key = self._getKey()

        # if we don't do this, self._contents will be shared
        # by all Carts... I wish python had a way to declare
        # variables.. :/
        
        self._contents = []
        

    ## public methods ########################################


    def start(self):
        """cart.start() - fetches the _contents from the pool."""
        if self.pool.has_key(self.key):
            self._contents = self.pool[self.key]

    
    def isEmpty(self):
        """cart.isEmpty() - Returns 1 if the cart is empty."""
        return len(self._contents)==0


    def add(self, label, price=0, quantity=None, link=None, extra=None): 
        "cart.add(label, [price,quantity,link,extra]) - add item to cart."""
        if quantity is None:
            quantity = 1
        if link is None:
            link = ""                
        if label:
            # if the item is already in the cart with the
            # same options, just increase the quantity..
            for item in self._contents:
                if (label==item["label"]):
                    item["quantity"] = item["quantity"] + quantity
                    return
            # if we're still here, just add it in
            self._contents.append({"label":label, "quantity":quantity,
                                  "price":price, "link":link, "extra":extra})
        else:
            pass # nothing to add


    def count(self):
        """Count of items in cart. (does NOT consider quanities per item)"""
        return len(self._contents)


    def update(self, index, newQuantity):
        """cart.update(index, newQuanity) - update quantity for an item.

        If newQuantity is None, nothing changes.
        """
        if newQuantity is not None:
            self._contents[index]["quantity"] = newQuantity
        

    def remove(self, index):
        """cart.remove(index) - Remove an item from the cart."""
        del self._contents[index]


    def purge(self):
        """cart.purge() - Delete any items with 0 quantity from the cart."""
        self._contents = filter(lambda x: x["quantity"]!=0, self._contents)


    def empty(self):
        """cart.empty() - Remove all items from the cart."""
        self._contents = []


    def stop(self):
        """cart.stop() - Store the cart's _contents cart.pool"""
        self.pool[self.key] = self._contents


    def subtotal(self):
        """cart.subtotal() - returns a subtotal of the sale amounts"""
        subt = 0
        for item in self._contents:
            subt = subt + (item["price"] * item["quantity"])
        return subt
            

    ## queries #########################################################

    def q_contents(self):
        """Returns an editable copy of the cart's contents, plus subtotals"""
        import copy, zikeshop
        res = copy.deepcopy(self._contents)
        for row in res:
            row["subtotal"] = str(zikeshop.FixedPoint(row["price"]) \
                                  * row["quantity"])
        return res


    ## private methods #################################################

    def _getKey(self):
        """private method to generate a key for the pool."""
        return "__cart_" + self.name



