from exceptions import Exception
class Denial(Exception):
    def __init__(self, reason):
         self.reason=reason
