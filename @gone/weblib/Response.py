__ver__="$Id$"
from weblib import Finished

class Response(object):
    """
    Minimal HTTP Response object
    """
    def __init__(self, out=None):
        self.out = out
        self.contentType = "text/html"
        self.headers = []
        self.buffer = ""
        self._sentHeaders = 0        

    def write(self, data):
        self.buffer = self.buffer + data
    
    def flush(self):
        if self.out:
            if not self._sentHeaders:
                self.out.write(self.getHeaders())
                self._sentHeaders = 1
            self.out.write(self.buffer)
            self.buffer = ""
            
    def end(self):
        self.flush()
        raise Finished

    ## header stuff #####################################
        
    def getHeaders(self):
        res = "Content-type: " + self.contentType + "\n"
        for k,v in self.headers:
            res += "%s:%s\n" % (k,v)
        return res + "\n"

    def addHeader(self, key, value):
        assert value is not None
        self.headers.append((key, value))

    def addCookie(self, key, value):
        self.addHeader("Set-Cookie", key + "=" + value)

    def redirect(self, url):
        self.addHeader("Status", "303")
        self.addHeader("Location", url)
        self.end()
