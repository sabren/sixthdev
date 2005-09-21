import unittest

#*** the solution compiler should be easy:
# just "for x in solution" or list(solution)

class SolutionTest(unittest.TestCase):
    def test(self):
        # is like a list but you can only append
        s = Solution()
        assert list(s) == []
        s.append("a")
        assert list(s) == ["a"]
        s.append("b")
        s.append("c")
        assert list(s) == ["a","b","c"]
        assert str(s) == "abc"

class Solution(object):
    def __init__(self):
        self.parts = []

    def append(self, x):
        self.parts.append(x)

    def __iter__(self):
        return self.parts.__iter__()

    def __str__(self):
        return "".join(self)


#*** want to give big picture and fill details in later
#*** explain what trailblazing is
#**** blaze(name)
#***** maps name to a position on the list

class BlazeTest(unittest.TestCase):
    def setUp(self):
        s = Solution()
        s.blaze("start")
        s.append("[")
        s.append("{")
        s.blaze("middle")
        s.append("}")
        s.append("]")
        s.blaze("end")
        self.solution = s
        
    def test(self):
        self.assertEquals("[{}]", "".join(self.solution))
        

#*****  just map the name to a placeholder

def _Solution_getBlazes(self):
    if not hasattr(self, "blazes"):
        self.blazes = {}
    return self.blazes
    
def _Solution_blaze(self, name):
    place = self.placeHolder()
    self.getBlazes()[name] = place
    self.append(place)

# tack it on to the original class:
Solution.getBlazes = _Solution_getBlazes
Solution.blaze = _Solution_blaze

#***** reason for placeholder is that
#***** could just insert to the list but then it screws up our keys
#***** so: placeholder() -> Solution()

def _Solution_placeHolder(self):
    return Solution()
Solution.placeHolder = _Solution_placeHolder

#**** we don't actualy want to see those placeholders
#**** plus lose ability to iterate when we went nested
#**** but easy to fix: __iter__

def _Solution___iter__(self):
    for item in self.parts:
        if isinstance(item, Solution):
            for child in item:
                yield child
        else:
            yield item
Solution.__iter__ = _Solution___iter__

#*** want to extend without screwing up the blazes

class BlazeExtensionTest(BlazeTest):
    def test(self):
        self.assertEquals("[{}]", "".join(self.solution))
        self.solution["start"].append("<")
        self.solution["middle"].append("*")
        self.solution["middle"].append("-")
        self.solution["middle"].append("*")
        self.solution["end"].append(">")
        self.assertEquals("<[{*-*}]>", "".join(self.solution))

"""
Now, we could just return the key from the getBlaze()[key]
but that doesn't allow us to follow a trail. Consider:
"""

class AtTest(unittest.TestCase):
    def test(self):
        words = Solution()
        alphabet = "_abcdefghijklmnopqrstuvwxyz"
        
        # this is a somewhat big solution space
        # 26 x 26 = 676 blazes [25 letters + _]
        for x in alphabet:
            words.blaze(x)
            for y in alphabet:
                words[x].blaze(y)

        # add some words to the tree:
        words["t.w"].append("twas")
        words["a._"].append("a")
        words["d.a"].append("dark")
        words["a.n"].append("and")
        words["s.t"].append("stormy")
        words["n.i"].append("night")

        # they should be alphabetized now:
        self.assertEquals("a and dark night stormy twas",
                           " ".join(words))

       
# so here's how we do that:

def _Solution___getitem__(self, trail):
    split = trail.split(self.splitter, 1)
    head, tail = split[0], split[1:]
    assert len(tail) in [0,1] # because of 1 in trail.split()
    if tail:
        return self.getBlazes()[head][tail[0]]
    else:
        return self.getBlazes()[head]
    
Solution.__getitem__ = _Solution___getitem__

#***** make split char configurable (but classwide)
Solution.splitter = "."



#**** how to extend the point?
#***** this already works
#**** how to replace the point?
#**** just clear and append again

class ClearTest(unittest.TestCase):
    def test(self):
        s = Solution()
        s.append("[")
        s.blaze("content")
        s["content"].append("before")
        s.append("]")

        self.assertEquals("[before]", "".join(s))
        s.clear("content")
        self.assertEquals("[]", "".join(s))
        s["content"].append("after")
        self.assertEquals("[after]", "".join(s))


def _Solution_clear(self, trail=None):
    if trail:
        self[trail].clear()
    else:
        self.parts = []
        self.blazes = {}
Solution.clear = _Solution_clear



# finally, we wan to be able to merge two solutions together
# a list uses the extend method for this,

class ExtendTest(unittest.TestCase):
    def test(self):
         a = Solution()
         a.blaze("a")
         a["a"].append("a")

         b = Solution()
         b.blaze("b")
         b["b"].append("b")

         a.extend(b)
         self.assertEquals("b", str(a["b"]))


# but because of the nested structures and names, we need to a little
# more work:
def _Solution_extend(self, other):
    self.parts.extend(other.parts)
    for k, v in other.getBlazes().items():
        self.getBlazes()[k] = v
Solution.extend = _Solution_extend


"""
run the tests:
"""
if __name__=="__main__":
    unittest.main()
