
from planaconda import Node

DBMAP = {
    Node: "plan_node",
    Node.__attrs__["parent"]: (Node, "parentID"),
    Node.__attrs__["children"]: (Node, "parentID"),
    }
