"""
e_category.py - category administration for zikeshop

$Id$
"""

import zikeshop
import zikebase
import weblib
import zdc


def show(node):

    if node.ID:
        print "<b>edit this category:</b>"
    else:
        print "<b>add a new category:</b>"
        node.name = ''
        node.parentID = 0
        node.descript = ''

    print '<form action="e_category.py" method="POST">'
    if node.ID:
        print '<input type="hidden" name="ID" value="%s">' % node.ID
    print 'name: <input type="text" name="name" value="%s"><br>' % node.name

    print 'subcategory of:'
    cur = zikeshop.dbc.cursor()
    if not node.ID:
        node.ID = 0

    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    ## added siteID
    #####################################################################

    sql = "SELECT ID, path, ID=%s FROM base_node WHERE siteID=%s " \
          % (node.parentID, weblib.auth.user.siteID)

    ## prevent loops in the tree:
    if node.path:
        sql = sql + "AND path NOT LIKE '%s%%' " % zdc.sqlEscape(node.path)

    ## alphabetize it:
    sql = sql + "ORDER BY path"

    cur.execute(sql)
    print weblib.selectBox("parentID", cur.fetchall(), blank=0)
    print '(optional) <br>'

    print 'description:<br>'
    print '<textarea cols="30" rows="5" name="descript">%s</textarea><br>' \
          % weblib.deNone(node.descript)
    print '<input name="action" value="save" type="submit">'
    print '</form>'
    

    if node.ID:
        print '<a href="e_category.py?action=delete&ID=%s">[delete this category]</a>'\
              % node.ID
    


if __name__=="__main__":
    weblib.auth.check()    
    import header

    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    zikebase.load("Node")
    zikebase.Node._defaults["siteID"]=weblib.auth.user.siteID

    if weblib.request.get("ID"):
        ed = zikebase.ObjectEditor(zikebase.Node, ID=weblib.request["ID"])
    else:
        ed = zikebase.ObjectEditor(zikebase.Node)
    ed.act()


    if not weblib.request.get("action"):
        show(ed.object)
    else:
        import l_category
        l_category.show()




