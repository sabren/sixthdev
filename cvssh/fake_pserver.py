"""
This is a fake pserver.
All it does is print out whatever the cvs client sends it.
This file isn't required, but was useful in development.
"""
import socket

# this mostly came from the python manual...

HOST = ''                # Symbolic name meaning the local host
PORT = 2401              # CVS pserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    try:
        conn, addr = s.accept()
        while 1:
            data = conn.recv(1024)
            if not data: break
            print data
        conn.close()
    except:
        print "[[[EXCEPTION]]]"

