"""
Category - a Node with Products in it.
"""
__ver__="$Id$"



import zikeshop, zdc, zikebase
zikebase.load("Node")

class Category(zikebase.Node):
    __super = zikebase.Node
#@TODO: make products into a junction.. (waiting on ability to << junctions)
##     _links = {
##         "products": [zdc.Junction, zikeshop.Product, "nodeID", "productID",
##                      'shop_product_node']
##         }
        
    _tuples = ["crumbs", "children", "products"] # @TODO: clean this up!

    def get_products(self):
        import zikeshop
        res =  map(lambda id: zikeshop.Product(ID=id),
                   map(lambda n: n["ID"],
                       self.__q_products()))
        return res
 
    def __q_products(self):
        res = []
        if self.ID:
            cur = self._table.dbc.cursor()
            sql =\
                """
                SELECT p.ID, code, name, price, productID, pictureID, descript
                FROM  shop_product p
                     LEFT JOIN shop_product_node pn on p.ID=pn.productID
                WHERE nodeID=%s
                ORDER BY code
                """ % self.ID
            cur.execute(sql)
            for row in cur.fetchall():
                #@TODO: fetchall to recordset should be automatic
                res.append({"ID": row[0], "code": row[1], "name":row[2],
                            "price":row[3], "productID": row[4],
                            "pictureID":row[5], "descript":row[6]})
        return res

