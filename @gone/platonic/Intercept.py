from exceptions import Exception
class Intercept(Exception):
    def __init__(self, where, **kwargs):
         self.where = where
         self.data = kwargs
    
    
