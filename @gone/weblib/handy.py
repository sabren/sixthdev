# handy routines
# $Id$

def xmlEncode(s):
    """
    xmlEncode(s) ->  s with >, <, and & escaped as &gt;, &lt; and &amp;
    """
    res = ""
    for ch in s:
        if ch == ">":
            res = res + "&gt;"
        elif ch=="<":
            res = res + "&lt;"
        elif ch=="&":
            res=res + "&amp;"
        else:
            res = res + ch
    return res
    
def sendmail(msg):
    """
    sendmail(msg) -> None  (sends an email.)
    """
    print '<pre style="background:gold; border:solid black 1px; color:black">'\
          + xmlEncode(msg) + '</pre>'
