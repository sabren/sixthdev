
from gameworld import event, Observable

class Avatar(Observable):
    """
    I'm something that can move around in a Game.
    """
        
    def walk(self, direction):
        try:
            self.notify(self, event.WalkAction(direction))
        except event.Blocked:
            self.onBlocked()

    def onBlocked(self):
        pass
    
