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
from rantelope import *


class RantelopeApp(sixthday.AdminApp):

    def __init__(self, clerk, input, user):
        super(RantelopeApp, self).__init__(clerk, input)
        self.user = user

        
    def act_(self):
        self.list_channel()
        

    ## authors #########################

    def list_author(self):
        authors = [BoxView(a) for a in self.clerk.match(Author)]
        self.generic_list(authors, "lst_author")

    def create_author(self):
        self.generic_create(Author, "frm_author")

    def edit_author(self):
        self.generic_show(Author, "frm_author")

    def save_author(self):
        a = self._getInstance(Author)
        if self.input.get("password"):
            a.password = self.input["password"]
        self.clerk.store(a)
        self.redirect(action="list&what=author")


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
        return chan

    def create_story(self):
        c = self.studyChannel(self.input.get("channelID"))
        self.model["siteurl"] = c.url        
        self.generic_create(Story, "frm_story")
        
    def edit_story(self):
        s = self.clerk.fetch(Story, self.input["ID"])
        c = self.studyChannel(s.channelID)
        self.model["siteurl"] = c.url
        self.model["stories"] = []
        self.generic_show(Story, "frm_story")

    def save_story(self):
        ## first save to database:
        story = self._getInstance(Story)
        if not story.author:
            story.author = self.user
        self.clerk.store(story)

        ## go back to the channel:
        self.redirect(action='create&what=story&channelID='
                            + str(story.channelID))        
        
    def show_story(self):
        self.generic_show(Story, "sho_story")

    ## comments ########################
        
    def save_comment(self):
        cmt = self.generic_save(Comment)
        self.redirect(action='show&what=story&ID='
                      + str(cmt.storyID))


    ## publishing ######################
        
    def act_publish(self):
        ## now write the XML file:
        chan=self.clerk.fetch(Channel, self.input["channelID"])
        chan.writeFiles()
        self.redirect(action="create&what=story&status=published&channelID="
                      + self.input["channelID"])


### main code #######################################

if __name__=="__main__":

    from sqlRantelope import clerk, dbc
    ENG.do_on_exit(dbc.close)
    
    from AuthorAuth import AuthorAuth
    from weblib import Sess, SessPool
    sess = Sess(SessPool.SqlSessPool(dbc), REQ, RES)
    sess.start()
    ENG.do_on_exit(sess.stop)

    auth = AuthorAuth(sess, clerk)
    auth.check()
    
    print >> RES, RantelopeApp(clerk, REQ, auth.user).act()
