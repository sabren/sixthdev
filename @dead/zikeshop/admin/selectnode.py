# this is a major kludge just to get the product page running..
# @TODO: figure out why this is so hard..
#@TODO: why can't I use ]'s in zebra??? XML?
import weblib.html

def selectnode(name, values=None, blank=None, attrs=None):
    # is this a mess or what?    
    from  mdl_category import model
    if type(values) != type([]):
        values = [values]
    values = map(str, values)
    hack = lambda c, ids=values: (c['ID'], c['path'], str(c['ID']) in ids)
    opts = map(hack, model['categories'])
    if blank is not None:
        opts = [(blank, '', values == [None])] + opts
    return weblib.html.select(name, opts, attrs=attrs)
