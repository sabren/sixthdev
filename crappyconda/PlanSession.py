
from planaconda import *

class PlanSession:
    def __init__(self, clerk):
        self.clerk = clerk

    def list_goal(self):
        return self.clerk.match(Goal)
    
