
from strongbox import *
from pytypes import FixedPoint
import sixthday

class Node(sixthday.Node):
    ID = attr(int, default=0)
    data = attr(str)
    ntype = attr(str, okay=["project","goal","task"], default="task")
    estimate = attr(FixedPoint)
    revised = attr(FixedPoint)
    actual = attr(FixedPoint)
    importance = attr(int, okay=range(10))
    isOnPlate = attr(int, okay=[True,False], default=False)
    status = attr(str, default="unclear",
                  okay=["unclear", "to do", "in progress",
                        "complete", "rejected"])

Node.__attrs__["parent"].type = Node
Node.__attrs__["children"].type = Node
    

class PlanApp(sixthday.AdminApp):

    def viewListProject(self):
        projs = self.clerk.match(Node, ntype="project")
        return {'projects': [BoxView(p) for p in projs] }

    def formEditNode(self):
        model = {}
        node = self._getInstance(Node)
        if node.parent is None:
            node.parent = Node()
        model.update(BoxView(node))
        nodes = [(n.ID, n.path) for n in self.clerk.match(Node)]
        model["nodes"] = [(0, "/")] + nodes
        return model

    def postSaveNode(self):
        parentID = self.input.get("parent", "0")
        if int(parentID) == 0:
            root = Node(ID=0)
            root.private.isDirty = False
            self.input["parent"] = root
        else:
            self.input["parent"] = self.clerk.fetch(Node, ID=int(parentID))
        node = self.generic_save(Node)
        self.redirect("?action=viewNode&ID=%s" % node.ID)

    def viewNode(self):
        model = {}
        nodeID = self.input.get("ID", "0")
        if int(nodeID) == 0:
            node = Node(name="root")
            for n in self.clerk.match(Node):
                if node.parent is None:
                    node.children << n
        else:
            node = self._getInstance(Node)
        model.update(BoxView(node))
        model["crumbs"] = [BoxView(c) for c in node.crumbs]
        return model
    
    def viewPlate(self):
        nodes = self.clerk.match(Node, isOnPlate=True)
        nodes.sort(lambda a,b: cmp(a.importance, b.importance))
        return {"nodes": [BoxView(n) for n in nodes]} # @TODO: =~ listProject

