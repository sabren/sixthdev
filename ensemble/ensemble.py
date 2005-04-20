"""
ensemble: load perl/ruby/whatever modules from python
"""
import os, sys, imp, new, xmlrpclib, pexpect
from xmlrpclib import Transport, ServerProxy, Fault, Binary

BANNER = "## ensemble v1.0 ##"

##################################################

class EnsembleTransport(Transport):
    """
    I'm a helper class that talks to the child processes.
    """
    def __init__(self, child):
        self.child = child

    def request(self, host, handler, request_body, verbose=0):
        xml = "<methodResponse>.*</methodResponse>"
        try:
            self.child.send(request_body)
            self.child.expect(xml)
            response = self.child.after
        except:
            raise Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value))
        else:
            if isinstance(response, Fault):
                raise response
            else:
                r = xmlrpclib.loads(response)[0]
                if isinstance(r[0], Binary):
                    return r[0].data
                else:
                    return r


##################################################

class Director(ServerProxy):
    """
    I'm the top-level object you create to talk
    to child processes.
    """
    def __init__(self, child_command):
        self.transport = EnsembleTransport(self.connect(child_command))
        ServerProxy.__init__(self, "http://ensemble/", # just to avoid error
                             transport=self.transport)

    def connect(self, child_command):
        child = pexpect.spawn(child_command)
        child.expect(BANNER)
        return child


##################################################

class ChildService:
    """
    I am the main code for the child process.
    """
    def __init__(self):
        self.code = new.module("-ensemble-")
        self.code.loadModule = self.loadModule

    def loadModule(self, modname, asname=None):
        _as = asname or modname
        setattr(self.code, _as,
                imp.load_module(modname, *imp.find_module(modname)))
        return True

    def invoke(self, method, params):
        f = self.code
        for item in method.split("."):
            f = getattr(f, item)
        return f(*params)

    def xml_invoke(self, req):
        params, method = xmlrpclib.loads(req)
        try:
            res = (self.invoke(method, params), )
        except:
            res = Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value))
        return xmlrpclib.dumps(res, methodresponse=1)
    
    def run(self):
        sys.stdout.write(BANNER + "\n")
        sys.stdout.flush()
        while True:
            req = ""
            while not req.count("</methodCall>"):
                req += sys.stdin.readline()
            sys.stdout.write(self.xml_invoke(req))
            sys.stdout.flush()

##################################################

if __name__=="__main__":
    ChildService().run()
