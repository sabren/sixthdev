
class Map(object):

    NORTH = ( 0, -1)
    SOUTH = ( 0, +1)
    EAST  = (-1,  0)
    WEST  = (+1,  0)

    def __init__(self):
        self.whatsat = {}
        self.whereis = {}

    def findAdjacent(self, direction, location):
        return (location[0] + direction[0],
                location[1] + direction[1])

    def locate(self, thing):
        return self.whereis.get(thing)

    def place(self, thing, location):
        self.whatsat.setdefault(location, [])
        self.whatsat[location].append(thing)
        self.whereis[thing] = location

    def remove(self, thing):
        location = self.whereis[thing]
        del self.whereis[thing]
        self.whatsat[location].remove(thing)

    def isOccupied(self, location):
        return bool(self.whatsat.get(location))

    
