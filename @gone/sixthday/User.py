import zdc
import handy

class User(zdc.RecordObject):
    _tablename = "base_user"
    
    def _new(self):
        super(User, self)._new()
        self.uid = handy.uid()

