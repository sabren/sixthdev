
# simple app to show rantelope blogs

from sqlRantelope import clerk
from rantelope import Channel

chan = clerk.fetch(Channel, REQ.get("channelID", 1))

if REQ.get("as") =="xml":
    RES.contentType="text/xml"
    print >> RES, chan.toRSS()
else:
    print >> RES, chan.toHTML()
