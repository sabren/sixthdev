from gameworld import Avatar, Map
from __future__ import generators

class Actor(Avatar):
    """
    I'm an avatar that moves on my own
    (if you call my .cue() method in an event loop)
    """
    def __init__(self, script):
        super(Actor, self).__init__()
        self.performance = self.__rehearse(script)

    def cue(self):
        self.performance.next()

    def __rehearse(self, script):
        """
        act out the script in tiny steps (generator)
        """
        directions = {
            "n": Map.NORTH,
            "s": Map.SOUTH,
            "e": Map.EAST,
            "w": Map.WEST,
            }
        while 1:
            for ch in script:
                if ch in directions:
                    self.walk(directions[ch])
                yield None
