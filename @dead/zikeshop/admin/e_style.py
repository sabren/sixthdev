"""
e_style.py - style administration for zikeshop

$Id$
"""

import zikeshop
import zikebase
import weblib
import zdc

class Style(zikeshop.Style):
    _defaults = {'style':'',
                 'productID': weblib.request.get("productID")}


def show(style):

    if style.ID:
        print "<b>edit this style:</b>"
    else:
        print "<b>add a new style:</b>"

    print '<form action="e_style.py" method="POST">'
    print 'name: <input type="text" name="style" value="%s"><br>' % style.style
    print '<input type="hidden" name="productID" value="%s">' % style.productID

    if style.ID:
        print '<input type="hidden" name="ID" value="%s">' % style.ID
        print '<a href="e_style.py?action=delete&ID=%s">'\
              '[delete this style]</a>'\
              % style.ID

    print '<input type="submit" name="action" value="save">'
    print '</form>'
    


if __name__=="__main__":
    weblib.auth.check()    
    import header

    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    Style._defaults["siteID"]=weblib.auth.user.siteID

    if weblib.request.get("ID"):
        ed = zikebase.ObjectEditor(Style, ID=weblib.request["ID"])
    else:
        ed = zikebase.ObjectEditor(Style)
    prodID = ed.object.productID # for the v_product line, below
    ed.act()


    if not weblib.request.get("action"):
        show(ed.object)
    else:
        import v_product
        v_product.show(zikeshop.Product(ID=prodID))

