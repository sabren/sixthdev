
import unittest
import zikebase
import zikebase.test

class NodeTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikebase.test.dbc.cursor()

        self.cur.execute("DELETE FROM base_node")
        self.cur.execute("INSERT INTO base_node (name, path) VALUES ('top', 'top')")
        self.cur.execute("INSERT INTO base_node (name, parentID) VALUES ('sub', 1)")

    

    def check_path(self):
        node = zikebase.Node(ID=2)
        node.name="subnode"

        assert node.path == "top/subnode", \
               "Node doesn't generate the proper path when name is changed."             



    def check_setPath(self):
        node = zikebase.Node()
        try:
            gotError = 0
            node.path = "XXXX"
        except TypeError:
            gotError = 1

        assert (gotError) and (node.path != "XXXX"), \
               "Node.path is supposed to be read only!"
            


    def check_updatePaths(self):
        # idle thought... this really doesn't account for record
        # locking... if a child is in memory, and you updatePaths,
        # it could be in conflict with the data in memory.. :/

        self.cur.execute("INSERT INTO base_node (name, parentID) VALUES ('subsub', 2)")

        node1 = zikebase.Node(ID=1)
        node1.name="super"
        node1.save()

        node2 = zikebase.Node(ID=2)
        assert node2.path == "super/sub", \
               "updatePaths doesn't update child nodes properly."

        node3 = zikebase.Node(ID=3)
        assert node3.path == "super/sub/subsub", \
               "updatePaths doesn't update grandchildren properly."

        


    def check_recusionCheck(self):

        # if you assign a node to itself, it's bad juju,
        # because of the check for children, you can
        # never delete it! So, we want to prevent that.

        node = zikebase.Node(ID=1)
        try:
            gotError = 0
            node.parentID = 1
        except:
            gotError = 1

        assert gotError, \
               "didn't get error assigning a node to itself."

        
        
