from narrative import testcase
import unittest


class Solution(object):

    # make split char configurable (but classwide)
    splitter = "."

    def __init__(self):
        self.parts = []
        self.visible = True
        self.blazes = {}

    #def __iter__(self):
    #    return self.parts.__iter__()

    def __iter__(self):
        for item in self.parts:
            if isinstance(item, Solution):
                for child in item:
                    yield child
            else:
                yield item

    def __getitem__(self, trail):
        split = trail.split(self.splitter, 1)
        head, tail = split[0], split[1:]
        assert len(tail) in [0,1] # because of 1 in trail.split()
        if tail:
            return self.getBlazes()[head][tail[0]]
        else:
            return self.getBlazes()[head]

    def __str__(self):
        return "".join(self)

    def append(self, x):
        self.parts.append(x)

    def blaze(self, name):
        return self.addChild(name, self.placeHolder())

    def addChild(self, name, child):
        self.getBlazes()[name] = child
        self.append(child)
        return child
        

    def clear(self, trail=None):
        if trail:
            self[trail].clear()
        else:
            self.parts = []
            self.blazes = {}

    def extend(self, other):
        self.parts.extend(other.parts)
        for k, v in other.getBlazes().items():
            self.getBlazes()[k] = v

    def getBlazes(self):
        return self.blazes

    def hide(self):
        self.visible = False

    def hideAll(self):
        self.hide()
        for kid in self.blazes.values():
            kid.hideAll()

    def placeHolder(self):
        return Solution()

    def show(self):
        self.visible = True

    def snapShot(self):
        if self.visible:
            return "".join(list(self.visibleParts()))
        else:
            return ""

    def visibleParts(self):
        for item in self.parts:
            if isinstance(item, Solution):
                yield item.snapShot()
            else:
                yield item




############################################


#*** the solution compiler should be easy:
# just "for x in solution" or list(solution)
@testcase
def testSolution(self):
    # is like a list but you can only append
    s = Solution()
    assert list(s) == []
    s.append("a")
    assert list(s) == ["a"]
    s.append("b")
    s.append("c")
    assert list(s) == ["a","b","c"]
    assert str(s) == "abc"
        


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

class BlazesShouldBeSolutions(BlazeTest):
    def test(self):
        """
        blaze should return the placeholder so that
        linehound can maintain a stack as it goes along
        """
        assert isinstance(self.solution.blaze('bleh'),Solution)

#*****  just map the name to a placeholder

#***** reason for placeholder is that
#***** could just insert to the list but then it screws up our keys
#***** so: placeholder() -> Solution()

#**** we don't actualy want to see those placeholders
#**** plus lose ability to iterate when we went nested
#**** but easy to fix: __iter__

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

# * hiding nodes
"""
While working on brickslayer, I realized it might make
more sense to have all the source code in the actual
files, and simply mark out chunks to be included in the
narrative. This is akin to an HTML page where some of the
elements are hidden by default.

Besides clearing up quite a bit of headache when it comes
to explaining where code should go, and making it easier to
see the entire solution with all variations at once, this
makes it possible to add a trail on top of an existing codebase.
"""

@testcase
def testSnapshot(self):

    s = Solution()
    s.append("<")
    
    a = s.blaze("a")
    a.append("[")

    b = a.blaze("b")
    b.append("{")
    b.append("}")

    a.append("]")
    s.append(">")

    self.assertEquals("<[{}]>", "".join(s))
    self.assertEquals("<[{}]>", s.snapShot())
    s["a.b"].hide()
    self.assertEquals("<[]>", s.snapShot())
    s["a"].hide()
    self.assertEquals("<>", s.snapShot())
    s["a.b"].show()
    self.assertEquals("<>", s.snapShot())


"""
run the tests:
"""
if __name__=="__main__":
    unittest.main()
