import arlo
import unittest
import sixthday.spec
from sixthday import Node

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.clerk = arlo.MockClerk(dbmap={
            Node.__attrs__["parent"]: (Node, "parentID"),
            Node.__attrs__["children"]: (Node, "parentID"),
            })
        s = self.clerk.storage
        
        # we use the storage object so we can define the
        # database without dealing with read-only attribures (path)
        s.store("Node", name='top', path='top', parentID=0)
        s.store("Node", name='sub', path='top/sub', parentID=1)
        s.store("Node", name='subsub', path='top/sub/sub', parentID=2)

        #import pdb; pdb.set_trace()

    def check_crumbs(self):
        node = self.clerk.fetch(Node, 1)
        assert node.crumbs == [], \
               "Didn't get right crumbs for node 1."

        node = self.clerk.fetch(Node, ID=3)
        goal = [{"ID": 1,  "name": "top",  "path": "top"},
                {"ID": 2,  "name": "sub",  "path": "top/sub"}]
        assert len(node.crumbs) == len(goal), \
               "Didn't get right crumbs for node 3."
        

    def check_path(self):
        node = self.clerk.fetch(Node, 2)
        node.name="subnode"
        node = self.clerk.store(node)
        assert node.path == "top/subnode", \
               "Node has wrong path after name change: %s" % node.path



##     def check_setPath(self):
##         node = Node()
##         try:
##             gotError = 0
##             node.path = "XXXX"
##         except TypeError:
##             gotError = 1
##         assert (gotError) and (node.path != "XXXX"), \
##                "Node.path is supposed to be read only!"
            


##     def check_updatePaths(self):
##         # idle thought... this really doesn't account for record
##         # locking... if a child is in memory, and you updatePaths,
##         # it could be in conflict with the data in memory.. :/

##         node1 = self.clerk.fetch(Node, 1)
##         node1.name="super"
##         self.clerk.store(node1)

##         node2 = self.clerk.fetch(Node, 2)
##         assert node2.path == "super/sub", \
##                "wrong child after updatePaths: %s" % node2.path

##         node3 = self.clerk.fetch(Node, 3)
##         assert node3.path == "super/sub/subsub", \
##                "updatePaths doesn't update grandchildren properly."

        

    def check_parent(self):
        node = self.clerk.fetch(Node, 2)
        assert isinstance(node.parent, Node), \
               ".parent doesn't return a Node"    


##     def check_recursionCheck(self):

##         # if you assign a node to itself, it's bad juju,
##         # because of the check for children, you can
##         # never delete it! So, we want to prevent that.

##         node = self.clerk.fetch(Node, 1)
##         try:
##             gotError = 0
##             node.parentID = 1
##         except:
##             gotError = 1

##         assert gotError, \
##                "didn't get error assigning a node to itself."


##         # need to handle strings, too, because of the web.

##         try:
##             gotError = 0
##             node.parentID = "1"
##         except:
##             gotError = 1

##         assert gotError, \
##                "didn't get error assigning a node to itself when using string"
