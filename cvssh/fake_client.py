"""
This is just a fake pserver client.
It logs you in and lets you issue CVS commands at a prompt.
It's not required, but it was helpful in development.
"""

import select
import socket
from cvssh import SocketStream, scramble

s = SocketStream(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
s.connect(("localhost", 2401))

print >> s, "BEGIN AUTH REQUEST"
print >> s, "/cvs/project"
print >> s, "user"
print >> s, scramble("password")
print >> s, "END AUTH REQUEST"
print >> s, "Root /cvs/project"

print dir(s.socket)

while 1:
    for x in range(200):
        readable, writable, mistake = select.select([s], [s], [s])
        if readable:
            print repr(s.read(65536))
    print >> s, raw_input(">")
