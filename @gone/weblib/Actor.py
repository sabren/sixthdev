"""
A base class for web pages that act differently based on a parameter.
"""
__ver__ = "$Id$"

#@TODO: subclass that uses Signature to pass values to act_XXX?
import weblib

class Actor:
    """
    Actor(input) #input=None or a dict with a key called 'action'.
    
    This class is designed to make it easy to write classes that can
    be called directly through a URL. It's just a base class, and only
    provides enough logic to handle dispatching actions right now.    
    
    The input dict should have a key called "action" that will tell the
    actor what to do. The Actor subclass must have a method caled act_XXX
    where XXX is whatever "action" mapped to.
    
    If input is None, it will use weblib.sess, or an empty dict if weblib.sess
    isn't defined.
    """

    ##@TODO: a generic nextMap for action chains might come in handy,
    ## and keep people from having to override every little method.

    ## constructor ################################################

    def __init__(self, input=None):
        if input is not None:
            self.input = input
        else:
            import weblib
            if hasattr(weblib, "request"):
                self.input = {}
                # this is so we can do self.input[xx]=yy
                for key in weblib.request.keys():
                    # .update doesn't work with non-dicts
                    self.input[key] = weblib.request[key]
                    
            else:
                self.input = {}

        # where is a special variable that tells you where
        # you can jump. It's basically a way to let you
        # redirect pages as you see fit via act_jump
        # without letting anyone use your page to redirect
        # things arbitrarily..
        self.where = {}
        
        self.action = None
        self.next = None
        self.errors = []
        self.model = {"errors":[]}
        for key in self.input.keys():
            self.model[key] = self.input[key]


    ## public methods ############################################

    def enter(self):
        """
        Override this with stuff to do before acting. called by act().
        """
        pass


    def exit(self):
        """
        Override this with stuff to do after acting. called by exit().
        """
        pass
    

    def act(self, action=None):
        """
        ex: actor.act();   actor.act('jump')
        """

        if action is not None:
            self.action = action
        else:
            self.action = self.input.get("action", "")

        self.enter()
        self.next=self.action
        while self.next is not None:
            next = self.next
            self.next = None
            if type(next)==type(""):
                self.do(next)
            else:
                apply(self.do, next)
        self.exit()


    def do(self, action, input=None, **params):
        """
        like act(), but doesn't do enter/exit stuff..
        handy if you want an action to call another action
        """
        if input is not None:
            self.input = input
        for key in params.keys():
            self.input[key]=params[key]

        oldaction = self.action
        if action is not None:
            self.action = action
            
        if type(self.action) == type(()):
            raise TypeError, 'Multiple actions requested: %s' \
                  % str(self.action)

        method = getattr(self, "act_" + self.action, self.act__error__)
        method() # hey! method acting! :)
        self.action = oldaction


    def complain(self, problems):
        """
        Generic error handler. Pass it a string or list of strings.
        """
        if type(problems)=="":
            probs = [problems]
        else:
            probs = problems
        for prob in probs:
            self.errors.append(prob)
            self.model["errors"].append({"error":prob})

    def consult(self, model):
        """
        updates the Actor's internal model based on the
        passed in model. model can be either a module
        name or a dict.

        if it's a module name, the module should contain
        a dict called model.
        """
        # models and modules.... heh... :)
        if type(model) == type(""):
            self.model.update(__import__(model).model)
        else:
            # assume it's a dict of sorts:
            for item in model.keys():
                self.model[item] = model[item]

    #@TODO: this replace (??) act_jump...
    #@TODO: make a test case for this.
    #@TODO: should this INSTANTLY redirect? what about nonbrowsers?
    def redirect(self, url=None, action=None):
        assert ((url is not None) ^ (action is not None)), \
               "syntax: actor.redirect(url XOR action)"
        if url:
            self.where["gohere"]=url
        else:
            self.where["gohere"]="%s?action=%s" % \
                                  (weblib.request.environ["REQUEST_URI"],
                                   action)
        self.next  = ("jump", {"where":"gohere"})


    def map_where(self, where):
        """
        Given a shortname, returns a url. Used to prevent
        people from redirecting randomly through pages.

        Returns None if no URL found.
        """
        return self.where.get(where)


    ## actions ###################################################

    def act_(self):
        """
        Default action. Does nothing, but you can override it.
        """
        pass

    def act_jump(self):
        """
        Jump to one of the urls defined in .where... expects where=xxx
        in input from a browser...
        Alternately, pass in the url from a script.
        """
        import weblib
        where = self.map_where(self.input["where"])
        if where:
            weblib.response.redirect(where)
        else:
            self.complain("'%s' is not a valid jump" % self.input["where"])

    def act__error__(self):
        """
        This gets called when an unknown action is requested.
        """
        self.complain("don't know how to %s" % self.action)
