"""
e_product.py - product administration for zikeshop

$Id$
"""

import zikebase
import zikeshop
import weblib
import zdc
        
weblib.auth.check()


def showForm(prod):
    if prod.ID:
        print "<b>edit this product:</b>"
    else:
        print "<b>add a new product:</b>"
        prod.descriptLong = ''
        prod.name = ''
        prod.code = ''


    print '<table width="90%"><tr><td width="50%" style="background:silver">'
    print '<form action="e_product.py" method="POST" ' \
          'enctype="multipart/form-data">'
    if prod.ID:
        print '<input type="hidden" name="ID" value="%s">' % prod.ID
    print 'code: <input type="text" name="code" value="%s"><br>' \
          % prod.code
    print 'name: <input type="text" name="name" value="%s"><br>' \
          % prod.name

    print 'price: $<input type="text" name="price" size="7" value="%s">'\
          % weblib.deNone(prod.price)
    print 'retail: $<input type="text" name="retail" size="7" value="%s"><br>'\
          % weblib.deNone(prod.retail)

    print 'weight (lbs):' \
          '<input type="text" name="weight" size="7" value="%s"><br>'\
          % weblib.deNone(prod.weight)

    print 'categories:<br>'
    cur = zikeshop.dbc.cursor()

    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    ## siteID
    #####################################################################


    if prod.nodeIDs:
        sql = "SELECT ID, path, ID in %s FROM base_node " \
              "WHERE siteID=%s ORDER BY path" \
              % (zdc.sqlSet(prod.nodeIDs), weblib.auth.user.siteID)
    else:
        sql = "SELECT ID, path, 0 FROM base_node " \
              "WHERE siteID=%s ORDER BY path" \
              % weblib.auth.user.siteID

    cur.execute(sql)
    print weblib.selectBox("nodeIDs", cur.fetchall(), extra="MULTIPLE")
    print '<br>'

    print 'description:<br>'
    print '<textarea cols="30" rows="5" name="descript">'
    print '%s</textarea><br>' % weblib.deNone(prod.descript)


    print 'email you when inventory drops to:'
    print '<input type="text" name="instock_warn" value="%s" size="5"><br>' \
          % weblib.deNone(prod.instock_warn)
    print '<i>(leave blank if you don\'t want email)</i><br>'


    print '<input type="checkbox" name="isHidden"'
    if prod.isHidden:
        print ' CHECKED'
    print '> hide this product<br>'

    print '<br>upload a new picture:<br>'
    print '<input name="picture" type="file"><br>'
    
    print '<input name="action" value="save" type="submit">'
    print '</form>'

    
    print '<a href="e_product.py?action=delete&ID=%s">' % prod.ID
    print '[delete this product]</a>'


    if prod.pictureID:
        print '<td valign="top">Image:<br>'
        print '<img src="picture.py?ID=%s">' % prod.pictureID
    else:
        print '<td valign="top">'
        
    print '</td></tr></table>'



if __name__=="__main__":
    import header
    
    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    zikeshop.Product._defaults["siteID"]=weblib.auth.user.siteID
    
    
    if weblib.request.get("ID"):
        ed = zikebase.ObjectEditor(zikeshop.Product, ID=weblib.request["ID"])
    else:
        ed = zikebase.ObjectEditor(zikeshop.Product)

    
    ## @TODO: make ObjectEditor robust enough to do type-checking ##
    ## @TODO: ObjectEditor should allow user to empty out a field.
    ## @TODO: ObjectEditor should handle booleans (checkboxes)
    # meanwhile:
    # <kludge>
    if weblib.request.get("action"):
        for item in ("instock_warn", "price", "retail"):
            if weblib.request.form.get(item) == "":
                del weblib.request.form[item]
                setattr(ed.object, item, None)


        # do this bit so that 
        if weblib.request.form.get("nodeIDs") is None:
            ed.object.nodeIDs = ()


        weblib.request.form["isHidden"] = weblib.request.get("isHidden")=="on"


        if weblib.request.get("action"):
            productID = ed.object.ID
        
    # </kludge>


    ed.object.ts = None # activate timestamp @TODO: have RecordObject do this..
    try:
        ed.act()
    except ValueError, msg:
        #@TODO: redisplay results on ValueError.
        assert 0, str(msg) + " .. Click your back button to try again."


    if not weblib.request.get("action"):
        showForm(ed.object)

    elif weblib.request["action"]=="delete":
        cur = zikeshop.dbc.cursor()
        cur.execute("SELECT ID FROM shop_style WHERE productID=%s" % productID)
        for row in cur.fetchall():
            cur.execute("DELETE FROM shop_inventory WHERE styleID=%s" % row[0])
        cur.execute("DELETE FROM shop_style where productID=%s" % productID)

        import l_product
        l_product.show()
        
    else:
        import v_product
        v_product.show(zikeshop.Product(ID=ed.object.ID))
