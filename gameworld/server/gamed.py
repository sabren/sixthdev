#!/usr/bin/twistd -ny

from twisted.application import service, internet
from twisted.internet import protocol, reactor
from twisted.protocols import basic
from gameworld import Map, Avatar, Actor, Game
from gameworld.event import Moved

def renderANSI(map):
    res = ["\033[H\033[2J"] # clear screen]
    for y in range(10):
        for x in range(10):
            if map.isOccupied((x,y)):
                res.append("x")
            else:
                res.append(".")
        res.append("\n")
    return "".join(res)
            

class BaseGameWorldProtocol(basic.LineReceiver):

    def connectionMade(self):
        self.factory.service.clients.append(self)
        self.avatar = Avatar()
        self.factory.service.game.spawn(self.avatar, (5,5))
        
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        self.factory.map.remove(self.avatar)


class AnsiGameWorldProtocol(BaseGameWorldProtocol):

    def lineReceived(self, data):
        for ch in data:
            if ch == "q":
                self.transport.loseConnection()
            elif ch=="n":
                self.avatar.walk(Map.NORTH)
            elif ch=="s":
                self.avatar.walk(Map.SOUTH)
            elif ch=="e":
                self.avatar.walk(Map.EAST)
            elif ch=="w":
                self.avatar.walk(Map.WEST)

    def on_notify(self, source, event):
        if event == Moved:
            self.transport.write(self.factory.getAnsiMap())


class FlashGameWorldProtocol(BaseGameWorldProtocol):


    def on_notify(self, source, event):
        if event == Moved:
            self.transport.write('<move av="0" x="%s" y="%s"/>\0'
                                 % (source.x, source.y))

            
class GameWorldService(service.Service):

    def __init__(self):
        self.clients = []
        self.game = Game()
        self.mob = Actor("eeeeeeewwwwwww")
        self.game.place(self.mob, (1,1))
        self.game.register(self.on_notify)
        reactor.callLater(1, self.tick)
    def tick(self):        
        self.mob.cue()
        reactor.callLater(0.5, self.tick)
    def on_notify(self, source, event):        
        self.ansiMap = renderANSI(self.game.map)
        #@TODO: clients should register directly with world
        for c in self.clients:
            c.on_notify(source, event)

    def getAnsiMap(self):
        return self.ansiMap
    def getAnsiFactory(self):
        f = protocol.ServerFactory()
        f.protocol = AnsiGameWorldProtocol
        f.service = self
        f.getAnsiMap = self.getAnsiMap
        return f

# run this thing on port 6000
application = service.Application('gameworld')
gws = GameWorldService()
tcp1 = internet.TCPServer(6000, gws.getAnsiFactory())
tcp1.setServiceParent(service.IServiceCollection(application))
#tcp2 = internet.TCPServer(6100, gws.getFlashFactory()))
#tcp2.setServiceParent(service.IServiceCollection(application))
