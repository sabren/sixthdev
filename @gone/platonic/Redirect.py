
#@TODO: Redirect should subclass object, not Exception
#I'd change it now but it's still being thrown in various places
class Redirect(Exception):
    # for assertions in unit tests:
    isModel, isRedirect = False, True
    def __init__(self, where):
         self.where = where
