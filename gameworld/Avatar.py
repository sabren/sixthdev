
from gameworld import Blocked

class Avatar(object):
    """
    I help move things around on Maps.
    """
    def __init__(self, map, location, facing=None):
        self.map = map
        self.location = location
        self.facing = facing or map.SOUTH
        self.map.place(self, location)

    def move(self, direction):
        goal = self.map.findAdjacent(direction, self.location)
        if self.map.isOccupied(goal):
            raise Blocked
        else:
            self.map.remove(self)
            self.location = goal
            self.map.place(self, goal)

    def face(self, direction):
        self.facing = direction
        
