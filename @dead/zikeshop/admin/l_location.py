"""
l_location.py - shows all locations (admin screen)

$Id$
"""

import zikeshop
import weblib

def show():

    print "<b>locations</b>&nbsp;&nbsp;&nbsp;"
    cur = zikeshop.dbc.cursor()

    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################

    sql ="SELECT ID, name FROM shop_location where siteID=%s order by name" \
                % weblib.auth.user.siteID

    cur.execute(sql)
    print '<b><a href="e_location.py">[add new]</a></b><br>'

    for row in cur.fetchall():
        print '<A HREF="e_location.py?ID=%s">%s</a><br>' % (row[0], row[1])


if __name__=="__main__":
    weblib.auth.check()    
    import header
    show()
