"""
Category - a Node with Products in it.

$Id$
"""
import zikeshop
import zikebase
zikebase.load("Node")

class Category(zikebase.Node):
    

    def q_products(self):
        cur = self._table.dbc.cursor()
        cur.execute(
            """
            SELECT ID, code, name, productID FROM shop_product p
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
                        "productID": row[3]})
        return res



    ### FIX THIS LATER (siteID reference) #######################
    def q_children(self):
        res = []
        cur = self._table.dbc.cursor()
        if self.ID is not None:
            cur.execute("select ID from base_node where parentID=%s and siteID=%s" \
                        % (self.ID, zikeshop.siteID))
            for row in cur.fetchall():
                node = Category(ID=row[0])
                res.append( {"ID": node.ID, "name": node.name, "path": node.path } )
        return res

