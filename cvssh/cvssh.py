#!/usr/bin/python
"""
cvssh.py - secure ext-to-pserver bridge for cvs

This program illustrates a new (and hopefully superior)
method of securing a CVS pserver.

It offers  an ext-to-pserver bridge: From the client CVS's
point of view, we look like ssh, but what we really do is
make our own ssl connection to a stunnel demon. This gives
us the security and client-side ease of ext/ssh with the
flexibility of pserver on the repository.
"""
__ver__="$Id$"

## -------------------------------------------------------------
## license
## -------------------------------------------------------------
## cvssh - a secure bridge for cvs pservers
## Copyright (C) 2002 Sabren Enterprises, Inc.
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  
## 02111-1307, USA.
## -------------------------------------------------------------

import os
import sys
import socket
import select
import time
import thread
import getpass

## LOG =open("w:\cvssh\log.txt", "a")
## def debug(msg):
##     print >> LOG, msg
##     LOG.flush()


# instead of the normal pserver port, we use our own port
# that wraps the pserver with stunnel ( http://www.stunnel.org/ )
SCVS_PORT = 2402 # @TODO: get a port assignment from iana.org

def get_connection(server):
    raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw.connect((server, SCVS_PORT))
    sock = socket.ssl(raw)
    return raw, sock


def request_auth(sock, username, cvsroot, password):
    """
    request authorization from the pserver.
    """
    print >> sock, "BEGIN AUTH REQUEST"
    print >> sock, cvsroot
    print >> sock, username
    print >> sock, scramble(password)
    print >> sock, "END AUTH REQUEST"

    # either it loves us or it hates us:
    verdict = sock.read(len("I ____ YOU\n"))

    ## debug("verdict is: " + verdict)
    res = 0 # pessimism pays.
    if verdict == "I LOVE YOU\n":
        res = 1 # aww. love trumps pessimism. how sweet.
    return res



def scramble(data):
    """
    CVS pserver uses a simple, easily reversable
    ciphertext to transfer passwords. This is
    the reason it's so insecure. :)
    """
    # this translation table came from the CVS source code:
    shifts = (
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
        114,120, 53, 79, 96,109, 72,108, 70, 64, 76, 67,116, 74, 68, 87,
        111, 52, 75,119, 49, 34, 82, 81, 95, 65,112, 86,118,110,122,105,
        41, 57, 83, 43, 46,102, 40, 89, 38,103, 45, 50, 42,123, 91, 35,
        125, 55, 54, 66,124,126, 59, 47, 92, 71,115, 78, 88,107,106, 56,
        36,121,117,104,101,100, 69, 73, 99, 63, 94, 93, 39, 37, 61, 48,
        58,113, 32, 90, 44, 98, 60, 51, 33, 97, 62, 77, 84, 80, 85,223,
        225,216,187,166,229,189,222,188,141,249,148,200,184,136,248,190,
        199,170,181,204,138,232,218,183,255,234,220,247,213,203,226,193,
        174,172,228,252,217,201,131,230,197,211,145,238,161,179,160,212,
        207,221,254,173,202,146,224,151,140,196,205,130,135,133,143,246,
        192,159,244,239,185,168,215,144,139,165,180,157,147,186,214,176,
        227,231,219,169,175,156,206,198,129,164,150,210,154,177,134,127,
        182,128,158,208,162,132,167,209,149,241,153,251,237,236,171,195,
        243,233,253,240,194,250,191,155,142,137,245,235,163,242,178,152 )
    return "A" + "".join(map(lambda ch, sh=shifts: chr(sh[ord(ch)]), data))
  


def cvspass_path():
    return os.environ["HOME"] + os.sep + ".cvspass"


def cvspass_key(username, server, cvsroot):
    return ":pserver:%s@%s:%s" % (username, server, cvsroot)


def save_password(username, server, cvsroot, password):
    """
    Emulate the -d:pserver:... login function.
    """
    # @TODO: allow "logout"

    # remove any old passwords for this key:
    clean = [line[:-1] for line in open(cvspass_path(), "r").readlines()
             if not line.startswith(cvspass_key(username, server, cvsroot))]

    # now save it with the new password
    file = open(cvspass_path(), "w")
    for line in clean:
        file.write(line)
    print >> file, cvspass_key(username, server, cvsroot), scramble(password)
    file.close()


def load_password(username, server, cvsroot):
    """
    We read passwords out of the .cvspass file, just like
    cvs -d:pserver: does. Note that this file could be
    considered fairly insecure...
    
    However, it releives the need for an interactive password
    prompt, which worked okay with msvcrt.getch(), but not
    on linux.
    """
    # @TODO: test whether this works with empty password.
    res = None
    try:
        cvspass = open(cvspass_path(),"r")
        for line in cvspass.readlines():
            if line.startswith(cvspass_key(username, server, cvsroot)):
                res = line.split(" ")[1] # the second field
                res = res[1:-1]          # strip the 'A" and the newline
                res = scramble(res)[1:]  # or unscramble it, really... :)
                raise "found!"
    finally:
        # there could either be an error for opening the file,
        # the "found!" exception, or just a normal loop through
        # without finding anything.. So we use finally.
        return res


# These next two functions are based on Sam Rushing's
# Medusa/monitor_client_win32.py ...
# See http://www.nightmare.com/ for more of Sam's stuff.


def client_thread(lock, sock):
    """
    Non-blocking I/O on sys.stdin is not allowd in
    Python for win32 (because select.select() uses
    winsock, and thus only works for sockets).
    So we use threads.

    This thread talks to the local parent cvs process.
    """
    buffer = ""
    while not sys.stdin.closed:
        ch = sys.stdin.read(1)
        if not ch:
            # stdin is closed, so we're all done.
            lock.release()
            sys.exit()
        buffer += ch
        if ch == '\n':
            sock.write(buffer)
            ## debug(">> " + repr(buffer))
            buffer = ""


def server_thread(lock, sock, raw):
    """
    This thread talks to the remote cvs process.
    sock is a secure socket, raw is the raw tcp/ip socket.
    """
    while lock.locked():
        r,w,e = select.select([raw], [raw], [raw])
        if raw in r:
            data = sock.read(1024)
            ## debug("<< " + repr(data))
            sys.stdout.write(data)
            sys.stdout.flush()



if __name__=="__main__":
    
    ## debug("** start **")

    # make sure we use binary mode on win32:
    if sys.platform=="win32":
        import msvcrt
        msvcrt.setmode(sys.__stdin__.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)

    if len(sys.argv) < 3:
        print "usage: cvssh user@server:/cvs/root login"
        print "other than that, this should be called by cvs."
        sys.exit()


    ### step 0: login ################################################


    # login is -->  cvssh user@server:/cvs/root login
    if sys.argv[2]=="login":

        # make sure we have all the info...
        try:
            username, rest = sys.argv[1].split("@")
            server, cvsroot = rest.split(":")
        except:
            print "usage: cvssh user@server:/cvs/root login"
            sys.exit()

        # okay, so get the password...
        password = getpass.getpass()

        # test the login...
        raw, sock = get_connection(server)
        if request_auth(sock, username, cvsroot, password):
            save_password(username, server, cvsroot, password)
        else:
            print "ACCESS DENIED: invalid username or password"
        sys.exit() # yuck. how lazy of me.


    ### step 1: gather connection info ###############################

    # username and server come from the cvs client via sys.argv:
    # sys.argv == ['stub', 'cvs.sabren.com', '-l', 'ftempy', 'cvs server']
    server   = sys.argv[1]
    username = sys.argv[3]    

    # "Root /cvsroot" is the first line of the local cvs's output to us.
    cvsroot = raw_input().split()[1]

    # load password from user's .cvspass file (or die trying):
    # note that "" is an okay password, but None isn't....
    password = load_password(username, server, cvsroot)
    ## debug("password is: " + password)
    if password is None:
        sys.stderr.write("No password found. Use 'cvssh login' first.\n")
        sys.exit()


    ### step 2: connect to the server ################################

    ## debug("opening socket....")
    raw, sock = get_connection(server)

    ## debug("got socket, sending auth request...")
    if not request_auth(sock, username, cvsroot, password):
        sys.stderr.write("ACCESS DENIED: try 'cvssh login' again.\n")
        sys.exit()


    ### step 3: let cvs do its thing #################################

    ## debug("sending the cvsroot")
    # we read the cvsroot in earlier, so we have to put it back:
    print >> sock, "Root " + cvsroot # "+" because ssl doesn't like commas :)

    ## debug("getting the lock...")
    lock = thread.allocate_lock()
    lock.acquire()

    ## Now that we've done our magic, we just get out of the
    ## way and let our local cvs process chat with the pserver
    
    ## debug("starting new thread")
    thread.start_new_thread(client_thread, (lock, sock))
    server_thread(lock, sock, raw)

    ## debug("** all done **")
    raw.close()

