"""
Response.py - loosely emulates the ASP Response object for python CGI's
"""
import weblib

class Response:
    """Response object similar to the one from ASP"""

    def __init__(self, engine=weblib):

        self.engine = engine
        if engine is weblib:
            weblib.response = self

        self.header = ""
        self.buffer = ""
        self._headerSent = 0

        import StringIO
        self._webout = StringIO.StringIO()


    def __getattr__(self, name):
        res = None
        
        if name == "buffer":
            if not self._headerSent:
                self._sendHeader()
            res = self._webout.getvalue()
        elif name in self.__dict__.keys():
            res = self.__dict__[name]
        else:
            raise AttributeError
            
        return res
        

    #### PRIVATE METHODS ###################
    
    def _sendHeader(self):
        #@TODO: allow changing the content-type..
        self._webout.write("content-Type: text/html\n")
        self._webout.write(self.header)
        self._webout.write("\n")
        self._headerSent = 1
    

    #### PUBLIC METHODS ####################

    def write(self, data):
        self.buffer = self.buffer + data

    def addHeader(self, key, value):
        self.header = self.header + key + ": " + value + "\n"


    def addCookie(self, key, value):
        self.addHeader("Set-Cookie", key + "=" + value)


    def end(self):
        import sys
        sys.exit()


    def redirect(self, url):
        self.addHeader("Location", url)
        self.end()
    

    #### NOT IMPLEMENTED YET #####################
    #
    # these are part of the ASP Response object
    # but not this one:
    #
    # appendToLog() - doesn't really apply to apache
    # binaryWrite() - do we need this?
    # clear() - clears output buffer.. might do someday
    # flush() - also for buffering.. could do someday
    #
    # buffer - if true, buffer the output
    # cacheControl - the cache-control header
    # charSet - the charset header
    # contentType - the content-type header
    # expires - the expires header, in... minutes?
    # expiresAbsolute - the expires header as a date
    # isClientConnected - browser still connected?
    # PICS - a PICS content-rating label
    # Status - HTTP response code.. can i change this?!?
    #
    # Cookies - replaced by addCookie()

