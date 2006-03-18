#!/usr/bin/env python2.4
# ledger.py
import re
import unittest
import datetime
from handy import trim
from decimal import Decimal
from strongbox import Strongbox, attr

# * Comments

class Comment:
    def __init__(self):
        self.lines = []
        
    def addCommentLine(self, line):
        self.lines.append(line)

# * Transactions and Items
"""
A basic transaction contains line items with
credits and debits. The line items must add up to 0.
"""
class TransactionTest(unittest.TestCase):
    def test(self):
        t = Transaction(
            posted =  "2005/01/01",
            party = "fred flintstone",
            memo = "owed him money",
            cleared = "2005/05/02",
            isReconciled = False,
            items = [])
        t.addItem("liability:fred", "10.00"),
        self.assertRaises(ValueError, t.validate)
        t.addItem("asset:checking", "-10.00"),
        t.validate() # should work now.

class Item(Strongbox):
    account = attr(str)
    amount = attr(Decimal)
        

class Transaction:
    def __init__(self, posted, party, memo=None,
                 cleared=None, isReconciled=False,
                 items = []):
        self.posted = posted
        self.party = party
        self.memo = memo
        self.cleared = cleared
        self.isReconciled = isReconciled
        self.items = items
        self.validate()
        self.comment = Comment()

    def addItem(self, account, amount_in):
        amount = amount_in
        if amount is None:
            amount = -self.total()
        self.items.append(Item(account=account,
                               amount=Decimal(amount)))

    def addCommentLine(self, line):
        self.comment.addCommentLine(line)

    def validate(self):
        if not self.total() == 0:
            raise ValueError("total should be 0, was %s" % self.total())

    def total(self):
        total = 0
        for item in self.items:
            total += item.amount
        return total


# * Ledger Parser
"""

"""
class ParserTest(unittest.TestCase):
    def test(self):
        ledger = trim(
            """
            ; one line comment
            
            ; multi 
            ;      line
            ;           comment

            2006/01/01 * paycheck {2006/01/02} : this one is reconciled
            ; a transaction comment
            asset:checking                           50.00
            income:whatever

            2006/01/02 whatever mart : unreconciled
            expense:groceries                        10.00
            expense:hardware                          5.00
            asset:checking
            """)

        book = parseLedger(ledger)
        assert isinstance(book[0], Comment)
        assert len(book[0].lines) == 1
        assert isinstance(book[1], Comment)
        assert len(book[1].lines) == 3
        assert isinstance(book[2], Transaction)
        assert isinstance(book[3], Transaction)

reHeadLine = re.compile(
    r"""
    (?P<date>\d{4}/\d{2}/\d{2})
    (?P<star>\s+[*])?
    \s+
    (?P<party>(\w|[ ])+)
    (?P<memo>:(\s|\w)+)?
    """, re.VERBOSE)

reItemLine = re.compile(
    r"""
    ^
    (?P<account>\w+(:\w+)*)
    \s*
    (?P<amount>\d+\.\d{2})?
    """, re.VERBOSE)

def parseLedger(text):
    entry = None
    res = []
    for rawline in text.split("\n"):        
        line = rawline.strip()       
        if line == "":
            if entry:
                res.append(entry)
            entry = None
        elif line.startswith(";"):
            if not entry:
                entry = Comment()
            entry.addCommentLine(line)
        elif reHeadLine.match(line):
            match = reHeadLine.match(line).groupdict()
            match["date"], match["star"], match["party"], match["memo"]
            entry = Transaction(1,2,3)
        elif reItemLine.match(line):
            match = reItemLine.match(line).groupdict()            
            entry.addItem(match["account"], match["amount"])
    return res
        

# * --
if __name__=="__main__":
    unittest.main()
    
