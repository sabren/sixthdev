
import zikebase
import zdc

class Content(zdc.RecordObject):
    __super = zdc.RecordObject
    _tablename = "base_content"

    def _new(self):
        self.__super._new(self)
        self.userID = 0
