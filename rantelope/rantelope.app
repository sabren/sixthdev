"""
Rantelope!
(c)2002-2003 Sabren Enterprises, Inc.
This program is free software,
licensed under the GNU GPL.
"""
__ver__="$Id$"

from Node import Node
from strongbox import *
import sixthday
import zebra
from schema import *                


class RantelopeApp(sixthday.AdminApp):

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
        chan = self.clerk.fetch(Channel, long(self.input["ID"]))
        model = {"errors":[]}
        model.update(BoxView(chan))
        print >> self, zebra.fetch("sho_channel", model)


    def save_channel(self):
        chan = self.generic_save(Channel)
        chan.writeFiles()
        self.redirect(action='show&what=channel&ID=%s' % chan.ID)

    ## categories ######################

    def save_category(self):
        cat = self.generic_save(Category)
        self.redirect(action='show&what=channel&ID=%s' % cat.channelID)

    def edit_category(self):
        self.generic_show(Category, "frm_category")
    

    ## stories #########################

    def studyChannel(self, channelID):
        assert channelID, "must supply valid channelID"
        chan = self.clerk.fetch(Channel, channelID)
        self.model["categories"] = [(c.ID, c.name) for c in chan.categories]
        # @TODO: will need to limit number of past stories soon.
        self.model["stories"] = [BoxView(s) for s in chan.stories]

    def create_story(self):
        self.studyChannel(self.input.get("channelID"))
        self.generic_create(Story, "frm_story")
        
    def edit_story(self):
        s = self.clerk.fetch(Story, self.input["ID"])
        self.studyChannel(s.channelID)
        self.generic_show(Story, "frm_story")

    def save_story(self):
        ## first save to database:
        story = self.generic_save(Story)

        ## now write the XML file:
        chan=self.clerk.fetch(Channel, self.input["channelID"])
        chan.writeFiles()

        ## go back to the channel:
        self.redirect(action='create&what=story&channelID='
                            + str(chan.ID))
        
    def show_story(self):
        self.generic_show(Story, "sho_story")

    ## comments ########################
        
    def save_comment(self):
        cmt = self.generic_save(Comment)
        self.redirect(action='show&what=story&ID='
                            + str(cmt.storyID))


### main code #######################################

if __name__=="__main__":
    from sqlRantelope import clerk   
    print >> RES, RantelopeApp(clerk, REQ).act()

