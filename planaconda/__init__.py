
from strongbox import *
from pytypes import FixedPoint
import sixthday

class Node(sixthday.Node):
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
        return BoxView(self._getInstance(Node))
    
    

