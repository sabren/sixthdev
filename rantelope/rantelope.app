"""
Rantelope!
(c)2002 Sabren Enterprises, Inc.
This program is free software,
licensed under the GNU GPL.
"""
__ver__="$Id$"

### object model ####################################

from strongbox import *
import zebra

class Story(Strongbox):
    ID = attr(long)
    channelID = attr(long)
    title = attr(str)
    link = attr(str)
    description = attr(str)
    
class Channel(Strongbox):
    ID = attr(long)
    title = attr(str)
    link = attr(str)
    description = attr(str)
    rssfile = attr(str, okay=lambda x: "/" not in x and x.endswith(".rss"))
    stories = linkset(Story)

    def writeRSS(self):
        RSS = open(self.rssfile, "w")
        print >> RSS, zebra.fetch("rss", BoxView(self))


### interface #######################################

import sixthday

class RantelApp(sixthday.AdminApp):

    def act_(self):
        self.list_channel()

    ## channels ########################

    def list_channel(self):
        channels = [BoxView(c) for c in self.clerk.match(Channel)]
        self.generic_list(channels, "lst_channel")

    def create_channel(self):
        self.generic_create(Channel, "frm_channel")
        
    def edit_channel(self):
        self.generic_show(Channel, "frm_channel")

    def show_channel(self):
        self.generic_show(Channel, "sho_channel")

    def save_channel(self):
        self.generic_save(Channel)
        self.redirect(action='list&what=channel')

    ## stories #########################

    def create_story(self):
        assert self.input["channelID"], "must supply channelID"
        self.generic_create(Story, "frm_story")
        
    def edit_story(self):
        self.generic_show(Story, "frm_story")

    def save_story(self):
        ## first save to database:
        story = self.generic_save(Story)

        ## now write the XML file:
        chan=self.clerk.fetch(Channel, self.input["channelID"])
        chan.writeRSS()

        ## go back to the channel:
        self.redirect(action='show&what=channel&ID='
                            + str(story.channelID))
        


### main code #######################################

if __name__=="__main__":

    import arlo, storage, sqlRantelope
    dbmap = {Channel: "rnt_channel",
             Channel.__attrs__["stories"]: (Story, "channelID"),
             Story: "rnt_story" }
    CLERK = arlo.Clerk(storage.MySQLStorage(sqlRantelope.dbc), dbmap)
    
    ## now just run the app!
    print >> RES, RantelApp(CLERK, REQ).act()

