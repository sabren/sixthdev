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

        ed = zikebase.ObjectEditor(zikebase.Node, ID=1)
        try:
            gotError = 0
            ed.act({"action":"save", "parentID":"1"})
        except:
            gotError = 1

        assert gotError, \
               "shouldn't be able to assign Nodes to themselves!!"
        
