
import weblib
from zikeshop import dbc


def showNodes():
    cur = dbc.cursor()
    cur.execute("select ID, name from base_node where parentID=0 order by name")

    print "<h1>top</h1>"
    if cur.rowcount:
        print "<h2>Categories</h2>"
    for row in cur.fetchall():
        print '<A href="category.py?nodeID=%s">%s</A><br>' % (row[0], row[1])


def showProds(nodeID):
    import zikebase

    # breadcrumb trail
    node = zikebase.Node(ID=nodeID)
    path = node.name
    while node.parentID:
        node = node.parent
        path = ('<A HREF="category.py?nodeID=%s">%s</a>' % (node.ID, node.name)) + \
               " : " + path
    print '<h1><A HREF="category.py">top</A> : %s</h1>' % path

    # children
    children = zikebase.Node(ID=nodeID).getChildren()
    if children:
        print "<h2>Subcategories</h2>"
    for child in children:
        print '<a href="category.py?nodeID=%s">%s</a>' % (child.ID, child.name)

    # products    
    cur = dbc.cursor()
    sql="SELECT code, product FROM shop_product p " + \
         "LEFT JOIN shop_product_node pn ON p.ID=pn.productID " + \
         "WHERE nodeID=%s " % nodeID + \
         "ORDER BY code"

    cur.execute(sql)
    print "<h2>Products in this category:</h2>"
    for row in cur.fetchall():
        print '<A href="product.py?code=%s">%s</A><br>' % (row[0], row[1])




if __name__ == "__main__":
    if weblib.request.has_key("nodeID"):
        showProds(weblib.request["nodeID"])
    else:
        showNodes()


    print "<hr>"
    print '<a href="cart.py">view cart</a>'
    print "<hr>"
    print "zikeshop alpha (c)2000 zike interactive, inc"
