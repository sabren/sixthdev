
from planaconda import Node, Comment

DBMAP = {
    Node: "plan_node",
    Node.__attrs__["parent"]: (Node, "parentID"),
    Node.__attrs__["children"]: (Node, "parentID"),
    Node.__attrs__["comments"]: (Comment, "nodeID"),
    Comment.__attrs__["node"]: (Node, "nodeID"),    
    }
