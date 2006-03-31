#!/usr/local/bin/python2.4
import ledger
import sys

book = ledger.bankView(ledger.parseLedger(sys.stdin.read()))

if "-D" in sys.argv:
    filter = ledger.byDay
else:
    filter = ledger.byMonth

if "-r" in sys.argv:
    book = [t for t in book if t.isReconciled]


for month, balance in ledger.history(book, "asset:checking", filter):
    print "%10s %-15s" % (month, balance)

