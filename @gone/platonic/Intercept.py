from exceptions import Exception
class Intercept(Exception):
    def __init__(self, where):
         self.where = where
         
    
    
