
from strongbox import *
import sixthday

class Node(sixthday.Node):
    ntype = attr(str, okay=["project","goal","task"], default="task")
    

class PlanApp(sixthday.AdminApp):

    def viewListProject(self):
        projs = self.clerk.match(Node, ntype="project")
        return {'projects': [BoxView(p) for p in projs] }

    def formEditNode(self):
        return BoxView(Node())


