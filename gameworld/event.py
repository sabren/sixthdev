
class Spawned: pass
class Blocked: pass
class Moved: pass

class WalkAction:
    def __init__(self, direction):
        self.direction = direction
