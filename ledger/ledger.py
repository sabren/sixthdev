#!/usr/bin/env python2.5
"""
Ledger is a text-based double-entry account program:

  http://www.newartisans.com/software/ledger.html
  http://sourceforge.net/projects/ledger/
  
This is a python module for working with files in a
subset of the ledger syntax. It currently handles
basic transactions and comments.
"""
LICENSE=\
'''
Copyright (c) 2008 Sabren Enterprises Inc
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    
    * Neither the name of the <ORGANIZATION> nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
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

## object model ######################################################

class Comment:
    """
    A comment inside the ledger file.
    Can be freestanding or part of a Transaction.
    """
    def __init__(self):
        self.lines = []

    def __str__(self):
        return "\n".join(self.lines + [""])
        
    def addCommentLine(self, line):
        self.lines.append(line)

    def effectOnAccount(self, account):
        return 0

class Item(Strongbox):
    """
    A line item inside a Transaction.
    """
    account = attr(str)
    amount = attr(Decimal)
    implied = attr(bool, default=False)
    state = attr(str, okay=['*','!','']) # cleared, pending, default 
    charPos = attr(int, default=0)

    def clone(self):
        return Item(account=self.account, amount=Decimal(self.amount))

class Transaction:
    """
    An individual transaction. Contains Items and possibly a Comment.
    """
    def __init__(self, posted, party, checknum=None, memo=None, preComment=None,
                 cleared=None, state='',  items = None, lineNum=0, charPos=0):
        self.posted = posted
        self.party = party
        self.memo = memo
        self.cleared = cleared
        self.state = state.strip() if state else ''
        self.isReconciled = bool(self.state=='*')
        self.items = items or []
        self.validate()
        self.comment = Comment()
        self.checknum = checknum
        self.lineNum = lineNum
        self.charPos = charPos
        self.preComment = preComment

    def __str__(self):

        res = []
        
        if self.preComment:
            res.append(str(self.preComment))
            
        res.append(self.posted)
        if self.cleared: res.append("=%s" % self.cleared)
        res.append(" ")
        if self.isReconciled: res.append("* ")
        if self.checknum: res.append("(%s) " % self.checknum)
        res.append(self.party)
        if self.memo: res.append(" " + self.memo)
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

    def addItem(self, account, amount_in, state='', charPos=0):
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

        def dequote(s):
            return s.replace('"',r'\"').replace("'",r"\\'")

        
        
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
        yield '"%s"' % dequote((self.party + ' ' + self.memo)
                               if self.memo else self.party)
        yield '\n'
        for item in self.items:
            if item.account.startswith(account):
                yield '  (%s "%s" "%s" %s)' % (
                    item.charPos, item.account, item.amount,
                    ('t' if item.state=='*'
                     else ('pending' if item.state=='!'
                           else 'nil' )))
        yield ")"
        

    def bankDate(self):
        if self.cleared:
            return date(self.cleared)
        else:
            return date(self.posted)

    def clone(self):
        return Transaction(posted =self.posted, party=self.party,
                           memo=self.memo, cleared=self.cleared,
                           state = self.state,
                           items = [i.clone() for i in self.items])

    def effectOnAccount(self, account):
        return sum([item.amount for item in self.items
                    if item.account.startswith(account)])

    def total(self):
        return sum([item.amount for item in self.items])

    def validate(self):
        if not self.total() == 0:
            raise ValueError("total should be 0, was %s" % self.total())


## parser ############################################################

reHeadLine = re.compile(
    r"""
    (?P<date>\d{4}/\d{2}/\d{2})(\=(?P<effective>\d{4}/\d{2}/\d{2}))?
    (?P<state>\s+[\*|!])?
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

def parseDate(datestr):
    return [int(x) for x in datestr.split("/")]

def parseLedger(text):
    """
    returns a list containing Comments and Transactions
    """
    entry = None
    res = []
    lineNum = 0
    charPos = 2 # we start at 0, emacs starts at 1
                # plus we're always 1 char behind (because...?)
    for rawline in text.split("\n"):
        lineNum += 1
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
            preComment = None
            if entry is not None:
                assert isinstance(entry, Comment)
                preComment = entry
            entry = Transaction(posted=match["date"],
                                state = match["state"],
                                party = match["party"].strip(),
                                cleared = (match["cleared"]
                                           or match["effective"]),
                                checknum = match["checknum"],
                                memo = match["memo"],
                                preComment = preComment,
                                lineNum = lineNum,
                                charPos=charPos)        
        elif reItemLine.match(line):
            assert entry, "got item before entry on line %s" % lineNum
            match = reItemLine.match(line).groupdict()
            entry.addItem(match["account"], match["amount"],
                          match['state'], charPos)

        charPos += len(rawline)+1 # +1 for len('\n')
    return res





## helper functions and reports ######################################

def balance(book, account):
    return sum([t.effectOnAccount(account) for t in book])

def bankView(book):
    """
    This shows the bank's view of the ledger. That is,
    it sorts by the effective or cleared-on date. This
    is useful when trying to reconcile with a bank
    statement.
    """
    res = [t.clone() for t in transactionsOnly(book)]
    for item in res:
        if item.cleared:
            #print item.posted , "<----", item.cleared
            item.posted = item.cleared
            item.cleared = None            
    res.sort(lambda a, b: cmp(parseDate(a.posted), parseDate(b.posted)))
    return res


def checkTransactionOrder(book):
    last =None
    for t in transactionsOnly(book):
        if t.party == 'opening balance' and last is None:
            continue # b/c sometimes we have transactions from december up front
        tdate = parseDate(t.posted)
        if tdate < last and last is not None:
            print "transaction out of order on line %s" % t.lineNum
            print "---------------------------------" + ("-"*len(str(t.lineNum)))
            print t
        last = tdate

def dailyHistory(book, account):
    return history(book, account, groupField=transactionDay)

def emacsView(book, account):
    """
    This attempts to mimic ledger's --emacs flag.
    """
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

def _genMerge(book1, book2):
    """
    recursively merge two books.
    (assumes they are sorted by date)
    """

    def holdComments(book, hold):
        while book:
            if isinstance(book[0], Transaction):
                return
            else: # comments:
                hold.append(book.pop(0))
            
    # wow this is ugly :(
    # this is messy because we're trying to keep the comments
    # in place while we merge the others :/
    hold1 = []
    hold2 = []

    holdComments(book1, hold1)
    while book1:
        holdComments(book2, hold2)
        if len(book2) == 0:
            while hold1: yield hold1.pop(0)
            while hold2: yield hold2.pop(0)
            break
        else:
            d1 = parseDate(book1[0].posted)
            d2 = parseDate(book2[0].posted)
            if d1 < d2:
                while hold1: yield hold1.pop(0)
                yield book1.pop(0)
                holdComments(book1, hold1)
            else:
                while hold2: yield hold2.pop(0)
                yield book2.pop(0)

    for c1 in hold1: yield c1
    for c2 in hold2: yield c2

    # done. one list is empty, empty the other:
    if book1:
        for item in book1: yield item
    else:
        for item in book2: yield item
        
def merged(book1, book2):
    return list(_genMerge(book1[:], book2[:]))
    
def monthlyHistory(book, account):
    return history(book, account, groupField=transactionMonth)

def transactionDay(trans):
    return trans.posted

def transactionMonth(trans):
    return trans.posted[:7]

def transactionsOnly(book):
    return [x for x in book if isinstance(x, Transaction)]


if __name__=="__main__":

    #@TODO: real option parsing here
    
    if "emacs" in sys.argv:
        assert sys.argv[1:5] == ['-f','-','--uncleared','emacs']
        assert len(sys.argv) == 6, "emacs option requires account name"
        account = sys.argv[5]        
        book = parseLedger(sys.stdin.read())
        for item in emacsView(book, account):
            print item
    elif "--check" in sys.argv:
        fname = sys.argv[-1]
        checkTransactionOrder(parseLedger(open(fname).read()))
    elif "--merge" in sys.argv:
        book1, book2 = [parseLedger(open(f).read()) for f in sys.argv[-2:]]
        for item in merged(book1, book2):
            print item
    else:
        os.execvp('ledger', sys.argv[1:])
        
