"""
Wizard class for the web..
"""
import zikeshop

class Wizard(zikeshop.ShopActor):

    steps = []

    def showPage(self, page):
        exec("import %s" % self.fieldPages[page])
        exec("%s.show(self.get_model())" % self.fieldPages[page])

    def nextStep(self):
        """Figure out what more we need to do, and do it."""

        """
        @TODO: 0923.2000 - plan for new Wizard class

        I think it would be cool if we had a default flow through
        the pages, and also allow that to be overridden... Maybe
        there ought to be something like:

        self.steps = dict_mapping_steps_to_next_steps # or maybe a list
        self.next = self.steps[self.thisStep]
        self.do_this_step()
        # above line has opportunity to alter self.next...
        self.do_next_step()
        """

        ## first, if we need more info, ask for it:
        for item in self.steps:
            # check has and get so that we can assign items
            # before calling act() (as we do in zikeshop/public/newaddress.py)
            if getattr(self, item, None) is None:
                if self.fieldPages.get(item):
                    self.showPage(item)
                else:
                    raise "don't know how to get %s" % item
                break
        

    def act_(self):
        """If we don't have something better to do, just show the next step"""
        self.nextStep()


