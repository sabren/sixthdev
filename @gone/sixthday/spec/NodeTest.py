
import unittest
import zikebase
import zikebase.test

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.ds = zikebase.test.dbc
        self.cur = zikebase.test.dbc.cursor()

        self.cur.execute("DELETE FROM base_node")
        self.cur.execute("INSERT INTO base_node (name, path) "
                         "VALUES ('top', 'top')")
        self.cur.execute("INSERT INTO base_node (name, path, parentID) "
                         "VALUES ('sub', 'top/sub', 1)")
        self.cur.execute("INSERT INTO base_node (name, path, parentID) "
                         "VALUES ('subsub', 'top/sub/subsub/', 2)")


    def check_crumbs(self):
        node = zikebase.Node(self.ds, ID=1)
        goal = []
        assert node.crumbs == goal, \
               "Didn't get right crumbs for node 1."

        node = zikebase.Node(self.ds, ID=3)
        goal = [{"ID": 1,  "name": "top",  "path": "top"},
                {"ID": 2,  "name": "sub",  "path": "top/sub"}]
        assert len(node.crumbs) == len(goal), \
               "Didn't get right crumbs for node 3."
        


    def check_q_children(self):
        node = zikebase.Node(self.ds, ID=1)
        assert len(node.q_children()) == 1, \
               "wrong q_children"
    

    def check_path(self):
        node = zikebase.Node(self.ds, ID=2)
        node.name="subnode"
        node.save()

        assert node.path == "top/subnode", \
               "Node has wrong path after name change: %s" % node.path



    def check_setPath(self):
        node = zikebase.Node(self.ds)
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

        node1 = zikebase.Node(self.ds, ID=1)
        node1.name="super"
        node1.save()

        node2 = zikebase.Node(self.ds, ID=2)
        assert node2.path == "super/sub", \
               "wrong child after updatePaths: %s" % node2.path

        node3 = zikebase.Node(self.ds, ID=3)
        assert node3.path == "super/sub/subsub", \
               "updatePaths doesn't update grandchildren properly."

        

    def check_parent(self):
        node = zikebase.Node(self.ds, ID=2)
        assert isinstance(node.parent, zikebase.Node), \
               ".parent doesn't return a Node"    


    def check_recusionCheck(self):

        # if you assign a node to itself, it's bad juju,
        # because of the check for children, you can
        # never delete it! So, we want to prevent that.

        node = zikebase.Node(self.ds, ID=1)
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
