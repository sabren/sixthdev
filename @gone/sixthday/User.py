import zdc
import handy
from strongbox import attr

class User(zdc.RecordObject):
    _tablename = "base_user"
    ID = attr(long)
    uid = attr(str)
    username = attr(str)
    email = attr(str)
    password = attr(str)
    
    def _new(self):
        super(User, self)._new()
        self.uid = handy.uid()

