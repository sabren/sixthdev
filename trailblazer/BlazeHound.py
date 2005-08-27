
# This is BlazeHound, our XML-based solution compiler.

# Here's what we're shooting for: We should be able
# to put a bunch of ideas in the same file and have it
# all mixed up, and modify things as we go along so
# that we're able to explain things in nice little
# pieces... But then in the end we want the computer
# to be able to go back and compile all the trails into
# the full solution
_TEST_NARRATIVE =\
"""\
<xml>
  <trail:blaze trail="char">
    <trail:blaze trail="alpha">XYZ</trail:blaze>
    <trail:blaze trail="number">123</trail:blaze>
  </trail:blaze>
  <trail:replace trail="char.alpha">ABC</trail:replace>
  <trail:extend trail="char.number">456</trail:extend>
  <trail:extend trail="char.alpha">DEF</trail:extend>
</xml>\
"""
_TEST_SOLUTION_CHAR ="ABCDEF123456"
_TEST_SOLUTION_ALPHA ="ABCDEF"
_TEST_SOLUTION_NUMBER ="123456"


# It's pretty straightforward. We're just going
# to parse the XML file and add all the chunks
# to a solution. So in terms of our technology,
# we want to create a Saxophone with some TagHandlers
# that build a Solution object from the xml tags.
from Solution import Solution
from altosax import Saxophone, TagHandler, DOCUMENT

# Since state machines are kind of tricky, we can
# use the logging module to help us see what's
# happening. 
import logging

# To see the output, just uncomment this next line:
#logging.root.setLevel(logging.DEBUG)


# Just to be clear we have three tags. We're
# going to skirt around the whole issue of xml
# namespaces here, because by default, xml.sax
# just ignores the colon and returns the whole
# qname. This means "trail:" isn't a real
# namespace. This should probably be fixed later.

#@TODO: clean up namespace handling
TAG_BLAZE = "trail:blaze"
TAG_REPLACE = "trail:replace"
TAG_EXTEND = "trail:extend"

# Now the basic TagHandler almost does what we want,
# but not quite. Why? Because it's appending to a
# list as we go along, but what we really want to
# do is append to a Solution.

# ah, but which solution? if all we had were blaze
# tags, then we could just make up a new solution
# at the start of each tag and build up the tree
# using anonymous instances.

# but, since we want to be able to modify the tree
# as we go (using the replace and extend tags)
# then we need to be able to walk the tree. which
# means we need to hold on to the root.

# it also means that we can't have a separate
# solution for each tag.

# if we want nested blaze tags, then we need the
# concept of a "current" solution as well as the
# "root" solution. so we need exactly one root
# Solution, plus one Solution per trail: tag.

# But that's all easy os far as SolutionBuilder
# is concerned. just replace the .data attribute
# with a Solution, either a specific one that
# we pass in, or a brand new one:

class SolutionBuilder(TagHandler):
    def __init__(self, tag, attrs, solution):
        super(SolutionBuilder, self).__init__(tag, attrs)
        self.data = solution

# by default, all tags and data (for example, html content)
# will go to this generic tog. 

# But, we have three tags we need to handle specially:
# blaze, extend, and replace. We could implement each one as
# a TagHandler and pass the same Solution object around
# but since Solution is a recursive data structure anyway,
# it's easier to just use SolutionBuilder.

# What I'm proposing here is that each tag gets its
# own Solution object, and as we close the tags, we
# just append those Solutions to the parent solution.

# This implies that you can nest the "blaze" tags
# (because creating a new solution is always okay)
# but you nesting the extend or replace tags is
# tricky because a child tag has no access to the
# parent tag's data. All we can do is tell the parent
# that this is an "extend" or "replace" action once
# the tag gets closed, and here's all the new data
# we collected. In other words, all the magic happens
# in the SolutionBuilder.child handler:

    def child(self, child):
        if child.tag == TAG_BLAZE:
            self.onBlaze(child)
        elif child is not None:
            # not a trail tag so we can just collapse the
            # solution into a string:
            self.data.append(str(child))

############################################################
#@TODO: TagHandler should do dispatch
############################################################
#
# I REALLY don't like that.
#
# The whole point of saxophone was that I wouldn't have to
# write my own dispatch routine like that. It was supposed
# to happen through composition and a generic dispatch and
# callback mechanism. What went wrong?
#
# Well, right now the dispatch happens when the tag STARTS,
# and it's all controlled centrally in the Saxophone. What
# I want here is to handle different types of tags when
# they CLOSE. So I missed the boat a little bit. I THINK
# I'd like to keep the on-open stuff for zebra/reptile,
# but I'll have to think about it. In other words, I've
# either got it backwards or I could need either, depending
# on the situation. But whatever. I'll try again with
# a different design some other time. The above dispatch
# will work just fine for now.
#
############################################################            

# Anyway, the mini tag handler-like methods are easy
# enough. Here's the Blaze handler:

    def onBlaze(self, child):
        trail=child.attrs["trail"]
        self.data.blaze(trail)
        self.data.at(trail).extend(child.data)

    def child(self, data):
        ## self.data.append(data)
        pass

# so really this should all work for our test but
# not yet for dotted paths. I'll have to rethink
# this. But let's go ahead and implement the test:
import unittest 
class BlazeHoundTest(unittest.TestCase):
    def test(self):
        sxp = BlazeHound()
        sol = sxp.parseString(_TEST_NARRATIVE).data
        logging.debug(sol.getBlazes())
        logging.debug(list(sol))
        print sxp.getSolution()
        self.assertEquals(str(sol["chars.alpha"]), _TEST_SOLUTION_ALPHA)
        self.assertEquals(str(sol["chars.number"]), _TEST_SOLUTION_NUMBER)      





###############################################################

class BlazeHoundTag(SolutionBuilder):
    def __init__(self, hound, tag, attrs):
        solution = Solution()
        super(BlazeHoundTag, self).__init__(tag, attrs, solution)
        self.hound = hound
        self.hound.pushContext(solution)
        self.trail = attrs["trail"]


class ExtendTag(BlazeHoundTag):
    def close(self):
        self.hound.popContext()
        self.hound.getSolution().at(self.trail).extend(self.data)
        return None
    
class ReplaceTag(BlazeHoundTag):
    def close(self):
        self.hound.popContext()
        print self.hound.getSolution()
        self.hound.getSolution().at(self.trail).clear()
        self.hound.getSolution().at(self.trail).extend(self.data)
        return None

class BlazeHound(Saxophone):

    def __init__(self, sol=None):
        # by default, use self.onAny, below
        super(BlazeHound, self).__init__(self.onAny)

        # the other tags are easy:
        self.onTag(TAG_EXTEND,
                   lambda tag, attrs: ExtendTag(self, tag, attrs))
        self.onTag(TAG_REPLACE,
                   lambda tag, attrs: ReplaceTag(self, tag, attrs))


# now, we need to be able to get to our solution as we go along
# this means we can't wait for the top level tag to close in order
# to get at it. so... we need to create the root solution
# ourselves and hold on to it.

        self.rootSolution = sol or Solution()
        self.contexts = [self.rootSolution] # solution stack

# Saxophone.byDefault needs to be a callable that returns
# a TagHandler. There's no reason it con't just be a method:

    def onAny(self, tag, attrs):
        return SolutionBuilder(tag, attrs, self.getContext())

    def getSolution(self):
        return self.rootSolution


    def getContext(self):
        return self.contexts[-1]

    def pushContext(self, solution):
        self.contexts.append(solution)

    def popContext(self):
        return self.contexts.pop()

# run the tests
if __name__=="__main__":
    unittest.main()
    
