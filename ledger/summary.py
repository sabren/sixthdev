#!/usr/local/bin/python2.5
import ledger
import sys

book = ledger.bankView(ledger.parseLedger(sys.stdin.read()))

if "-D" in sys.argv:
    report = ledger.dailyHistory
else:
    report = ledger.monthlyHistory

if "-r" in sys.argv:
    book = [t for t in book if t.isReconciled]


for month, balance in report(book, "asset:checking"):
    print "%10s %-15s" % (month, balance)

