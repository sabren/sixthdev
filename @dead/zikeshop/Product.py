"""
Product.py - product object for zikeshop
"""
__ver__="$Id$"

#@TODO: get rid of nodeIDs, replace with a join object.

import zdc
import zikebase
import zikeshop

class Product(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_product")
    _links = {
        #@TODO: we have a chicken and egg problem here...
        "styles": [zdc.LinkSet, None, "parentID"],
        }

    # @TODO: fix this!!!!!! there should be no _tuples..
    # or should there be? I DO need to tell ObjectView
    # that there's a collection called nodes...
    # I'm only doing it this way because I don't have
    # a *:* join object yet.
    #
    # I need this to display the product page
    # (this product is in ...)
    _tuples = ['nodes']
    
    ### Magic RecordObject Methods ############################

    def _init(self):
        self.nodeIDs = ()
        self._pic = None            

    def _new(self):
        self.__super._new(self)
        self._data['class'] = "product"
        self.price = 0
        self.retail = 0
        self.weight = 0
        self.parentID = 0
        self.inStock = 0
        self.onHold = 0


    def _fetch(self, **where):

        # same old thing...
        apply(zdc.RecordObject._fetch, (self,), where)
        
        # except we also get some nodeIDs:
        if self.ID:
            cur = self._table.dbc.cursor()
            cur.execute("select nodeID from shop_product_node " + \
                        "where productID=%s ORDER BY nodeID" % int(self.ID))

            # cur.execute returns a tuple of tuples, eg ((1,), (2,) ...)
            # we only want the first value (column) from each tuple.
            if cur.rowcount:
                self.nodeIDs = tuple(
                    reduce(lambda x, y: x+[int(y[0])], cur.fetchall(), []))
                
    def set_nodeIDs(self, value):
        msg = "Product.nodeIDs should be an int or sequence of ints."
        vals = []
        if type(value) == type(0):
            vals.append(value)
        elif type(value)==type(""):
            vals.append(int(value))
        elif type(value) in (type(()), type([])):
            for item in value:
                vals.append(int(item))
        else:
            raise TypeError, msg + ".. not %s" % type(value)
        self._data["nodeIDs"] = tuple(vals)
        

    ## Normal RecordObject Methods #######################################

    def getEditableAttrs(self):
        return zdc.RecordObject.getEditableAttrs(self) + ['picture']

    def delete(self):
        #@TODO: decrease inventory
        self._deleteNodes()
        for style in self.styles:
            style.delete()
        zdc.RecordObject.delete(self)


    def save(self):

        if self._pic:
            self._pic.save()
            self.pictureID = self._pic.ID

        # validation logic:
        sql = "SELECT name FROM shop_product " \
              "WHERE code='%s' AND siteID=%i " \
              % (self.code, zikeshop.siteID)
        if self.ID:
            sql = sql + "AND ID != %i" % int(self.ID)

        cur = self._table.dbc.cursor()        
        cur.execute(sql)
        if cur.rowcount:
            raise ValueError, "This code already exists!"
        

        zdc.RecordObject.save(self)

        # handle the nodes:
        nodeIDs = self.nodeIDs
        self._deleteNodes()
        self.nodeIDs = nodeIDs
        
        for id in self.nodeIDs:
            cur.execute("INSERT INTO shop_product_node (nodeID, productID) "
                        "VALUES (%s, %s)" % (id, int(self.ID)))


    ## accessors ###############################################

    def get_available(self):
        return self.inStock - self.onHold

    def get_price(self):
        return zikeshop.FixedPoint(self._data.get('price', '0.00'))

    def set_picture(self, blob):
        # on a multipart/form-data form,
        # if you don't upload a file, it still gives you
        # a string field.. this "if" copes with that.
        if type(blob) != type(""):
            self.get_picture()
            self._pic.picture = blob.value
            import zikeshop
            self._pic.siteID = zikeshop.siteID
            self._pic.type = blob.type

    def get_picture(self):
        if not self._pic:
            if self.pictureID:
                self._pic = zikebase.Picture(ID=self.pictureID)
            else:
                self._pic = zikebase.Picture()
        return self._pic


    def get_nodes(self):
        #@TODO: replace with a junction thingy..
        return map(lambda x: zikebase.Node(ID=x), self.nodeIDs)

    def get_styles(self):
        res = []
        if self.ID:
            sql = "SELECT ID from shop_product WHERE parentID=%s" % self.ID
            cur = zikeshop.dbc.cursor()
            cur.execute(sql)
            for row in cur.fetchall():
                res.append(zikeshop.Product(ID=row[0]))
        return res


        
    ## Other stuff ############################################

    def _deleteNodes(self):
        """
        delete nodes for this product. used internally.
        """
        cur = self._table.dbc.cursor()
        cur.execute("DELETE FROM shop_product_node WHERE productID=%s" \
                    % int(self.ID))
        self.nodeIDs = ()

