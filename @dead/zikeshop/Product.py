"""
Product.py - product object for zikeshop
"""
__ver__="$Id$"

import zdc
import zikebase
import zikeshop

class Product(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_product")

    # @TODO: fix this!!!!!! there should be no _tuples..
    # or should there be? I DO need to tell ObjectView
    # that there's a collection called nodes...
    # I'm only doing it this way because I don't have
    # a *:* join object yet.
    #
    # I need categories to display the product page
    # (this product is in ...)
    #
    _tuples = ['styles', 'categories']
    
    ### Magic RecordObject Methods ############################

    def _init(self):
        self._pic = None            

    def _new(self):
        self.__super._new(self)
        self._data['class'] = "product"
        self.code = ""
        self.name = ""
        self.descript = ""
        self.warn = 0
        self.price = 0
        self.cost = 0
        self.retail = 0
        self.weight = 0
        self.parentID = 0


    def _fetch(self, **where):
        apply(self.__super._fetch, (self,), where)
        self.categories.fetch()

    ## Normal RecordObject Methods #######################################

    def getEditableAttrs(self):
        return self.__super.getEditableAttrs(self) + ['picture']

    def delete(self):
        self.categories.delete()
        #@TODO: clean this up:
        for style in self.styles:
            style.delete()
        self.__super.delete(self)


    def save(self):
        if self._pic:
            self._pic.save()
            self.pictureID = self._pic.ID

        # validation logic:
        sql = "SELECT name FROM shop_product " \
              "WHERE code='%s' " \
              % (self.code)
        if self.ID:
            sql = sql + "AND ID != %i" % int(self.ID)

        cur = self._table.dbc.cursor()
        cur.execute(sql)
        if cur.rowcount:
            raise ValueError, "This code already exists!"

        self.__super.save(self)
        self.categories.save()


    ## accessors ###############################################

    def get_price(self):
        return zdc.FixedPoint(self._data.get('price', '0.00'))

    def get_cost(self):
        return zdc.FixedPoint(self._data.get('cost', '0.00'))

    def get_retail(self):
        return zdc.FixedPoint(self._data.get('retail', '0.00'))


    def set_picture(self, blob):
        # on a multipart/form-data form,
        # if you don't upload a file, it still gives you
        # a string field.. this "if" copes with that.
        if type(blob) != type(""):
            self.get_picture()
            self._pic.picture = blob.value
            self._pic.type = blob.type

    def get_picture(self):
        if not self._pic:
            if self.pictureID:
                self._pic = zikebase.Picture(ID=self.pictureID)
            else:
                self._pic = zikebase.Picture()
        return self._pic


    def get_styles(self):
        return zdc.LinkSet(self, zikeshop.Style, "parentID")

    ## category junction stuff #########################################

    def get_categories(self):
        if not self._data.has_key("cats"):
            self._data["cats"] = CatJunction(self)
        return self._data["cats"]
          
    def set_categories(self, value):
        vals = []
        if type(value) == type(0):
            vals.append(value)
        elif type(value)==type(""):
            vals.append(int(value))
        elif type(value) in (type(()), type([])):
            for item in value:
                vals.append(int(item))
        else:
            raise TypeError, \
                  "value assigned to categories should be int or int list," \
                  "not %s" % type(value)

        self.categories.clear()
        for catID in vals:
            self.categories << zikeshop.Category(ID=catID)

        
class CatJunction(zdc.IdxDict):
    __super = zdc.IdxDict

    def __init__(self, owner):
        self.__super.__init__(self)
        self.owner = owner

    def delete(self):
        """
        delete nodes for this product. used internally.
        """
        cur = self.owner._table.dbc.cursor()
        cur.execute("DELETE FROM shop_product_node WHERE productID=%s" \
                    % int(self.owner.ID))

    def fetch(self):
        if self.owner.ID:
            cur = self.owner._table.dbc.cursor()
            cur.execute("select nodeID from shop_product_node " + \
                        "where productID=%s ORDER BY nodeID" \
                        % int(self.owner.ID))

            # cur.execute returns a tuple of tuples, eg ((1,), (2,) ...)
            # we only want the first value (column) from each tuple.
            for row in cur.fetchall():
                self << zikeshop.Category(ID=row[0])

    def IDs(self):
        #@TODO: do I really need .IDs? (maybe for the edit product form?)
        return tuple(map( lambda cat: cat.ID, self))
                
    def save(self):
        # handle the nodes:
        cur = self.owner._table.dbc.cursor()        
        self.delete()
        for cat in self:
            cur.execute("INSERT INTO shop_product_node (nodeID, productID) "
                        "VALUES (%s, %s)" % (cat.ID, int(self.owner.ID)))
