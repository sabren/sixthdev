
__ver__="$Id$"

import unittest
from rantelope import AuthorAuth, Author
from arlo import MockClerk
from weblib import Sess, SessPool, Request, Response

class AuthorAuthTest(unittest.TestCase):
    
    def test_login(self):

        clerk = MockClerk()
        clerk.store(Author(username='fred', password='wanda'))
        sess = Sess(SessPool.InMemorySessPool(),Request(),Response())
        aa = AuthorAuth(sess, clerk)
        
        assert aa.fetch(1).username == 'fred'
        aa.login(1)
        assert aa.user.username == 'fred'

        assert aa.validate({"username":"fred", "password":"wanda"})
        assert not aa.validate({"username":"fake", "password":"spam"})
        
