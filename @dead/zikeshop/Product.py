"""
Product.py - product object for zikeshop

$Id$
"""

import zdc
import zikeshop

class Product(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_product")
    _defaults = {}
    _tuples = ['nodeIDs']
    
    nodeIDs = ()

    def _init(self):
        self.nodeIDs = ()
            

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
        
            
    def getNodes(self):
        import zikebase
        res = []
        for nodeID in self.nodeIDs:
            res.append(zikebase.Node(ID=row[0]))
        return res



    def deleteNodes(self):
        cur = self._table.dbc.cursor()
        cur.execute("DELETE FROM shop_product_node WHERE productID=%s" % int(self.ID))
        self.nodeIDs = ()
        

    def delete(self):
        self.deleteNodes()
        zdc.RecordObject.delete(self)


    def save(self):
        zdc.RecordObject.save(self)

        # and handle the nodes:
        nodeIDs = self.nodeIDs
        self.deleteNodes()
        self.nodeIDs = nodeIDs
        
        cur = self._table.dbc.cursor()        
        for id in self.nodeIDs:
            cur.execute("INSERT INTO shop_product_node (nodeID, productID) " + \
                        "VALUES (%s, %s)" % (id, int(self.ID)))

