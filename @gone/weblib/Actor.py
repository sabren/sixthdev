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
                self.input = weblib.request
            else:
                self.input = {}


    ## public methods ############################################

    def enter(self):
        """Override this with stuff to do before acting. called by act()."""
        pass


    def exit(self):
        """Override this with stuff to do after acting. called by exit()."""
        pass
    

    def act(self, action=None):
        """ex: actor.act();   actor.act("jump")"""
        self.enter()

        if action is not None:
            toDo = action
        else:
            toDo = self.input.get("action", "")
        
        method = "act_" + toDo
        apply(getattr(self, method), ())

        self.exit()


    ## actions ###################################################

    def act_(self):
        """Default action. Does nothing, but you can override it."""
        pass
