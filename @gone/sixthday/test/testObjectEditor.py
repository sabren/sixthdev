"""
testObjectEditor.py - test scripts for zikebase.ObjectEditor
"""
__ver__="$Id$"

# not everything is tested yet...
# ObjectEditor was refactored into existence from
# other, tested scripts..

import zikebase
import unittest
import zdc

class TestObjectClass(zdc.Object):
    __super = zdc.Object

    def _init(self):
        self.isTrue=1
        self.isAlsoTrue=1

    def _new(self):
        pass

    #@TODO: shouldn't the base Object class be more useful?
    def getEditableAttrs(self):
        return self._data.keys()
    def getEditableTuples(self):
        return []

    def save(self):
        pass




class ObjectEditorTestCase(unittest.TestCase):

    def setUp(self):
        self.ds = zikebase.test.dbc
        self.cur = zikebase.test.dbc.cursor()
        self.cur.execute("delete from base_node")

    def check_simple(self):
        """
        can we save a single node to the database?
        """        
        req = {"action":"save"}
        ed = zikebase.ObjectEditor(zikebase.Node, self.ds, req)
        ed.act()
        assert isinstance(ed.object, zikebase.Node), \
               "Didn't even create a simple node.."
        assert ed.object.ID == 1, \
               "didn't save node to database..."


    def check_editNode(self):
        """
        for some reason, it wasn't triggering error
        on a recursive node, even though the node
        object itself did.. (??)

        turns out it had to do with the fact that
        on the web, the parentID is a string..
        """
        node = zikebase.Node(self.ds)
        node.name="fred"
        node.save()

        req = {"action":"save", "parentID":"1"}
        ed = zikebase.ObjectEditor(zikebase.Node, self.ds, req, key=1)

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

        .expected() figures it out..
        """
        OEd = zikebase.ObjectEditor

        # case 1: single field is expected
        ed = OEd(TestObjectClass,
                 self.ds,
                 input={"__expect__":"name:fred"})
        assert ed.expected() == {'name':'fred'}, \
               "expected() screws up w/ just one field"

        # case 2: multiple fields...
        ed = OEd(TestObjectClass,
                 self.ds,
                 input={"__expect__":("fname:fred", "lname:tempy")})
        assert ed.expected() == {'fname':'fred', 'lname':'tempy'}, \
               "expected() screws up when __expect__ is a tuple"


        # case 3: invalid format - single field:
        try:
            gotError = 0
            ed = OEd(TestObjectClass, self.ds, input={"__expect__":"fred"})
            ex = ed.expected()
        except ValueError:
            gotError = 1
        assert gotError, \
               "didn't get valueError with bad __expect__ field"

        # case 4: invalid format - tuple:
        try:
            gotError = 0
            ed = OEd(TestObjectClass, self.ds,
                     input={"__expect__":("fname:fred", "lastname...?")})
            ex = ed.expected()
        except ValueError:
            gotError = 1
        assert gotError, \
               "didn't get valueError with bad __expect__ tuple"


    def check_expectations(self):
        """
        this just exercises the behaviour of objecteditor based
        on results from expected()..
        """
        ed = zikebase.ObjectEditor(TestObjectClass, self.ds, {})
        assert ed.object.isTrue, \
               "foo should be true by default!"

        #@TODO: type checking for formacceptor?
        #@TODO: rename objectEditor to FormAcceptor?
        ed.input = {"isTrue":"0"}
        ed.act("save")
        assert ed.object.isTrue == '0', \
               "that shoulda turned foo's isTrue field off."
        
        ed = zikebase.ObjectEditor(TestObjectClass, self.ds, {})
        ed.input = {"__expect__":"isTrue:0"}
        ed.act("save")
        assert ed.object.isTrue == '0', \
               "isTrue should be 0 because of __expect__."

        
        # now try testing two of 'em
        ed = zikebase.ObjectEditor(TestObjectClass, self.ds, {})
        ed.input = {"__expect__":("isTrue:0", "isAlsoTrue:0")}
        ed.act("save")
        assert ed.object.isTrue == '0', \
               "isTrue should be 0 because of __expect__."
        assert ed.object.isAlsoTrue == '0', \
               "isAlsoTrue should be 0 because of __expect__."




    def check_nested(self):
        """
        Sometimes, we want to save several objects at once.
        for example, in zikeshop's point of sale system
        we want to save a Sale object with several details.

        This test attemps to save a node and one subnode.
        """
        node = zikebase.Node(self.ds)
        node.name = 'general'
        node.save()

        nodeID = node.ID
        del node

        req = {
            "action":"save",
            "children(+0|parentID)":nodeID,
            "children(+0|name)":'specific',
            }
        
        ed = zikebase.ObjectEditor(zikebase.Node, self.ds, req, nodeID)
        ed.act()

        assert len(ed.object.children) == 1, \
               "wrong length for ed.object.children: %s" \
               % len(ed.object.children)


        # now check that it actually made it to the db..
        del ed
        node = zikebase.Node(self.ds, ID=nodeID)
        assert len(node.children) == 1, \
               "wrong length for node.children: %s" % len(node.children)

        assert node.children[0].name=='specific', \
               "wrong name for child node: %s" % node.children[0].name


