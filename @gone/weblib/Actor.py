"""
A base class for web pages that act differently based on a parameter.
"""
__ver__ = "$Id$"

#@TODO: subclass that uses Signature to pass values to act_XXX?

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

        # jumpMap is a special variable that tells you where
        # you can jump. It's basically a way to let you
        # redirect pages as you see fit via act_jump
        # without letting anyone use your page to redirect
        # things arbitrarily..
        self.jumpMap = {}
        
        self.action = None
        self.next = None
        self.model = {}
        self.model.update(self.input)


    ## public methods ############################################

    def enter(self):
        """Override this with stuff to do before acting. called by act()."""
        pass


    def exit(self):
        """Override this with stuff to do after acting. called by exit()."""
        pass
    

    def act(self, action=None):
        """ex: actor.act();   actor.act("jump")"""

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
        self.input.update(params)

        self.perform(action)
            

    def perform(self, action=None):
        oldaction = self.action
        if action is not None:
            self.action = action
            
        if type(self.action) == type(()):
            raise TypeError, 'Multiple actions requested: %s' \
                  % str(self.action)

        method = getattr(self, "act_" + self.action, self.act__error__)
        method() # hey! method acting! :)
        self.action = oldaction


    def complain(self, problem):
        raise Error, problem


    ## actions ###################################################

    def act_(self):
        """Default action. Does nothing, but you can override it."""
        pass

    def act_jump(self):
        import weblib
        weblib.response.redirect(self.jumpMap[self.input["where"]])

    def act__error__(self):
        self.complain("don't know how to %s" % self.action)
