#! /usr/bin/python
"""
simple twisted server
"""

import sys
import os

from twisted.python import log
from twisted.python import failure

from twisted.internet.app import Application
from twisted.internet import threads

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.web import static
from twisted.web import util

from weblib import Engine, Response


#log.startLogging(sys.stdout, 1)

class TwistedCookieWrapper(object):
    def __init__(self, request):
        self.request = request

    def __getitem__(self, name):       
        return self.request.getCookie(name)

    def __setitem__(self, name, value):
        self.request.setCookie(name, value)


from UserDict import UserDict
class TwistedRequestWrapper(UserDict):
    def __init__(self, request):
        self.data = request.args
        self.request = request
        self.environ = {}
        self.cookie = TwistedCookieWrapper(request)
        self.query = self

    def get(self, name, default=None):
        rv = self.request.args.get(name, default)
        if rv is not None:
            if type(rv)==list:
                return rv[0]
            return tuple(rv)

    def __len__(self):
        return len(self.request.args)

    def __getitem__(self, name):
        rv = self.request.args[name]
        if type(rv)==list:
            return rv[0]
        return tuple(rv)


class TwistedResponse(Response):
    def __init__(self, request):
        super(TwistedResponse,self).__init__()
        self.request = request

    def redirect(self, url):
        self.request.redirect(url)


class TwistedEngine(Engine):
    def __init__(self, path, request):
        super(TwistedEngine, self).__init__(
            open(path).read(), TwistedRequestWrapper(request))
        self.path = path
        self.twistedRequest = request

    def getScriptName(self):
        return self.path


    def makeResponse(self):
        return TwistedResponse(self.twistedRequest)



class RantResource(Resource):
    isLeaf = 1
    def __init__(self, path, registry):
        self.path = path
        self.registry = registry

    def render(self, request):
        import pdb; pdb.set_trace()
        return self._thread(request)
        #d = threads.deferToThread(self._thread, request)
        #d.addCallback(self._finish, request)
        #return NOT_DONE_YET

    def _finish(self, result, request):
        request.write(result)
        request.finish()

    def _thread(self, request):
        e = TwistedEngine(path=self.path, request=request)
        e.start()
        e.setDir(os.path.split(self.path)[0])
        e.injectParts()
        e.runDotWeblibPy()
        #import pdb; pdb.set_trace()
        e.runScript()        
        if e.result in (e.SUCCESS, e.EXIT):
            for k,v in e.response.headers: # @TODO: encapsulate me!
                request.setHeader(k,v)
            return e.response.buffer
        elif e.result == e.FAILURE:
            # assertion failure:
            return str(e.error)
        elif e.result == e.EXCEPTION:
            request.setHeader('content-type', "text/plain")
            return e.error
            #return util.formatFailure(failure.Failure(e.exception))
        else:
            raise Exception("should never get here: unknown Engine.result:%s" % e.result)


application = Application("rantserver")
fl = static.File('/home/pair/lib/')
fl.processors = {'.app': RantResource, '.py': RantResource}
application.listenTCP(8109, Site(fl),
                      )#interface="65.61.166.185",)
