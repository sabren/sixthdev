import handy
from strongbox import Strongbox, attr

class User(Strongbox):

    ID = attr(long, default=None)
    uid = attr(str)
    username = attr(str)
    email = attr(str)
    password = attr(str)
    
    def __init__(self, **init):
        super(User, self).__init__(**init)
        if not self.uid: self.uid = handy.uid()
