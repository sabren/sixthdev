
import zikebase
import zdc

class Content(zdc.RecordObject):
    _table = zdc.Table(zikebase.dbc, "base_content")
    _defaults = {"userID": 0}   
