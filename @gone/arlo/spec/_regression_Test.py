import unittest
from strongbox import *
from arlo import Clerk
from storage import MockStorage

class _regression_Test(unittest.TestCase):

    def test_complex_recursion(self):
        """
        test case from cornerhost that exposed a bug.
        this is probably redundant given test_recursion
        but it doesn't hurt to keep it around. :)

        This test is complicated. Basically it sets up
        several classes that refer to each other in a loop
        and makes sure it's possible to save them without
        infinite recursion.
        
        @TODO: isInstance(LinkSetInjector) in Clerk.py need tests
        It ought to do some kind of polymorphism magic anyway.
        (huh??)
        """

        class User(Strongbox):
            ID = attr(long)
            username = attr(str)
            domains = linkset(forward,None)
            sites = linkset(forward,None)
        class Domain(Strongbox):
            ID = attr(long)
            user = link(User)
            name = attr(str)
            site = link(forward)            
        class Site(Strongbox):
            ID = attr(long)
            user = link(User)
            domain = link(Domain)
        User.domains.type = Domain
        User.sites.type = Site
        Domain.__attrs__["site"].type = Site
        dbMap = {
            User:"user",
            User.domains: (Domain, "userID"),
            User.sites: (Site, "userID"),
            Domain:"domain",
            Domain.user: (User, "userID"),
            Domain.site: (Site, "siteID"),
            Site:"site",
            Site.user: (User, "userID"),
            Site.domain: (Domain, "domainID"),
            } 
       
        clerk = Clerk(MockStorage(), dbMap)
        u = clerk.store(User(username="ftempy"))
        u = clerk.match(User,username="ftempy")[0]
        d = clerk.store(Domain(name="ftempy.com", user=u))
        assert d.user, "didn't follow link before fetch"
        d = clerk.match(Domain, name="ftempy.com")[0]

        # the bug was here: it only happened if User had .domains
        # I think because it was a linkset, and the linkset had
        # an injector. Fixed by breaking the test for
        # hasInjectors out of an "and" and into the body of the
        # if block, in Clerk.store()
        assert d.user, "didn't follow link after fetch"
        assert d.user.ID == u.ID

        # ah, but then we had an infinite recursion problem
        # with site, but I fixed that with private.isDirty:
        d.site = clerk.store(Site(domain=d))
        d = clerk.store(d)
        assert d.site.domain.name == "ftempy.com"

        # and again here:
        d = clerk.fetch(Domain, 1)
        assert not d.private.isDirty
        assert not d.site.private.isDirty # this failed.
        clerk.store(d)                    # so this would recurse forever
