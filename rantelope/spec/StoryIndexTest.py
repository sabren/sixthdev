
__ver__="$Id$"

import unittest
from rantelope import Story, StoryIndex
from arlo import MockClerk

class StoryIndexTest(unittest.TestCase):
    
    def test_basics(self):
        #@TODO: MockClerk shouldn't need a dbmap!!
        c = MockClerk(dbmap=
                      {Story.__attrs__["comments"]: ("SADF", "storyID"),
                       Story.__attrs__["author"]: ("asdf","sadf")})

        idx = StoryIndex(c, "spec/indextest.rk")


        s1 = c.store(Story(title="onedog", description="a big dog"))
        s2 = c.store(Story(title="twodog", description="dog eat dog"))
        s3 = c.store(Story(title="onecat", description="a fat cat"))

        idx.addStory(s1)
        idx.addStory(s2)
        idx.addStory(s3)

        dogs = idx.match("dog")
        cats = idx.match("cat")
        assert len(dogs)==2, dogs        
        assert len(cats)==1, cats
        
        # and check scoring:
        assert dogs[0].title=="twodog"
        assert dogs[1].title=="onedog"

        blank = c.store(Story(title="", description=""))
        idx.addStory(blank)
