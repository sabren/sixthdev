import unittest
from strongbox import *
from arlo import Clerk, Schema
from storage import MockStorage

class _regression_Test(unittest.TestCase):

    def test_disappearing_events(self):
        """
        This bug came from duckbill. A subscription
        would post events to its account, and then
        when it showed the statements the new events
        would be the only ones to show up - even though
        there were still others in the database.

        In other words, the injector wasn't working.

        Turns out the problem was that the sub.account
        stub didn't have injectors on ITS dependent
        objects. That's why I now replace .private
        in LinkInjector.inject()
        """
        class Evt(Strongbox):
            ID = attr(long)
            evt = attr(str)
            acc = link(forward)
        class Sub(Strongbox):
            ID = attr(long)
            acc = link(forward)
        class Acc(Strongbox):
            ID = attr(long)
            subs = linkset(Sub, "acc")
            evts = linkset(Evt, "acc")
        Evt.acc.type = Acc
        Sub.acc.type = Acc
        schema = Schema({
            Evt:"evt",
            Sub:"sub",
            Acc:"acc",
            Evt.acc: "accID",
            Sub.acc: "accID",
        })
        st = MockStorage()
        c1 = Clerk(st, schema)

        # store an account with two events and one sub:
        a = Acc()
        a.evts << Evt(evt="1")
        a.evts << Evt(evt="2")
        assert a.private.isDirty
        a.subs << Sub()
        c1.DEBUG = 1
        c1.store(a)

        # new clerk, new cache:
        c2 = Clerk(st, schema)

        # add more events while s.acc is a stub
        s = c2.fetch(Sub, ID=1)
        assert not s.private.isDirty
        #@TODO: maybe len() should trigger the lazyload...
        assert len(s.acc.evts) == 0, [e.evt for e in s.acc.evts]
        s.acc.evts << Evt(evt="3")
        #assert len(s.acc.evts) == 1, [e.evt for e in s.acc.evts]
        assert len(s.acc.evts) == 3, [e.evt for e in s.acc.evts]
        c2.DEBUG = 0
        c2.store(s)
        a2 = c2.fetch(Acc, ID=a.ID)

        assert a is not a2

        # we should now have all three events,
        # but we were getting only the third one:
        assert len(a2.evts) == 3, [e.evt for e in a2.evts]
    

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
            domains = linkset(forward,"user")
            sites = linkset(forward,"user")
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
        Domain.site.type = Site
        dbMap = Schema({
            User:"user",
            Domain:"domain",
            Domain.user: "userID",
            Domain.site: "siteID",
            Site:"site",
            Site.user: "userID",
            Site.domain: "domainID",
        })
       
        clerk = Clerk(MockStorage(), dbMap)
        u = clerk.store(User(username="ftempy"))
        u = clerk.match(User,username="ftempy")[0]
        d = clerk.store(Domain(name="ftempy.com", user=u))
        assert d.user, "didn't follow link before fetch"
        d = clerk.match(Domain, name="ftempy.com")[0]

        # the bug was here: it only happened if User had .domains
        # I think because it was a linkset, and the linkset had
        # an injector. Fixed by inlining the injector test into
        # Clekr.store:
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
