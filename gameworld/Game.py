
from gameworld import Observable, Map, event

class Game(Observable):

    def __init__(self, map=None):
        super(Game, self).__init__()
        self.map = map or Map()

    def place(self, subject, location):
        self.map.place(subject, location)
        subject.register(self.on_notify)

    def spawn(self, subject, location):
        self.place(subject, location)
        self.notify(subject, event.Spawned)

    def locate(self, subject):
        return self.map.locate(subject)

    def on_notify(self, subject, e):
        if isinstance(e, event.WalkAction):
            self.nudge(subject, e.direction)

    def nudge(self, subject, direction):
        here  = self.map.whereis[subject]
        there = self.map.findAdjacent(direction, here)
        if self.map.isOccupied(there):
            raise event.Blocked()
        else:
            self.map.move(subject, there)
        self.notify(subject, event.Moved)
    
