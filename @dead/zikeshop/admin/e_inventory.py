"""
e_inventory.py - manage inventory of a particular product

$Id$
"""

import weblib
import zikeshop


def show(prod):

    cur = zikeshop.dbc.cursor()

    ## first, make sure there's one record for every style-location pair.
    ## I'd prefer to do this with an INSERT INTO statement, but MySQL doesn't
    ## like having the destination table in the FROM clause..

    sql = weblib.trim(
        """
        SELECT L.ID, S.ID 
        FROM shop_location L, shop_style S
        LEFT JOIN shop_inventory I on (S.ID=I.styleID) AND (L.ID=I.locationID)
        WHERE (I.ID IS NULL) AND (S.productID=%s) AND (L.siteID=%s)
        """) % (prod.ID, weblib.auth.user.siteID)

    cur.execute(sql)
    for row in cur.fetchall():
        sql = "INSERT INTO shop_inventory (locationID, styleID, amount) " +\
              "VALUES (%s, %s, 0)" % row
        cur.execute(sql)


    ## now we can select the inventory data easily.

    sql = weblib.trim(
        """
        SELECT I.ID, L.name, S.style, I.amount
        FROM shop_inventory I, shop_location L, shop_style S
        WHERE (I.locationID=L.ID) AND (I.styleID=S.ID) and (S.productID=%s)
        ORDER BY L.name, S.style
        """) % prod.ID


    ## show the form:

    print weblib.trim(
        '''
        <h3>inventory</h3>
        Update inventory for <a href="v_product.py?ID=%s">%s: %s</a>
        in the boxes below.<br>
        <form action="e_inventory.py?productID=%s" method="POST">
        <table>
        ''') % (prod.ID, prod.code, prod.name, prod.ID)

    cur.execute(sql)
    loc = None
    for row in cur.fetchall():
        lastLoc = loc
        (ID, loc, style, amt) = row
        if lastLoc != loc:
            print '<tr><th colspan="2" align="left">%s</th></tr>' % loc
        print weblib.trim(
            '''
            <tr><td>%s</td>
            <td><input type="text" name="inv_%s" size="5" value="%s"></td></tr>
            ''') % (style, ID, amt)

    print weblib.trim(
        """
        </table>
        <input type="submit" name="action" value="save">
        </form>
        """)




if __name__=="__main__":
    weblib.auth.check()
    import header

    prod = zikeshop.Product(ID=weblib.request["productID"])
    assert prod.siteID == weblib.auth.user.siteID, "not your product"
    cur = zikeshop.dbc.cursor()

    if weblib.request.get("action")=="save":
        for item in weblib.request.keys():
            if item[:4]=="inv_":
                #@TODO: make updateInventory a Product method:
                cur.execute("update shop_inventory set amount=%s where ID=%s"
                            % (weblib.request[item], item[4:]))
                
        import v_product
        v_product.show(prod)
    else:
        show(prod)

