#!/usr/local/bin/python2.5
import sys
from ledger import bankView, parseLedger

stream = sys.stdin

for entry in bankView(parseLedger(stream.read())):
    print entry
