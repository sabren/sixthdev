"""
location administration for zikeshop

$Id$
"""

import zikeshop
import zikebase
import weblib
import zdc

class Location(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_location")
    _defaults = {'name':''}

    def delete(self):
        cur = self._table.dbc.cursor()
        cur.execute("DELETE FROM shop_inventory WHERE locationID=%s" % self.ID)
        zdc.RecordObject.delete(self)
        


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
    Location._defaults["siteID"]=weblib.auth.user.siteID

    if weblib.request.get("ID"):
        ed = zikebase.ObjectEditor(Location, ID=weblib.request["ID"])
    else:
        ed = zikebase.ObjectEditor(Location)
    ed.act()


    if not weblib.request.get("action"):
        show(ed.object)
    else:
        import l_location
        l_location.show()

