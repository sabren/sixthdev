"""
Product.py - product object for zikeshop
"""
__ver__="$Id$"

import zdc
import zikeshop
from zikeshop import Picture

class Product(zdc.RecordObject):
    _tablename = "shop_product"

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
        super(Product,self)._new()
        self._data['class'] = "product"
        self.code = ""
        self.name = ""
        self.brief=""
        self.descript = ""
        self.warn = 0
        self.price = 0
        self.cost = 0
        self.retail = 0
        self.weight = 0
        self.parentID = 0
        self.isHidden = 0

        self.hold = 0
        self.stock = None  # no value known (this doesn't mean no stock..)
        self.warn = None   # no warning


    def _fetch(self, **where):
        super(Product, self)._fetch(**where)
        self.categories.fetch()

    ## Normal RecordObject Methods #######################################

    def getEditableAttrs(self):
        #@TODO: this model is really straining: available isn't editable..
        #(but I need it here for now so ObjectView can find available..)
        return super(Product,self).getEditableAttrs() + ['picture','available']

    def delete(self):
        self.categories.delete()
        #@TODO: clean this up:
        for style in self.styles:
            style.delete()
        super(Product,self).delete()


    def save(self):
        if self._pic:
            self._pic.save()
            self.pictureID = self._pic.ID

        # check for dulplicate codes:
        where = "code = '%s'" % (self.code)
        if self.ID:
            where = where + "AND ID != %i" % int(self.ID)
        if self._ds.select(self._tablename, where):
            raise ValueError, "This code already exists!"

        super(Product,self).save()
        self.categories.save()


    ## accessors ###############################################

    def get_price(self):
        return zdc.FixedPoint(self._data.get('price', '0.00'))

    def get_cost(self):
        return zdc.FixedPoint(self._data.get('cost', '0.00'))

    def get_retail(self):
        return zdc.FixedPoint(self._data.get('retail', '0.00'))

    def get_available(self):
        #@TODO: this is where styled/unstyled distinction
        # would come in handy
        res = (self.stock or 0) - self.hold
        for item in self.styles:
            res = res + (item.stock or 0) - item.hold
        return res
    
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
                self._pic = Picture(self._ds, ID=self.pictureID)
            else:
                self._pic = Picture(self._ds)
        return self._pic


    def get_styles(self):
        if not self._data.has_key("_styles"):
            self._data["_styles"] = zdc.LinkSet(self,
                                                zikeshop.Style,
                                                "parentID")
        return self._data["_styles"]

    ## category junction stuff #########################################


    def get_categories(self):
        if not self._data.has_key("cats"):
            self._data["cats"] = zdc.Junction(self,
                                              zikeshop.Category,
                                              "shop_product_node",
                                              "productID", "nodeID")
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
        from zikeshop import Category
        for catID in vals:
            self.categories << Category(self._ds, "@TODO: fixme!", ID=catID)

    def get_label(self):
        return self.name

    def __str__(self):
        return self.label
