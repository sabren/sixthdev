"""
Category - a Node with Products in it.

$Id$
"""
import zikeshop
import zikebase
zikebase.load("Node")

class Category(zikebase.Node):
    __super = zikebase.Node
    _tuples = ["crumbs", "children", "products"] # @TODO: clean this up!

    def get_products(self):
        #@TODO: clean this junk up and make it a LinkSet!!!!
        import zikeshop
        return map(lambda id: zikeshop.Product(ID=id),
                   map(lambda n: n["ID"],
                       self.q_products()))
    
    # @TODO: get rid of all this q_xxx nonsense.. objectView is better
    def q_products(self):
        cur = self._table.dbc.cursor()
        cur.execute(
            """
            SELECT p.ID, code, name, price, productID, pictureID
            FROM  shop_product p
                 LEFT JOIN shop_product_node pn on p.ID=pn.productID
            WHERE nodeID=%s and siteID=%s
            ORDER BY code
            """
            % (self.ID, zikeshop.siteID)
            )
        res = []
        for row in cur.fetchall():
            #@TODO: fetchall to recordset should be automatic
            res.append({"ID": row[0], "code": row[1], "name":row[2],
                        "price":row[3], "productID": row[4],
                        "pictureID":row[5]})
        return res



    ### FIX THIS LATER (siteID reference) #######################
    def q_children(self):
        import weblib
        res = []
        cur = self._table.dbc.cursor()
        if self.ID is not None:
            cur.execute("select ID from base_node where parentID=%s"
                        % self.ID)
            for row in cur.fetchall():
                node = Category(ID=row[0])
                res.append( {"ID": node.ID, "name": node.name,
                             "path": node.path,
                             "encpath":weblib.urlEncode(node.path) } )
        return res


