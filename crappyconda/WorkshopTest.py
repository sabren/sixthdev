
from strongbox import *
import workshop
import unittest

class WorkshopTest(unittest.TestCase):

    def setUp(self):

        other = workshop.ProtoClass(name="Other")
        thing = workshop.ProtoClass(name="Thing")
        thing.attrs << workshop.ProtoAttr(name="at", type="str")
        thing.links << workshop.ProtoLink(name="ln", type=other)
        thing.joins << workshop.ProtoJoin(name="jn", type=other)

        self.thing = thing
        self.other = other

        self.model = workshop.Model()
        self.model.add(other)
        self.model.add(thing)

    def test_class(self):

        code = self.model.asCode()
        print code
        
        exec code
        assert Other is not None
        assert Thing is not None
        
        t = Thing()
        assert hasattr(t, "at")        
        assert hasattr(t, "ln")
        assert hasattr(t, "jn")        


    def test_dbmap(self):

        m = workshop.ProtoMap()
        m.ccells << workshop.ClassCell(
            what=self.thing,
            tablename="test_thing")
        m.lcells << workshop.LinkCell(
            what=self.thing.links[0],
            tablename="test_link",
            fieldname="linkID")

        exec self.model.asCode()
        dbmap = eval(m.asCode())
        assert dbmap[Thing] == "test_thing"
        

if __name__=="__main__":
    unittest.main()
    
