#**** Solution 

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

class Solution(object):
    def __init__(self):
        self.parts = []

    def append(self, x):
        self.parts.append(x)


    def __iter__(self):
        return self.parts.__iter__()


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


def _Solution___getitem__(self, key):    
    return self.getBlazes()[key]
Solution.__getitem__ = _Solution___getitem__

#**** would like cleaner way to revisit a point
#***** we have trail[x][y][z] but this is ugly
#***** so, solution.find(trail="x.y.z")

class AtTest(unittest.TestCase):
    def test(self):
        words = Solution()
        alphabet = "_abcdefghijklmnopqrstuvwxyz"
        
        # this is a somewhat big solution space
        # 26 x 26 = 676 blazes [25 letters + _]
        for x in alphabet:
            words.blaze(x)
            for y in alphabet:
                words.at(x).blaze(y)

        # add some words to the tree:
        words.at("t.w").append("twas")
        words.at("a._").append("a")
        words.at("d.a").append("dark")
        words.at("a.n").append("and")
        words.at("s.t").append("stormy")
        words.at("n.i").append("night")

        # they should be alphabetized now:
        self.assertEquals("a and dark night stormy twas",
                           " ".join(words))

       
# here's how we did it:

def _Solution_at(self, trail):
    split = trail.split(self.splitter, 1)
    head, tail = split[0], split[1:]
    assert len(tail) in [0,1] # because of 1 in trail.split()
    if tail:
        return self[head].at(tail[0])
    else:
        return self[head]
    
Solution.at = _Solution_at

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
        s.at("content").append("before")
        s.append("]")

        self.assertEquals("[before]", "".join(s))
        s.clear("content")
        self.assertEquals("[]", "".join(s))
        s.at("content").append("after")
        self.assertEquals("[after]", "".join(s))


def _Solution_clear(self, trail=None):
    if trail:
        self.at(trail).clear()
    else:
        self.parts = []
        self.blazes = {}
Solution.clear = _Solution_clear

