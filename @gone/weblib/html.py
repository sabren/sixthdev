"""
weblib.html - a utility module to help create html forms.
"""

_isReadOnly_ = 0 # yay! everyone loves global variable!

##[ HTML form elements ]################################

def textarea(name, value, cols, rows):
    '''
    An html TextArea tag
    '''
    return '<textarea name="%s" cols="%i" rows="%i" ' \
           'name="comments">%s</textarea><br>' \
           % (name, cols, rows, weblib.htmlEncode(weblib.deNone(value)))


def checkbox(name, isChecked):
    '''
    An html checkbox. Also adds a hidden __expect__ variable
    since the browser doesn\'t often send unchecked checkboxes.
    '''
    return '<input type="hidden" name="__expect__" value="%s;0">' \
           '<input type="checkbox" value="1" name="%s"%s>' \
           % (name, name, ['','CHECKED'][isChecked])

def text(name, value, width=None, size=None, maxlength=None,
         readonly=None, attrs=''):
    '''
    Returns the HTML code for a text INPUT tag.
    '''
    global _isReadOnly_
    readonly = _isReadOnly_
    if readonly:
        res = value
    else:
        #@TODO: should be a global way of turning off None, right?
        res = '<input type="text" name="%s" value="%s"' \
              % (name, weblib.deNone(value))
        if size:
            res = res + ' size="%i"' % size
        if maxlength:
            res = res + ' maxlength="%i"' % size
        res = res + '>'
    return res

def hidden(name, value=None, attrs=''):
    '''
    Returns HTML code for a hidden input tag.
    '''
    return '<input type="hidden" name="%s" value="%s">' \
           % (name, weblib.deNone(value))


def select(name, value, options, attrs=''):
    '''
    returns HTML for a select box.
    opttions is a sequence of (key/value) sequences..
    attrs is extra HTML to add to the thing..
    '''
    res = '<select name="%s"%s>' % (name, attrs)
    for option in  options:
        res = res + '<option value="%s"' % option[0]
        if option[0] == value:
            res = res +  'SELECTED'
        res = res + '>%s</option>' % option[1]
    return res + '</select>'


