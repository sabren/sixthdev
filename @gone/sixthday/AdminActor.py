"""
AdminActor - base class for apps that want to let you edit zdc.RecordObjects

dispatches the following actions: list, show, edit, create, delete

example: to let you list and edit Widgets:

- define a 'lst_widget.zb' zebra file with the html to list widgets
- define a 'dsp_widget.zb' zebra file with the html to show a single widget
- define a 'frm_widget.zb' zebra file with the form to add/edit a single widget
- define the widget AdminActor, like so:

class WidgetAdminActor(AdminActor):

    def list_widget(self):
        view = zdc.select(Widget)
        self.generic_list(view, 'lst_widget')
        
    def show_widget(self):
        self.generic_show(Widget, 'dsp_widget')

    def edit_widget(self):
        # edit is really just show with a different html view
        self.generic_show(Widget, 'frm_widget')
        
    def create_widget(self):
        # create is just edit with a new widget (no ID in url)
        self.generic_create(Widget, 'frm_widget')

    def save_widget(self):
        self.generic_create(Widget, 'frm_widget')

    # no delete_widget, so user can't delete...


"""
__ver__="$Id$"

import sixthday
import zdc
import zebra

class AdminActor(sixthday.Actor):

    def __init__(self, dbc, input):
        super(AdminActor, self).__init__(input)
        self.dbc = dbc

    ## list ###################################################
    
    def act_list(self):
        self._dispatch("list")

    def generic_list(self, listOfDicts, template):
        self.model["list"] = listOfDicts
        self._runZebra(template)
        

    ## show/edit/create ###############################################

    def act_show(self):
        self._dispatch("show")

    def act_edit(self):
        self._dispatch("edit")

    def act_create(self):
        self._dispatch("create")

    def generic_show(self, klass, template):
        self._showObject(klass(self.dbc, ID=self.input.get("ID")), template)

    def generic_create(self, klass, template):
        self._showObject(klass(self.dbc), template)

    ## delete  ######################################################
            
    def act_delete(self):
        self._dispatch("delete")

    def generic_delete(self, klass, nextAction):
        self._objectEdit(klass, "delete")
        self.redirect(action=nextAction)


    ## save ########################################################

    def act_save(self):
        self._dispatch("save")

    def generic_save(self, klass):
        return self._objectEdit(klass, "save")


    ###[ private methods ]###########################################

    def _dispatch(self, action):
        what = self.input.get("what", "")
        meth = getattr(self, "%s_%s" % (action, what), None)
        if meth:
            meth()
        else:
            self.complain("don't know how to %s %s" % (action, what))


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
        ed = sixthday.ObjectEditor(
            klass, self.dbc, self.input, self.input.get("ID"))
        ed.do(command)
        return ed.object
