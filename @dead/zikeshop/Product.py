
import zdc
import zikeshop

class Product(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_product")
    _defaults = {}
    _tuples = ['nodeIDs']


    def set_nodeIDs(self, IDs):
        """expects a tuple"""
        assert self.ID, "can't set nodeIDs until we have an ID"
        cur = self._table.dbc.cursor()
        cur.execute("DELETE FROM shop_product_node WHERE productID=%s" % int(self.ID))
        for id in IDs:
            cur.execute("INSERT INTO shop_product_node (nodeID, productID) " + \
                        "VALUES (%s, %s)" % (id, int(self.ID)))


    def get_nodeIDs(self):
        """returns a tuple"""
        res = ()
        if self.ID:
            cur = self._table.dbc.cursor()
            cur.execute("select nodeID from shop_product_node " + \
                        "where productID=%s ORDER BY nodeID" % int(self.ID))

            # cur.execute returns a tuple of tuples, eg ((1,), (2,) ...)
            # we only want the first value (column) from each tuple.
            if cur.rowcount:
                res = tuple(reduce(lambda x, y: x+[int(y[0])], cur.fetchall(), []))
                
        return res
        
            
    def getNodes(self):
        import zikebase
        res = []
        cur = self._table.dbc.cursor()
        if self.ID:
            cur.execute("select nodeID from shop_product_node where productID=%s" \
                        % self.ID)
            for row in cur.fetchall():
                res.append(zikebase.Node(ID=row[0]))

        return res


