"""
Product.py - product object for zikeshop

$Id$
"""

import zdc
import zikebase
import zikeshop

class Product(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_product")
    _defaults = {
        "price": 0,
        }
    _tuples = ['nodeIDs']
    _pic = None

    ### Magic RecordObject Methods ############################

    def _init(self):
        self.nodeIDs = ()
        self._pic = None            

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
                

    def get_price(self):
        return zikeshop.FixedPoint(self._data['price'])


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
        

    ### picture handling stufff #####################

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


    ## Normal RecordObject Methods #######################################

    def getEditableAttrs(self):
        return zdc.RecordObject.getEditableAttrs(self) + ['picture']

    def delete(self):
        self.deleteNodes()
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
        self.deleteNodes()
        self.nodeIDs = nodeIDs
        
        for id in self.nodeIDs:
            cur.execute("INSERT INTO shop_product_node (nodeID, productID) "
                        "VALUES (%s, %s)" % (id, int(self.ID)))

        # handle the styles: @TODO: fix this!
        if not self.q_styles():
            # insert one blank style record:
            cur.execute("INSERT INTO shop_style (productID) VALUES (%s)" \
                        % self.ID)



    ## Queries ###############################################

    def q_nodes(self):
        import zikebase, weblib
        res = []
        for nodeID in self.nodeIDs:
            node = zikebase.Node(ID=nodeID)
            res.append({"ID": nodeID, "name":node.name, "path":node.path,
                        "encpath":weblib.urlEncode(node.path) })
        return res


    def q_styles(self):
        """Returns a list of dicts with ID, style, and instock amount
        for the product's styles"""

        cur = self._table.dbc.cursor()
        cur.execute(
            """
            SELECT s.ID, style, amount from shop_style s
            LEFT JOIN shop_inventory i ON s.ID=i.styleID
            WHERE s.productID=%s
            """ % self.ID)
        res = []
        for row in cur.fetchall():
            res.append({"ID":row[0], "style":row[1], "instock":row[2]})
        return res
        
        
    ## Other stuff ############################################

    def deleteNodes(self):
        cur = self._table.dbc.cursor()
        cur.execute("DELETE FROM shop_product_node WHERE productID=%s" \
                    % int(self.ID))
        self.nodeIDs = ()
