"""
testObjectEditor.py - test scripts for zikebase.ObjectEditor

$Id$
"""

# not everything is tested yet... ObjectEditor was refactored into existence from
# other, tested scripts..

import zikebase
import unittest


class ObjectEditorTestCase(unittest.TestCase):


    def check_editNode(self):

        # for some reason, it wasn't triggering error
        # on a recursive node, even though the node
        # object itself did.. (??)

        # ah.. turns out it had to do with the fact that
        # on the web, the parentID is a string..
        
        cur = zikebase.test.dbc.cursor()
        cur.execute ("delete from base_node")

        node = zikebase.Node()
        node.name="fred"
        node.save()

        ed = zikebase.ObjectEditor(
            zikebase.Node,
            {"action":"save", "parentID":"1"},
            ID=1)
        try:
            gotError = 0
            ed.act()
        except:
            gotError = 1

        assert gotError, \
               "shouldn't be able to assign Nodes to themselves!!"
        

    def check_expect(self):
        """
        Sometimes, especially when it comes to checkboxes, select
        boxes, and radio buttons, the browser won't send a value
        back if you don't select one.

        Say you're editing an object with a boolean field, which would
        be represented by a checkbox. There's three possibilities.

        - You set it to true.
        - You set it to false.
        - You leave it alone, or the field isn't on this form.

        Unfortunately, the browser only sends two possible values:
        
        - The value assigned to the checkbox (usually 'on')
        - nothing at all. 

        So, objectEditor supports a special (hidden) field called
        __expect__ .. example:

        <input type="hidden" name="__expect__" value="isTrue;0">
        <input type="checkbox" name="isTrue" value="1">

        Now objectEditor knows that 'isTrue' really was on the form,
        so if it doesn't get a value, use the default value specified
        after the semicolon. (0).

        You can have multiple __expect__ fields on a form.
        """
        
        class FooBar:
            def getEditableAttrs(self):
                return ['isTrue', 'isAlsoTrue']

            def getEditableTuples(self):
                #@TODO: get rid of EditableTuples, replace with addXXX,delXXX
                return []
            
            def save(self):
                pass

            def __init__(self, ID=None):
                self.isTrue = 1
                self.isAlsoTrue = 1
        
        ed = zikebase.ObjectEditor(FooBar)
        assert ed.object.isTrue, \
               "foo should be true by default!"

        #@TODO: type checking for formacceptor?
        #@TODO: rename objectEditor to FormAcceptor?
        ed.input = {"isTrue":"0"}
        ed.act("save")
        assert ed.object.isTrue == '0', \
               "that shoulda turned foo's isTrue field off."
        
        ed = zikebase.ObjectEditor(FooBar)
        ed.input = {"__expect__":"isTrue;0"}
        ed.act("save")
        assert ed.object.isTrue == '0', \
               "isTrue should be 0 because of __expect__."

        
        # now try testing two of 'em
        ed = zikebase.ObjectEditor(FooBar)
        ed.input = {"__expect__":("isTrue;0", "isAlsoTrue;0")}
        ed.act("save")
        assert ed.object.isTrue == '0', \
               "isTrue should be 0 because of __expect__."
        assert ed.object.isAlsoTrue == '0', \
               "isAlsoTrue should be 0 because of __expect__."
