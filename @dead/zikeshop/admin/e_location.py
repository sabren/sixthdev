"""
location administration for zikeshop

$Id$
"""

import zikeshop
import zikebase
import weblib
import zdc


def show(location):

    if location.ID:
        print "<b>edit this location:</b>"
    else:
        print "<b>add a new location:</b>"

    print '<form action="e_location.py" method="POST">'
    print 'name: <input type="text" name="name" value="%s"><br>' \
          % location.name

    if location.ID:
        print '<input type="hidden" name="ID" value="%s">' % location.ID
        print '<a href="e_location.py?action=delete&ID=%s">' \
              '[delete this location]</a>'\
              % location.ID

        
    print '<input type="submit" name="action" value="save">'
    print '</form>'
    

if __name__=="__main__":
    weblib.auth.check()    
    import header
    
    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    zikeshop.Location._defaults["siteID"]=weblib.auth.user.siteID

    ed = zikebase.ObjectEditor(zikeshop.Location, weblib.request.get("ID"))
    ed.act()


    if not weblib.request.get("action"):
        show(ed.object)
    else:
        import l_location
        l_location.show()

