
import zdc
import zikeshop

class Product(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_product")
    _defaults = {}

    def getNodes(self):
        res = []
        cur = self._table.dbc.cursor()
        if self.ID:
            cur.execute("select nodeID from shop_product_node where parentID=%s" % self.ID)
            for row in cur.fetchall():
                res.append(Node(ID=row[0]))

        return res
