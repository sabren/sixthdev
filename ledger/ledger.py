#!/usr/bin/env python2.4
# ledger.py
import re
import copy
import unittest
from itertools import groupby
from handy import trim
from decimal import Decimal
from datetime import date
from strongbox import Strongbox, attr
from pytypes import Date

# * Comments

class CommentTest(unittest.TestCase):
    def test_str(self):
        c = Comment()
        c.addCommentLine("; 1")
        c.addCommentLine("; 2")
        self.assertEquals("; 1\n; 2", str(c))

class Comment:
    def __init__(self):
        self.lines = []

    def __str__(self):
        return "\n".join(self.lines)
        
    def addCommentLine(self, line):
        self.lines.append(line)

    def effectOnAccount(self, account):
        return 0

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
            memo = ": owed him money",
            cleared = "2005/05/02",
            isReconciled = False,
            items = [])
        t.addItem("liability:fred", "10.00"),
        self.assertRaises(ValueError, t.validate)
        t.addItem("asset:checking", "-10.00"),
        t.validate() # should work now.

    def test_effectOnAccount(self):
        t = Transaction(None, None, None, items = [
            Item(account="asset:cash", amount="-6"),
            Item(account="expense:a",  amount="2"),
            Item(account="expense:b",  amount="3"),
            Item(account="expense:c",  amount="1"),])
        self.assertEquals(-6, t.effectOnAccount("asset:"))
        self.assertEquals(-6, t.effectOnAccount("asset:cash"))
        self.assertEquals(-6, t.effectOnAccount("a"))
        self.assertEquals(0,  t.effectOnAccount("equity"))
        self.assertEquals(2,  t.effectOnAccount("expense:a"))
        self.assertEquals(3,  t.effectOnAccount("expense:b"))
        self.assertEquals(1,  t.effectOnAccount("expense:c"))
        self.assertEquals(6,  t.effectOnAccount("expense:"))

    def test_str(self):
        t = Transaction(posted="2005/01/01",
                        checknum="232",
                        party="asdf",
                        isReconciled = True,
                        memo=": xxx", items = [
            Item(account="asset:cash", amount="-600"),
            Item(account="expense:a",  amount="2"),
            Item(account="expense:b",  amount="3"),
            Item(account="expense:c",  amount="595", implied=True),])
        self.assertEquals(str(t), trim(
            """
            2005/01/01 * (232) asdf : xxx
                asset:cash                               -600.00
                expense:a                                   2.00
                expense:b                                   3.00
                expense:c
            """))
        
      
class Item(Strongbox):
    account = attr(str)
    amount = attr(Decimal)
    implied = attr(bool, default=False)

    def clone(self):
        return Item(account=self.account, amount=Decimal(self.amount))
        

class Transaction:
    def __init__(self, posted, party, checknum=None, memo=None,
                 cleared=None, isReconciled=False,
                 items = None):
        self.posted = posted
        self.party = party
        self.memo = memo
        self.cleared = cleared
        self.isReconciled = isReconciled
        self.items = items or []
        self.validate()
        self.comment = Comment()
        self.checknum = checknum

    def __str__(self):
        res = []
        res.append(self.posted + " ")
        if self.isReconciled:
            res.append("* ")
        if self.checknum:
            res.append("(%s) " % self.checknum)
        res.append(self.party)
        if self.cleared:
            res.append(" {%s}" % self.cleared)
        if self.memo:
            res.append(" " + self.memo)
        res.append("\n")
        for i in self.items:
            if i.implied:
                res.append("    %s\n" % i.account)
            else:
                res.append("    %-38s %9.2f\n" % (i.account, i.amount))
        if self.comment:
            res.append(str(self.comment))
        return "".join(res)
        

    def clone(self):
        return Transaction(posted =self.posted, party=self.party,
                           memo=self.memo, cleared=self.cleared,
                           isReconciled = self.isReconciled,
                           items = [i.clone() for i in self.items])

    def addItem(self, account, amount_in):
        implied = False
        amount = amount_in
        if amount is None:
            implied = True
            amount = -self.total()
        self.items.append(Item(account=account,
                               amount=Decimal(amount),
                               implied=implied))

    def bankDate(self):
        if self.cleared:
            return date(self.cleared)
        else:
            return date(self.posted)

    def addCommentLine(self, line):
        self.comment.addCommentLine(line)

    def validate(self):
        if not self.total() == 0:
            raise ValueError("total should be 0, was %s" % self.total())

    def total(self):
        return sum([item.amount for item in self.items])

    def effectOnAccount(self, account):
        return sum([item.amount for item in self.items
                    if item.account.startswith(account)])


# * Ledger Parser
"""
The ledger is represented as a list of Comments and Transactions
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
                income:whatever                         -50.00
                asset:checking
            ;   a transaction comment

            2006/01/02 (1000) whatever mart : unreconciled check 1000
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
        assert book[2].posted == "2006/01/01"
        self.assertEquals(book[2].cleared, "2006/01/02")
        assert book[2].items[0].amount == -50
        assert book[2].items[1].amount ==  50
        assert isinstance(book[3], Transaction)
        assert book[3].memo.count("unreconciled")
        self.assertEquals("1000", book[3].checknum)
        assert book[3].items[0].amount == 10
        assert book[3].items[1].amount ==  5
        assert book[3].items[1].implied == False
        assert book[3].items[2].amount == -15
        assert book[3].items[2].implied == True

reHeadLine = re.compile(
    r"""
    (?P<date>\d{4}/\d{2}/\d{2})
    (?P<star>\s+[*])?
    (\s+[(](?P<checknum>\d+)[)])? # check number.. discard for now
    \s+
    (?P<party>([^:{])+)
    (\{(?P<cleared>\d{4}/\d{2}/\d{2})\}\s*)?
    (?P<memo>:.*)?
    """, re.VERBOSE)

reItemLine = re.compile(
    r"""
    ^
    \s*
    (?P<account>\w+(:\w+)*)
    \s*
    (?P<amount>-?\d+\.\d{2})?
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
            entry = Transaction(posted=match["date"],
                                isReconciled = bool(match["star"]),
                                party = match["party"].strip(),
                                cleared = match["cleared"],
                                checknum = match["checknum"],
                                memo = match["memo"])
        elif reItemLine.match(line):
            match = reItemLine.match(line).groupdict()
            entry.addItem(match["account"], match["amount"])
    return res
        

# * Balance History
"""
Take an account, group it by month.
"""

class HistoryTest(unittest.TestCase):
    def test(self):
        book = parseLedger(trim(
            """
            ; yadda yadda yadda
            
            2005/01/01 opening balance
              equity:open           -100.00
              asset:cash             100.00

            2005/02/05 the store
              expense:stuff            5.00
              asset:cash              -5.00

            2005/02/10 the store again
              expense:stuff            5.00
              asset:cash              -5.00

            2005/03/01 beat up kid for lunch money
              asset:cash                5.00
              income:extortion         -5.00
            """))
        
        self.assertEquals(95, balance(book, "asset:"))
        self.assertEquals(monthlyHistory(book, "asset:"),
               [("2005/01", 100),
                ("2005/02", 90),
                ("2005/03", 95)])
        self.assertEquals(monthlyHistory(book, "expense:"),
               [("2005/01",  0),
                ("2005/02", 10),
                ("2005/03", 10)])
        self.assertEquals(monthlyHistory(book, "income:"),
               [("2005/01",  0),
                ("2005/02",  0),
                ("2005/03", -5)])



# * bankView and History

class BankViewTest(unittest.TestCase):
    def test(self):
        book = parseLedger(trim(
            """
            2005/01/01 * asdf {2005/02/01}
                expense:asdf                               10.00
                asset:checking
            """))

        assert bankView(book)[0].posted == "2005/02/01"
        assert bankView(book)[0].cleared is None
        self.assertEquals(str(bankView(book)[0]), trim(
            """
            2005/02/01 * asdf
                expense:asdf                               10.00
                asset:checking                            -10.00
            """))

def bankView(book):
    res = [t.clone() for t in transactionsOnly(book)]
    for item in res:
        if item.cleared:
            #print item.posted , "<----", item.cleared
            item.posted = item.cleared
            item.cleared = None            
    res.sort(lambda a, b: cmp(parseDate(a.posted), parseDate(b.posted)))
    return res

def balance(book, account):
    return sum([t.effectOnAccount(account) for t in book])

def transactionsOnly(book):
    return [x for x in book if isinstance(x, Transaction)]

def parseDate(datestr):
    return [int(x) for x in datestr.split("/")]

def byMonth(trans):
    return trans.posted[:7]

def byDay(trans):
    return trans.posted

def history(book, account, filter):
    total = 0
    res = []
    for month, mbook in groupby(transactionsOnly(book), filter):
        total += balance(mbook, account)
        res.append((month, total))
    return res

def monthlyHistory(book, account):
    return history(book, account, byMonth)

def dailyHistory(book, account):
    return history(book, account, byDay)
    
# * --
if __name__=="__main__":
    unittest.main()
        
    
