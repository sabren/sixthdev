
import unittest
import sixthday.spec
from sixthday import Node
from strongbox import Clerk

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.clerk = sixthday.spec.clerk
        self.cur = sixthday.spec.dbc.cursor()

        self.cur.execute("DELETE FROM base_node")
        self.cur.execute("INSERT INTO base_node (name, path) "
                         "VALUES ('top', 'top')")
        self.cur.execute("INSERT INTO base_node (name, path, parentID) "
                         "VALUES ('sub', 'top/sub', 1)")
        self.cur.execute("INSERT INTO base_node (name, path, parentID) "
                         "VALUES ('subsub', 'top/sub/subsub/', 2)")


    def check_crumbs(self):
        node = self.clerk.load(Node, ID=1)
        goal = []
        assert node.crumbs == goal, \
               "Didn't get right crumbs for node 1."

        node = self.clerk.load(Node, ID=3)
        goal = [{"ID": 1,  "name": "top",  "path": "top"},
                {"ID": 2,  "name": "sub",  "path": "top/sub"}]
        assert len(node.crumbs) == len(goal), \
               "Didn't get right crumbs for node 3."
        


    def check_q_children(self):
        node = self.clerk.load(Node, ID=1)
        assert len(node.q_children()) == 1, \
               "wrong q_children"
    

    def check_path(self):
        node = self.clerk.load(Node, ID=2)
        node.name="subnode"
        node.save()

        assert node.path == "top/subnode", \
               "Node has wrong path after name change: %s" % node.path



    def check_setPath(self):
        node = self.clerk.new(Node)
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

        node1 = self.clerk.load(Node, ID=1)
        node1.name="super"
        node1.save()

        node2 = self.clerk.load(Node, ID=2)
        assert node2.path == "super/sub", \
               "wrong child after updatePaths: %s" % node2.path

        node3 = self.clerk.load(Node, ID=3)
        assert node3.path == "super/sub/subsub", \
               "updatePaths doesn't update grandchildren properly."

        

    def check_parent(self):
        node = self.clerk.load(Node, ID=2)
        assert isinstance(node.parent, Node), \
               ".parent doesn't return a Node"    


    def check_recusionCheck(self):

        # if you assign a node to itself, it's bad juju,
        # because of the check for children, you can
        # never delete it! So, we want to prevent that.

        node = self.clerk.load(Node, ID=1)
        try:
            gotError = 0
            node.parentID = 1
        except:
            gotError = 1

        assert gotError, \
               "didn't get error assigning a node to itself."


        # need to handle strings, too, because of the web.

        try:
            gotError = 0
            node.parentID = "1"
        except:
            gotError = 1

        assert gotError, \
               "didn't get error assigning a node to itself when using string"
