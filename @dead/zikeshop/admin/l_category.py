"""
l_category.py - shows all categories (admin screen)

$Id$
"""

import zikeshop
import weblib

def show():

    print "<b>categories</b>&nbsp;&nbsp;&nbsp;"
    cur = zikeshop.dbc.cursor()

    #####################################################################
    ### note to self: TAKE THIS OUT BEFORE CHECKING IN ##################
    #####################################################################
    ## i put the siteID in this one... this probably ought to be swept
    ## away into some kind of query repository...
    ##
    ## alternatively, this could have its own treeID, and I'd only have
    ## to tie nodes to trees..
    #####################################################################

    sql ="SELECT ID, path FROM base_node where siteID=%s order by path" \
                % weblib.auth.user.siteID

    cur.execute(sql)
    print '<b><a href="e_category.py">[add new]</a></b><br>'

    for row in cur.fetchall():
        print '<A HREF="e_category.py?ID=%s">%s</a><br>' % (row[0], row[1])


if __name__=="__main__":
    weblib.auth.check()    
    import header
    show()
