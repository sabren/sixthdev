
from strongbox import Strongbox, link
from unittest import TestCase

class LinkedListMember(Strongbox):
    next = link("LinkedListMember")

class NonMember(Strongbox):
    pass

class NotEvenAStrongbox:
    pass

class LinkTest(TestCase):

    def check_typing(self):
        one = LinkedListMember()
        two = LinkedListMember()
        bad = NonMember()

        one.next = two
        two.next = one
        assert one.next.next is one

        failed = 0
        for item in (bad, NotEvenAStrongbox(), "wrong type"):
            try:
                one.next = item
            except TypeError:
                failed += 1
        assert failed == 3, "Link should force types"

        two = LinkedListMember()
        one = LinkedListMember(next=two)
        assert one.next is two
        assert two.next is None
