
from strongbox import *
from storage import MockStorage
from arlo import CallbackClerk, Schema
import unittest


class Thing(Strongbox):
    ID = attr(long)
    x = attr(str)

class OtherThing(Strongbox):
    ID = attr(long)
    x = attr(str)

class CallbackClerkTest(unittest.TestCase):

    def test_onStore(self):
        queue = []
        schema = Schema({
            Thing: "thing",
            OtherThing: "other",
        })
            
        clerk = CallbackClerk(MockStorage(), schema)
        clerk.onStore(Thing, queue.append)
        
        clerk.store(Thing(x="a"))
        clerk.store(Thing(x="b"))
        clerk.store(OtherThing(x="not me"))


        queue2 = []
        clerk.onStore(Thing, queue2.append)
        clerk.store(Thing(x="c"))

        # "c" should wind up in both:
        assert len(queue) == 3
        assert "".join([t.x for t in queue]) == "abc"

        assert len(queue2) == 1
        assert queue2[0].x=="c"

if __name__=="__main__":
    unittest.main()
    
