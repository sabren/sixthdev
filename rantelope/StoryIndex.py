
import ransacker
from rantelope import Story

class StoryIndex(ransacker.SQLiteIndex):

    def __init__(self, clerk, filename):
        self.clerk = clerk
        super(StoryIndex, self).__init__(filename)

    def addStory(self, story):
        if story.title or story.description:
            self.addDocument(story, story.title + " " + story.description)
        else:
            # @TODO: this store a blank code is a kludge
            # I'm doing it because by removing the REPLACE INTO
            # for registerPage, _doIndexing  calls commit()
            # even though nothing has been done yet, which
            # causes a crash.
            self.addDocument(story, "_")

    def _registerPage(self, story):
        assert story.ID, "must have an ID"                
        
    def _getPageID(self, story):
        return story.ID
    
    def score(self, word):
        sql =(
            """
            SELECT pageID, count
            FROM idx_freq f, idx_word w
            WHERE f.wordID=w.ID and w.word='%s'
            ORDER BY count DESC
            """ % self._esc(word))
        self.cur.execute(sql)
        return tuple([ (self.clerk.fetch(Story, ID) ,count)
                       for ID, count in self.cur.fetchall()])


    def search(self, query):
        #@TODO: strongboxen need to be hashable!
        matchIDs = {}
        for term in query.split():
            if not term.strip(): continue
            for story,score in self.score(term):
                matchIDs.setdefault(story.ID, 0)
                matchIDs[story.ID] += score

        matchIDs = matchIDs.items()
        matchIDs.sort(lambda a,b: cmp(a[1],b[1]))
        return [self.clerk.fetch(Story, ID) for ID,score in matchIDs]
    
