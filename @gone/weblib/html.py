"""
weblib.html - a utility module to help create html forms.
"""
__ver__="$Id$"

import weblib

#@TODO: test cases for each and every one of these punks..

##[ HTML form elements ]################################

def textarea(name, value, attrs=''):
    '''
    An html TextArea tag
    '''
    return '<textarea name="%s"%s>%s</textarea>' \
           % (name, attrs, weblib.htmlEncode(weblib.deNone(value)))

def checkbox(name, isChecked, onValue=1, offValue=0, attrs=''):
    '''
    An html checkbox. Also adds a hidden __expect__ variable
    since the browser doesn\'t often send unchecked checkboxes.
    '''
    return '<input type="hidden" name="__expect__" value="%s:%s">' \
           '<input type="checkbox" name="%s" %s %s value="%s">' \
           % (name, offValue, name, attrs, ['','CHECKED'][isChecked], onValue)

def radio(name, isChecked, value=1, attrs=''):
    '''
    An html radio button. 
    '''
    return '<input type="radio" name="%s" %s %s value="%s">' \
           % (name, attrs, ['','CHECKED'][isChecked], value)

def text(name, value, attrs=''):
    '''
    Returns the HTML code for a text INPUT tag.
    '''
    return '<input type="text" name="%s" %s value="%s">' \
           % (name, attrs, weblib.deNone(value))

def hidden(name, value, attrs=''):
    '''
    Returns HTML code for a hidden input tag.
    '''
    return '<input type="hidden" name="%s" %s value="%s">' \
           % (name, attrs, weblib.deNone(value))


def select(name, options, value=None, attrs=''):
    '''
    returns HTML for a select box.
    options is either:
        a sequence of keys (if keys and values are the same)
        a sequence of (key/value) sequences..
    value is either a key or list of keys (can be [])
    attrs is extra HTML to add to the thing..
    '''

    ## make sure vals is a list
    if type(value)!=type([]):
        vals = [value]
    else:
        vals = value

    ## expand options into a X*3 grid (if it's not):
    opts = []
    if options:
        # if options is a sequence of sequences:
        if type(options[0]) in (type([]), type(())):
            case = len(options[0])
            ## if options is a list of 3-tuples:
            if case == 3:
                ## leave it as is, ignore values
                opts = options
            ## elif options is a list of 2-tuples:
            elif case == 2:
                ## loop through and add isChecked
                for item in options:
                    opts.append(list(item) + [(item[0] in vals)])
            else:
                raise TypeError, \
                      "Invalid option structure passed to html.select()!"
        ## else options is a list of keys:
        else:
            ## loop through and add make it [key key isChecked]
            for item in options:
                opts.append([item, item, (item in vals)])
    else:
        pass # kinda silly to want no options, but no point crashing.

    ## now that we have an X*3 grid, show the box:
    res = '<select name="%s" %s>' % (name, attrs)
    for option in  opts:
        res = res + '<option value="%s"' % option[0]
        if option[2]:
            res = res +  'SELECTED'
        res = res + '>%s</option>' % option[1]
    return res + '</select>'

