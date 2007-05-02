#!/usr/bin/env python2.5
# ledger.py
from datetime import date
from decimal import Decimal
from handy import trim
from itertools import groupby
from pytypes import Date
from strongbox import Strongbox, attr
import time
import copy
import sys, os
import re

def balance(book, account):
    return sum([t.effectOnAccount(account) for t in book])

def bankView(book):
    res = [t.clone() for t in transactionsOnly(book)]
    for item in res:
        if item.cleared:
            #print item.posted , "<----", item.cleared
            item.posted = item.cleared
            item.cleared = None            
    res.sort(lambda a, b: cmp(parseDate(a.posted), parseDate(b.posted)))
    return res

class Comment:
    def __init__(self):
        self.lines = []

    def __str__(self):
        return "\n".join(self.lines + [""])
        
    def addCommentLine(self, line):
        self.lines.append(line)

    def effectOnAccount(self, account):
        return 0

def dailyHistory(book, account):
    return history(book, account, groupField=transactionDay)


def emacsView(book, account):
    yield "("
    for item in transactionsOnly(book):
        if item.state == '*':
            continue
        elif item.effectOnAccount(account):
            yield "".join(item.asEmacs(account))
    yield ")"

def history(book, account, groupField):
    total = 0
    res = []
    for month, mbook in groupby(transactionsOnly(book), groupField):
        total += balance(mbook, account)
        res.append((month, total))
    return res

class Item(Strongbox):
    account = attr(str)
    amount = attr(Decimal)
    implied = attr(bool, default=False)
    state = attr(str, okay=['*','!','']) # cleared, pending, default 
    charPos = attr(int, default=0)

    def clone(self):
        return Item(account=self.account, amount=Decimal(self.amount))

def monthlyHistory(book, account):
    return history(book, account, groupField=transactionMonth)

def parseDate(datestr):
    return [int(x) for x in datestr.split("/")]

def parseLedger(text):
    entry = None
    res = []
    charPos = 2 # we start at 0, emacs starts at 1, plus we're always 1 char behind
    for rawline in text.split("\n"):
        line = rawline.strip() 
        if line == "":
            if entry:
                res.append(entry)
            entry = None
        elif line.startswith(";"):
            if entry is None:
                entry = Comment()
            entry.addCommentLine(line)
        elif reHeadLine.match(line):
            match = reHeadLine.match(line).groupdict()
            entry = Transaction(posted=match["date"],
                                state = match["state"],
                                party = match["party"].strip(),
                                cleared = (match["cleared"]
                                           or match["effective"]),
                                checknum = match["checknum"],
                                memo = match["memo"],
                                charPos=charPos)
        elif reItemLine.match(line):
            match = reItemLine.match(line).groupdict()
            entry.addItem(match["account"], match["amount"], match['state'], charPos)

        charPos += len(rawline)+1 # +1 for len('\n')
    return res

reHeadLine = re.compile(
    r"""
    (?P<date>\d{4}/\d{2}/\d{2})(\=(?P<effective>\d{4}/\d{2}/\d{2}))?
    (?P<state>\s+[*|!])?
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
    (?P<state>\s+[*|!])?
    \s*
    (?P<account>\w+(:\w+)*)
    \s*
    (?P<amount>-?\d+\.\d{2})?
    """, re.VERBOSE)

class Transaction:
    def __init__(self, posted, party, checknum=None, memo=None, cleared=None,
                 state='',  items = None, charPos=0):
        self.posted = posted
        self.party = party
        self.memo = memo
        self.cleared = cleared
        self.state = state.strip() if state else ''
        self.isReconciled = bool(state=='*')
        self.items = items or []
        self.validate()
        self.comment = Comment()
        self.checknum = checknum
        self.charPos = charPos

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
        else:
            res.append("\n")
        return "".join(res)

    def addCommentLine(self, line):
        self.comment.addCommentLine(line)

    def addItem(self, account, amount_in, state, charPos):
        implied = False
        amount = amount_in
        if amount is None:
            implied = True
            amount = -self.total()
        if not state:
            state = self.state or ''
        self.items.append(Item(account=account,
                               amount=Decimal(amount),
                               implied=implied,
                               state=state.strip(),
                               charPos=charPos))

    def asEmacs(self, account):
        _ = ' '
        yield '("<stdin>" '  # @TODO: filename
        yield str(self.charPos)
        yield _

        # this is the emacs date format...
        y,m,d = [int(part) for part in self.posted.split('/')]
        date = time.mktime((y,m,d, 0,0,0,0,0,0))
        yield "(%s %s 0)" % (int(date / 65536),  int(date % 65536))
        
        yield _
        yield ('"%s"' % self.checknum) if self.checknum else 'nil'
        yield _
        yield '"%s"' % ((self.party + ' ' + self.memo) if self.memo else self.party)
        yield '\n'
        for item in self.items:
            if item.account.startswith(account):
                yield '  (%s "%s" "%s" %s)' % (
                    item.charPos, item.account, item.amount,
                    't' if item.state=='*' else 'pending' if item.state=='!' else 'nil' )
        yield ")"
        

    def bankDate(self):
        if self.cleared:
            return date(self.cleared)
        else:
            return date(self.posted)

    def clone(self):
        return Transaction(posted =self.posted, party=self.party,
                           memo=self.memo, cleared=self.cleared,
                           isReconciled = self.isReconciled,
                           items = [i.clone() for i in self.items])

    def effectOnAccount(self, account):
        return sum([item.amount for item in self.items
                    if item.account.startswith(account)])

    def total(self):
        return sum([item.amount for item in self.items])

    def validate(self):
        if not self.total() == 0:
            raise ValueError("total should be 0, was %s" % self.total())

def transactionDay(trans):
    return trans.posted

def transactionMonth(trans):
    return trans.posted[:7]

def transactionsOnly(book):
    return [x for x in book if isinstance(x, Transaction)]



if __name__=="__main__":
    
    if "emacs" in sys.argv:
        assert sys.argv[1:5] == ['-f','-','--uncleared','emacs']
        assert len(sys.argv) == 6, "emacs option requires account name"
        account = sys.argv[5]        
        book = parseLedger(sys.stdin.read())
        for item in emacsView(book, account):
            print item
    else:
        os.execvp('ledger', sys.argv[1:])
        
