#! /usr/bin/python
"""
simple twisted server
"""

from twisted.web.server import Site
from twisted.internet.app import Application
from twisted.web.resource import Resource

class RantResource(Resource):
    isLeaf = 1
    def render(self, request):
        return "RantResource"

application = Application("rantserver")
application.listenTCP(8109, Site(RantResource()),
                      )#interface="65.61.166.185",)

if __name__=='__main__':
    application.run()
