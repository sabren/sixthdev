"""
A base class for web pages that act differently based on a parameter.
"""
__ver__ = "$Id$"

#@TODO: subclass that uses Signature to pass values to act_XXX?

class App(object):
    """
    App(input) where input=a dict, usually with a key called 'action'.
    
    This class is designed to make it easy to write classes that can
    be called directly through a URL. It's just a base class, and only
    provides enough logic to handle dispatching actions right now.    
    
    The input dict should have a key called "action" that will tell the
    actor what to do. The App subclass must have a method caled act_XXX
    where XXX is whatever "action" mapped to.
    """

    ##@TODO: a generic nextMap for action chains might come in handy,
    ## and keep people from having to override every little method.

    ## constructor ################################################

    def __init__(self, input):
        self.debug = 0 # alters behavior of complain()

        self._copyinput(input)

        # out is just a buffer:
        import cStringIO
        self.out = cStringIO.StringIO()

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

    def _copyinput(self, input):
        self.input = {} # so we can call do() with extra params
        try:
            for k in input.keys():
                self.input[k] = input[k]
        except AttributeError, e:
            raise "invalid input: %s" % `input`
            


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
        returns output buffer built by calls to write()

        ## @TODO: clean up this whole 'next' concept..
        ## looks like it was set up to tell the client to
        ## reinvoke act(). But it's basically a giant,
        ## nasty GOTO feature and must be killed!
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
                raise TypeError, "next should not be... %s" % `next`
        self.exit()
        return self.out.getvalue()


    def do(self, action, input=None, **params):
        """
        like act(), but doesn't do enter/exit stuff..
        handy if you want an action to call another action
        """
        if input is not None:
            self._copyinput(input)
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
        if type(problems)==type(""):
            probs = [problems]
        else:
            probs = problems
        for prob in probs:
            self.errors.append(prob)
            self.model["errors"].append({"error":prob})
            if self.debug:
                print "\n::>ERROR<::", prob

    def consult(self, model):
        """
        updates the App's internal model based on the
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


    def redirect(self, url=None, action=None):
        """
        Sets self.next and throws weblib.Redirect
        """
        if not ((url is not None) ^ (action is not None)):
            raise TypeError, "syntax: actor.redirect(url XOR action)"
        if url:
            where=url
            self.next = None
        else:
            #@TODO: why __weblib_ignore_form__ again?
            where="?action=%s&__weblib_ignore_form__=1" % (action)
            self.next = action
        import weblib
        raise weblib.Redirect, where


    def map_where(self, where):
        """
        Given a shortname, returns a url. Used to prevent
        people from redirecting randomly through pages.

        Returns None if no URL found.
        """
        return self.where.get(where)


    def write(self, what):
        """
        write something to output..
        """
        self.out.write(what)


    ## actions ###################################################

    def act_(self):
        """
        Default action. Does nothing, but you can override it.
        """
        pass

    def act__error__(self):
        """
        This gets called when an unknown action is requested.
        """
        self.complain("don't know how to %s" % self.action)
