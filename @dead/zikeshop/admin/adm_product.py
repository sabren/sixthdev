"""
adm_product.py - product administration for zikeshop

$Id$
"""

import zikeshop
import weblib
import zdc
import sys


class ObjectEditor:
    """A class for editing descendents of zdc.Object"""

    ## attributes ########################################

    what   = None # what class?
    object = None # an instance of the class
    input  = {}

    ## constructor #######################################

    def __init__(self, what, **args):
        """ex: objed=ObjectEditor(Person, fName="fred", lName="smith")"""
        self.what = what
        self.object = apply(self.newObject, (), args)


    ## public methods ####################################

    def newObject(self, **which):
        """Create a new instance of whatever class we're editing."""
        
        ## this next bit is python magic that will
        ## create a "what" and pass "where" to the
        ## constructor, assigning the result to self.object
        ##
        ## in the example above, objed.object would be
        ## a Person object representing "fred smith".
        
        return apply(self.what, (), which)


    def act(self, input):
        """objed.act(input) #input=a dict with a key called 'action'."""

        self.input = input
        if input.has_key("action"):
            method = "act_" + input["action"]

            ## more python magic to call the method:
            if hasattr(self, method):
                apply(getattr(self, method), ())
            else:
                raise "Don't know how to %s!" % action

        else:
            pass # do nothing - no action given


    def tuplize(self, input):
        if type(input) != type(()):
            return (input)
        else:
            return input


    ## actions ###########################################

    def act_delete(self):
        self.object.delete()
        self.object = self.newObject()
        

    def act_save(self):
        for field in self.object.getEditableAttrs():
            if self.input.has_key(field):
                setattr(self.object, field, self.input[field])
        for field in self.object.getEditableTuples():
            print "<h2>DOING %s</h2>" % field
            if self.input.has_key(field):
                setattr(self.object, field, self.tuplize(self.input[field]))
        self.object.save()


        

def showForm(prod):
    if prod.ID:
        print "<b>this is 'edit' mode</b>"
    else:
        print "<b>this is 'add' mode</b>"
        prod.descriptLong = ''
        prod.product = ''
        prod.code = ''

    print '<form action="adm_product.py" method="POST">'
    if prod.ID:
        print '<input type="hidden" name="ID" value="%s">' % prod.ID
    print 'code: <input type="text" name="code" value="%s"><br>' \
          % prod.code
    print 'product: <input type="text" name="product" value="%s"><br>' \
          % prod.product

    print 'categories:<br>'
    cur = zikeshop.dbc.cursor()
    if prod.nodeIDs:
        sql = "SELECT ID, path, ID in %s FROM base_node order by path" \
              % zdc.sqlSet(prod.nodeIDs)
    else:
        sql = "SELECT ID, path, 0 from base_node order by path"
    cur.execute(sql)
    print weblib.selectBox("nodeIDs", cur.fetchall(), extra="MULTIPLE")
    print '<br>'

    print 'description:<br>'
    print '<textarea cols="30" rows="5" name="descriptLong">'
    print '%s</textarea><br>' % prod.descriptLong
    print '<input name="action" value="save" type="submit">'
    print '</form>'


def showProductLinks():
    cur = zikeshop.dbc.cursor()
    cur.execute(
        "SELECT ID, code, product FROM shop_product order by code")

    print '<b><a href="adm_product.py">add new</a></b><br>'
    for row in cur.fetchall():
        print '<A HREF="adm_product.py?action=delete&ID=%s">[x]</a>' \
              % (row[0],)
        print '<A HREF="adm_product.py?ID=%s">%s</a>' % (row[0], row[1]),
        print row[2], "<br>"


if __name__=="__main__":
    import zikeshop.admin.header

    if weblib.request.get("ID"):
        ed = ObjectEditor(zikeshop.Product, ID=weblib.request["ID"])
    else:
        ed = ObjectEditor(zikeshop.Product)

    ed.act(weblib.request)

    showForm(ed.object)
    print '<hr>'
    showProductLinks()
    print '<hr>'
    print 'zikeshop alpha (c)2000 zike interactive, inc'
