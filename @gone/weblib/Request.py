"""
Request.py - emulates the ASP Request object for python CGI's
"""
__ver__="$Id$"

from weblib import urlDecode
from Cookie import SimpleCookie


def tuplify(thing):
    if type(thing)==tuple:
        return thing
    return (thing,)
def _tupleMerge(head, tail):
    return tuplify(head)+tuplify(tail)


class RequestData(dict):
    """
    a dict-like object to represent form contents or a query string
    """
    def __init__(self, string):
        self.string = string
        self.type = "application/x-www-form-urlencoded"
        for k,v in self._splitPairs(string).items():
            self[k]=v
    def _splitPairs(self, what, splitter="&", decode=1):
        res = {}
        for pair in what.split(splitter):
            if decode:
                pair = urlDecode(pair)
            l = pair.split("=", 1)
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ''
            if res.has_key(k):
                res[k] = _tupleMerge(res[k], v)
            else:
                res[k]=v
        return res

import os, sys
class RequestBuilder(object):
    """
    should only be used for CGI and testing
    """
    def build(self, method=None, querystring=None, form=None, cookie=None,
              content=None, remoteAddress=None):
        if content and not method: method = "POST"
        return Request(
            method= method or os.environ.get("REQUEST_METHOD", "GET"),
            query=RequestData(querystring
                              or os.environ.get("QUERY_STRING", "")),
            form=form,
            cookie=SimpleCookie(cookie or os.environ.get("HTTP_COOKIE", "")),
            content=content or self.fetchContent(),
            remoteAddress = remoteAddress or "unknownhost")
    def fetchContent(self):
        return sys.stdin.read(int(os.environ.get("CONTENT_LENGTH",0)))


class Request(object):
    """
    A read-only dictionary that represents an HTTP reqeust
    """
    def __init__(self, method, query, form, cookie, content, remoteAddress):
        self.method = method
        self.query = query
        self.cookie = cookie
        self.form = form or RequestData(content or "")
        self.content = getattr(self.form, "string", "")
        self.remoteAddress = remoteAddress

    def __getitem__(self, key):
        res = None
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                if res is None:
                    res = dict[key]
                else:
                    res = _tupleMerge(res, dict[key])
        if res is None:
            raise KeyError, key
        return res

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

