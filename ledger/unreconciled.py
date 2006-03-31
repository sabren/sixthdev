#!/usr/local/bin/python2.4

import ledger
import sys

books = ledger.parseLedger(sys.stdin.read())

for item in ledger.transactionsOnly(books):
    if not item.effectOnAccount("asset:checking"): continue
    if not item.isReconciled:
        print item
        

