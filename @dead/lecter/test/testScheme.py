"""
unit tests for lecter's scheme functions..
These roughly follow the concepts in the book, The Little Schemer
"""
__ver__="$Id$"

import unittest
from lecter import scheme
from scheme import f

class SchemeTestCase(unittest.TestCase):

    ## CHAPTER ONE ########################

    def check_atomP(self):
        """
        atom? should be true for atoms, false otherwise
        """
        assert scheme.atomP("hello"), "hello should be an atom"
        assert not scheme.atomP(["hello"]), "(hello) is not an atom"

    def check_listP(self):
        """
        list? should be true for lists, false otherwise
        """
        assert not scheme.listP("hello"), "hello is not a list"
        assert scheme.listP(["hello"]),   "(hello) is a list"
        assert scheme.listP([]),          "() is a list"

    def check_head(self):
        """
        (head) is lecter's (car)... It gets the first list member.
        """
        assert scheme.head(["a","b","c"])=="a", "(head '(a b c)) should be a"
        try:
            gotError=0
            scheme.head([])
        except:
            gotError=1
        assert gotError, "(head ()) should give error"
        

    def check_tail(self):
        """
        (tail) is lecter's (cdr).. It gets the rest of the list.
        """
        assert scheme.tail(["a","b","c"]) == ["b","c"], \
               "(tail '(a b c)) should be (b c)"
        assert scheme.tail([]) is None
        
    def check_cons(self):
        """
        (cons) appends something to the front of a list
        """
        assert scheme.cons("a", ["b","c"]) == ["a","b","c"], \
               "(cons a '(b, c)) should be a (a b c)"

    def check_nullP(self):
        """
        (null? x) tests for ()
        """
        assert scheme.nullP([]), "() should be null!"
        assert not scheme.nullP(["a"]), "(a) should not be null!"

    
    def check_eq(self):
        """
        (eq? a b) compares two atoms... [but we'll say two of anything]
        """
        assert scheme.eqP("a","a"), "(a) and (a) should be equal!"


    ## CHAPTER TWO ##########################

    def check_define(self):
        pass

        
    ## CHAPTER THREE ########################

