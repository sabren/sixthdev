
from strongbox import *
from pytypes import FixedPoint, DateTime
import sixthday

class Node(sixthday.Node):
    ID = attr(int, default=0)
    data = attr(str)
    name = attr(str)
    path = attr(str)
    ntype = attr(str, okay=["project","goal","task"], default="task")
    estimate = attr(FixedPoint)
    revised = attr(FixedPoint)
    actual = attr(FixedPoint)
    importance = attr(int, okay=range(10))
    isOnPlate = attr(int, okay=[True,False], default=False)
    status = attr(str, default="unclear",
                  okay=["unclear", "to do", "in progress",
                        "complete", "rejected"])
    parent = link(forward("planaconda.Node"))
    comments = linkset(forward("planaconda.Comment"), "node")

    def set_name(self, value):
        self.private.name = value
        if self.parent:
            self.private.path = self.parent.path + "/" + value
        else:
            self.path = "/" + value

    def set_parent(self, value):
        self.private.parent = value
        self.name = self.name


class Comment(Strongbox):
    ID = attr(int, default=0)
    node = link(Node)
    posted = attr(DateTime, default="now")
    content = attr(str)

Node.parent.type = Node
Node.children.type = Node
Node.comments.type = Comment
    

class PlanApp(sixthday.AdminApp):

    def viewListProject(self):
        projs = self.clerk.match(Node, ntype="project")
        return {'projects': [BoxView(p) for p in projs] }

    def formEditNode(self):
        model = {}
        
        parentID = self.input.get("parent", "0")
        if int(parentID):
            parent = self.clerk.fetch(Node, ID=parentID)
        else:
            parent = Node(ID=0)
            parent.private.isDirty = False
        self.input["parent"] = parent
            
        node = self._getInstance(Node)
        if node.parent is None:
            node.parent = Node()
        model.update(BoxView(node))
        nodes = [(n.ID, n.path) for n in self.clerk.match(Node)
                 if n.ntype != "task"]
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
        model["comments"] = [BoxView(c) for c in node.comments]
        model["comments"].sort(lambda a,b: -cmp(a["posted"], b["posted"]))
        return model
    
    def viewPlate(self):
        nodes = self.clerk.match(Node, isOnPlate=True)
        nodes.sort(lambda a,b: cmp(a.importance, b.importance))
        return {"nodes": [BoxView(n) for n in nodes]} # @TODO: =~ listProject

    def postComment(self):
        self.input["ID"] = self.input.get("node")
        assert self.input["ID"], "give me a node"
        n = self._getInstance(Node)
        n.comments << Comment(content=self.input.get("content"))
        self.clerk.store(n)
        self.redirect("?action=viewNode&ID=%s" % n.ID)

