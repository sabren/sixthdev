"""
e_product.py - product administration for zikeshop

$Id$
"""

import zikebase
import zikeshop
import weblib
import zdc
        

def show(prod):

    cur = zikeshop.dbc.cursor()
    
    print '<h3>view product</h3>'
    print '<table border="0"><tr><td width="300">'

    print '<b>code:</b> %s<br>' % prod.code
    print '<b>name:</b> %s<br>' % prod.name
    print '<b>price:</b> $%s<br>' % weblib.deNone(prod.price)
    print '<b>retail:</b> $%s<br>' % weblib.deNone(prod.retail)
    print '<b>weight:</b> %s lbs<br>' % weblib.deNone(prod.weight)
    print '<b>categories:</b><br>'

    if prod.nodeIDs:
        sql = "SELECT ID, path FROM base_node WHERE ID in %s AND siteID=%s ORDER BY path" \
              % (zdc.sqlSet(prod.nodeIDs), weblib.auth.user.siteID)
        cur.execute(sql)
        for row in cur.fetchall():
            print '<a href="l_product.py?nodeID=%s">%s</a><br>' % (row[0], row[1])
    else:
        print 'Not in any categories.<br>'
        
    print '<b>description:</b><br>%s<br>' % weblib.deNone(prod.descript)

    print '<b>picture:</b><br>'
    if prod.pictureID:
        print '<img src="picture.py?ID=%s"><br>' % prod.pictureID
    else:
        print 'No picture<br>'

    print '[<a href="e_product.py?ID=%s">edit this product</a>]' % prod.ID


    print '</td><td valign="top">'

    print '<b>styles/inventory:</b><br>'

    sql = weblib.trim(
        """
        SELECT S.ID, style, sum(amount) instock
        FROM shop_style S LEFT JOIN shop_inventory I ON S.ID = I.styleID 
        WHERE productID=%s
        GROUP BY style
        """) % prod.ID
    
    cur.execute(sql)

    if cur.rowcount:
        print '<table>'
        for row in cur.fetchall():
            print '<tr><td><a href="e_style.py?ID=%s">%s</a></td><td>%i</td>' % row
            print '<td></td></tr>'
        print '</table>'
    else:
        print 'no styles defined.<br>'

    print '[<a href="e_style.py?productID=%s">add style</a>]' % prod.ID
    print '[<a href="e_inventory.py?productID=%s">update inventory</a>]<br>' % prod.ID

    print '</td></tr></table>'

if __name__=="__main__":
    weblib.auth.check()
    import header
    
    assert weblib.request["ID"], "no ID specified"
    prod = zikeshop.Product(ID=weblib.request["ID"])
    assert prod.siteID == weblib.auth.user.siteID, "not your product"
    show(prod)


