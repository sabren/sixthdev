"""
show products in particular nodes.

$Id$
"""

import zikebase
import zikeshop
import weblib


def show(nodeID=None):
    cur = zikeshop.dbc.cursor()


    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################

    # the dropdown box
    sql = "SELECT ID, path, 0 FROM base_node WHERE siteID=%s ORDER BY path" \
          % weblib.auth.user.siteID
    cur.execute(sql)
    print '<form action="l_product.py" METHOD="get">'
    print "show products in... "
    print weblib.selectBox("nodeID", cur.fetchall(), blank='')
    print '<input type="submit" value="go">'
    if nodeID is not None:
        print '<a href="l_product.py">[recent products]</a><br>'
    print '</form>'


    # now for the display:
    sql = "SELECT DISTINCT ID, code, name, pictureID " \
          "FROM shop_product p LEFT JOIN shop_product_node pn ON p.ID=pn.productID " \
          "WHERE siteID=%s " % weblib.auth.user.siteID

    if nodeID is None:
        title = "Recent products:"
        sql = sql + "ORDER BY ts DESC LIMIT 10"
    elif nodeID:
        node = zikebase.Node(ID=nodeID)
        assert node.siteID==weblib.auth.user.siteID, \
               "not your node."
        title = "Products in %s:" % node.path
        sql = sql + "AND pn.nodeID=%s" % nodeID
    else:
        title = "Products without a category:"
        sql = sql + "AND pn.nodeID IS NULL"


    
    #####################################################################
    #####################################################################
        
    cur.execute(sql)    

    print '<b>%s</b>' % title
    print '<a href="e_product.py">[add]</a>'
    print '<br>'

    for row in cur.fetchall():
        print '<A HREF="v_product.py?ID=%s">%s</a>' % (row[0], row[1]),
        print row[2], "<br>"




if __name__=="__main__":
    weblib.auth.check()
    import header
    show(weblib.request.get("nodeID"))





