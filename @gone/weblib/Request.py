"""
Request.py - emulates the ASP Request object for python CGI's

don't want to use cgi because it has no cookies, and form/querystring
get lumped together. Plus it's old and crufty. :) .. but it also
*works*, so for now we'll use cgi.py after all..

@TODO: license
"""
__ver__="$Id$"

# @TODO: cookie support
# @TODO: request["x"] should look at all 3 sources
# @TODO: figure out how to treat file uploads

import string
import weblib


class Request:

    ## constructor ###################################################
    
    def __init__(self, querystring=None, form=None, environ=None, method=None,
                 cookie=None, engine=weblib, content=None, contentType=None):

        self.engine = engine
        if self.engine is weblib:
            weblib.request = self  # @TODO: get rid of this!!

        #@TODO: rename .contentType to .type !!!!!!!
        self._doEnvironJunk(environ)
        self._doQueryJunk(querystring)
        self._doCookieJunk(cookie)
        self._doMethodJunk(method, content)
        self._doTypeJunk(contentType)
        self._doContentJunk(content, form)
        
    ## private methods #################################################

    def _doEnvironJunk(self, environ=None):
        if environ is not None:
            self.environ = environ
        else:
            ## os.environ.copy() actually shares
            ## data with os.environ .. I suppose
            ## because it's an object.. Anyway,
            ## that's bad for us because it makes environ
            ## global, and that's NOT what we want. so
            ## we do the following instead:
            import os
            self.environ = {}
            for item in os.environ.keys():
                self.environ[item] = os.environ[item]

    def _doQueryJunk(self, querystring=None):
        if querystring is not None:
            self.querystring = querystring
        else:
            self.querystring = self.environ.get("QUERY_STRING", "")
        ## query, a hash of the querystring:
        self.query = self.parse(self.querystring, decode=1)

    def _doCookieJunk(self, cookie=None):
        ## @TODO: get some real cookie parsing abilities...
        if cookie is not None:
            self.cookie = cookie
        else:
            self.cookie = self.parse(self.environ.get("HTTP_COOKIE", ""),
                                     splitter=";")

    def _doMethodJunk(self, method=None, content=None):
        ## method
        if method is not None:
            self.method = method
        else:
            self.method = self.environ.get("REQUEST_METHOD")
            if self.method is None:
                if content:
                    self.method = "POST"
                else:
                    self.method = "GET"

    def _doTypeJunk(self, contentType):
        ## contentType:
        if contentType is not None:
            self.contentType = contentType
        else:
            self.contentType=self.environ.get("CONTENT_TYPE")
            if self.contentType is None:
                self.contentType = "application/x-www-form-urlencoded"
        
    def _doContentJunk(self, content=None, form=None):
        import sys

        ## multipart 
        if self.contentType[:10]=="multipart/":
            if content:
                self.form = self._parseMultiPartForm(content)
                self.content = content
            else:
                self.form = self._parseMultiPartForm(sys.stdin)
                self.content = ""

        ## any other type of form..
        else:

            ## content and contentLength:
            if content is not None:
                self.content = content
                self.contentLength = len(content)
            else:
                self.contentLength = int(self.environ.get("CONTENT_LENGTH", 0))
                if self.contentLength:
                    self.content = sys.stdin.read(self.contentLength)
                else:
                    self.content=""

            ## the form itself
            if form is not None:
                self.form = form
            elif self.method == "POST":
                self.form = self.parse(self.content, decode=1)
            else:
                self.form = {}

    def _parseMultiPartForm(self, stream):
        ## multipart/form-data (file upload forms):
        ## @TODO: lots of stuff! probably best to just rewrite this
        ## rather than try to yank stuff out of FieldStorage..
        form = {}
        import cgi, StringIO

        # pretend we're a file (FieldStorage requires this)
        # on the web, this would usually be stdin, which IS a file,
        # but if we assume that, we can't assign to content..
        # perhaps content should be a file-like pointer anyway?

        if type(stream)==type(""):
            storage = cgi.FieldStorage(StringIO.StringIO(stream),
                                       environ=self.environ)
            #@TODO: this isn't working in test!
        else:
            storage = cgi.FieldStorage(stream, environ=self.environ)

        for field in storage.keys():                
            ## handle multiple values for one field:
            if type(storage[field]) == type([]):
                form[field] = ()
                for item in storage[field]:
                    if item.filename:
                        form[field]=\
                            self._tupleMerge(form[field], item)
                    else:
                        form[field]=\
                            self._tupleMerge(form[field], item.value)
            ## or a single value for the field:
            elif storage[field].filename:
                form[field]=storage[field]
            else:
                form[field]=storage[field].value
        return form



    def _tupleMerge(self, head, tail):
        """converts head and tail into tuples (if they're not) and merges them"""

        if type(head) != type(()):
            head = (head,)
        if type(tail) != type(()):
            tail = (tail,)
        return head + tail


    def parse(self, what, splitter="&", decode=0):
        res = {}
        for pair in string.split(what, splitter):
            if decode:
                pair = weblib.urlDecode(pair)
            l = string.split(pair, "=", 1)
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ''
            if res.has_key(k):
                res[k] = self._tupleMerge(res[k], v)
            else:
                res[k]=v
        return res



    ## Dictionary Methods @TODO: more of them ##########################


    def __getitem__(self, key):
        res = None
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                if res is None:
                    res = dict[key]
                else:
                    res = self._tupleMerge(res, dict[key])
        if res is None:
            raise KeyError, key
        return res


    def __delitem__(self, key):
        res = None
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                res = 1
                del dict[key]
        if res is None:
            raise KeyError, key

    def get(self, key, failobj=None):
        try:
            return self[key]
        except KeyError:
            return failobj


    def keys(self):
        res = {}
        for dict in [self.query, self.form, self.cookie]:
            for key in dict.keys():
                res[key] = 1
                
        return res.keys()


    def has_key(self, key):
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                return 1
        return 0

