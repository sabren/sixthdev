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
import os
import sys
import socket
import select
import time
import thread
import msvcrt  # requires win32 (this is only for getting the password...)
  

## LOG =open("w:\cvssh\log.txt", "a")
## def debug(msg):
##     print >> LOG, msg
##     LOG.flush()

def pw_prompt():
    """
    Prompt the user for a password. We use getch so we
    can deal with the keyboard directly... (not stdin,
    since CVS is blocking that).. Oh, and it hides the
    password, too. :)
    """
    res = ""
    sys.stderr.write("Password: ")
    while 1:
        ch = msvcrt.getch() #@TODO: can I use curses for this on unix?
        res += ch
        if ord(ch)==13:
            break
    sys.stderr.write("\n")
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
        msvcrt.setmode(sys.__stdin__.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)


    ### step 1: gather connection info ###############################

    # username and server come from the cvs client via sys.argv:
    # sys.argv == ['stub', 'cvs.sabren.com', '-l', 'ftempy', 'cvs server']
    server   = sys.argv[1]
    username = sys.argv[3]    

    # we get the password from the user (for now anyway)
    password = pw_prompt()

    # "Root /cvsroot" is the first line of the local cvs's output to us.
    cvsroot = raw_input().split()[1]

    # instead of the normal pserver port, we use our own port
    # that wraps the pserver with stunnel ( http://www.stunnel.org/ )
    scvs_port = 2402 # @TODO: get a port assignment from iana.org



    ### step 2: connect to the server ################################

    ## debug("opening socket....")
    raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw.connect((server, scvs_port))
    sock = socket.ssl(raw)

    ## debug("got socket, sending auth request...")
    print >> sock, "BEGIN AUTH REQUEST"
    print >> sock, cvsroot
    print >> sock, username
    print >> sock, scramble(password)
    print >> sock, "END AUTH REQUEST"

    # either it loves us or it hates us:
    verdict = sock.read(len("I ____ YOU\n"))

    ## debug("verdict is: " + verdict)
    if verdict == "I HATE YOU\n":
        sys.stderr.write("ACCESS DENIED.\n")
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

