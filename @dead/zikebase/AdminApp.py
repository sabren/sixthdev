"""
AdminApp - base class for apps that want to let you edit zdc.RecordObjects

dispatches the following actions: list, show, edit, make, kill

example: to let you list and edit Widgets:

- define a 'lst_widget.zb' zebra file with the html to list widgets
- define a 'dsp_widget.zb' zebra file with the html to show a single widget
- define a 'frm_widget.zb' zebra file with the form to add/edit a single widget
- define the widget adminapp, like so:

class WidgetAdminApp(AdminApp):

    def list_widget(self):
        view = zdc.select(Widget)
        self.generic_list(view, 'lst_widget')
        
    def show_widget(self):
        self.generic_show(Widget, 'dsp_widget')

    def edit_widget(self):
        # edit is really just show with a different html view
        self.generic_show(Widget, 'frm_widget')
        
    def make_widget(self):
        # make is just edit with a new widget (no ID in url)
        self.generic_make(Widget, 'frm_widget')

    def save_widget(self):
        self.generic_create(Widget, 'frm_widget')

    # no kill_widget, so user can't delete...


"""
__ver__="$Id$"

import weblib
import zdc
import zebra

class AdminApp(weblib.Actor):
    __super = weblib.Actor

    def __init__(self, dbc, input):
        self.__super.__init__(self, input)
        self.dbc = dbc

    ## list ###################################################
    
    def act_list(self):
        self._dispatch("list")

    def generic_list(self, listOfDicts, template):
        self.model["list"] = listOfDicts
        self._runZebra(template)
        

    ## show/edit/make ###############################################

    def act_show(self):
        self._dispatch("show")

    def act_edit(self):
        self._dispatch("edit")

    def act_make(self):
        self._dispatch("make")

    def generic_show(self, klass, template):
        self._showObject(klass(self.dbc, ID=self.input.get("ID")), template)

    def generic_make(self, klass, template):
        self._showObject(klass(self.dbc), template)

    ## delete ######################################################
            
    def act_kill(self):
        self._dispatch("kill")

    def generic_kill(self, klass, nextAction):
        self._objectEdit(klass, "delete")
        self.redirect(action=nextAction)


    ## save ########################################################

    def act_save(self):
        self._dispatch("save")

    def generic_save(self, klass):
        self._objectEdit(klass, "save")


    ###[ private methods ]###########################################

    def _dispatch(self, action):
        what = self.input.get("what", "")
        meth = getattr(self, "%s_%s" % (action, what), None)
        if meth:
            meth()
        else:
            self.complain("don't know how to list %s" % what)


    def _runZebra(self, template):
        try:
            print >> self, zebra.fetch(template, self.model)
        except IOError:
            self.complain("unable to load %s.zb" % template)


    def _showObject(self, obj, template):
        self.consult(zdc.ObjectView(obj))
        self.consult(self.input) # so we can pre-populate via url
        self._runZebra(template)

    def _objectEdit(self, klass, command):
        import zikebase
        ed = zikebase.ObjectEditor(
                 klass, self.dbc, self.input, self.input.get("ID"))
        ed.do(command)
        #@TODO: delete this!
        if command == "delete":
            self.objectID = None
        else:
            self.objectID=ed.object.ID
