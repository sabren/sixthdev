"""
Misc handy routines
"""
import whrandom, string

def randpass(length=5):    
    okay = "abcdefghijkmnopqrstuvwxyz2345678923456789"
    res = ""
    for i in range(length+1):
        res += okay[whrandom.randrange(0, len(okay))]
    return res


def readable(bytes):
    """
    convert a bytecount into human-readable text
    """
    x = bytes
    b = x % 1000; x-=b; x/=1000
    k = x % 1000; x-=k; x/=1000
    m = x % 1000; x-=m; x/=1000
    g = x % 1000; x-=g; x/=1000
    if g: return str(g) + "." + string.zfill(str(m),3)[0] + "G"
    if m: return str(m) + "." + string.zfill(str(k),3)[0] + "M"
    if k: return str(k) + "." + string.zfill(str(b),3)[0] + "k"
    return str(b)

def sendmail(mail):
    import os
    sender = os.popen("/usr/sbin/sendmail -t", "w")
    sender.write(mail)
    sender.close()


def trim(s):
    """
    strips leading indentation from a multi-line string.
    for saving bandwith while making code look nice
    """

    import string
    lines = string.split(s, "\n")

    # strip leading blank line
    if lines[0] == "":
        lines = lines[1:]
        
    # strip indentation
    indent = len(lines[0]) - len(string.lstrip(lines[0]))
    for i in range(len(lines)):
        lines[i] = lines[i][indent:]

    return string.join(lines, "\n")


def indent(s, depth=1, indenter="    "):
    """
    opposite of trim
    """
    import string
    lines = string.split(s, "\n")

    # don't indent trailing newline
    trailer = ""
    if lines[-1] == "":
        lines = lines[:-1]
        # BUT.. add it back in later
        trailer = "\n"
        
    for i in range(len(lines)):
        lines[i] = (indenter * depth) + lines[i]
        
    return string.join(lines, "\n") + trailer
   



def uid():
    """
    unique identifier generator, for sessions, etc
    Returns a 32 character, printable, unique string
    """
    import md5, whrandom, string
    tmp, uid = "", ""
    
    # first, just get some random numbers
    for i in range(64):
        tmp = tmp + chr(whrandom.randint(0,255))

    # then make a 16-byte md5 digest...
    tmp = md5.new(tmp).digest()

    # and, since md5 is unprintable,
    # reformat it in hexidecimal:
    for i in tmp:
        uid = uid + string.zfill(hex(ord(i))[2:],2)        

    return uid


