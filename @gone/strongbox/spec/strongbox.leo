<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="16" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="10" left="10" height="624" width="768"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0" tab_width="8" page_width="132" tangle_bat="0" untangle_bat="0" output_doc_chunks="0" defaultTargetLanguage="Python" use_header_flag="0">
	<defaultDirectory>w:/strongbox/spec</defaultDirectory>
</preferences>
<find_panel_settings wrap="1" search_body="1">
	<find_string>dbc</find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1" a="E"><vh>strongbox module overview</vh></v>
<v t="T2"><vh>Persistence</vh></v>
<v t="T3" a="E"><vh>Replacing zdc</vh></v>
<v t="T4" a="E"><vh>@file StrongboxTest.py</vh>
<v t="T5" a="E"><vh>Strongbox uses metaclasses to provide its magic</vh></v>
<v t="T6" a="E"><vh>Strongbox attributes are defined as class variables</vh></v>
<v t="T7"><vh>Strongbox turns accessors into properties</vh></v>
<v t="T8"><vh>Private variables are explicitly private</vh></v>
<v t="T9"><vh>Attributes have defaults, but can be initialized via the constructor</vh></v>
<v t="T10"><vh>Without explicit defaults, strings default to '', ints and longs to 0</vh></v>
<v t="T11" a="V"><vh>Other types pass defaults to the constructor</vh></v>
<v t="T12" a="E"><vh>Attributes use static typing</vh></v>
<v t="T13" a="E"><vh>Attributes allow "None" by default</vh></v>
</v>
<v t="T14" a="E"><vh>@file SubjectTest.py</vh>
<v t="T15" a="E"><vh>Observers manage themselves with attach() and detatch()</vh></v>
<v t="T16"><vh>subject.notify() sends messages to all the observers</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="T1">@
Strongbox is a tool for strongly-typed data objects in python.</t>
<t tx="T2">@
Persistence is not actually handled by strongbox. It will be handled
by an outside module, which defines the process of mapping strongboxes to
tables in a relational database (or to some other form of persistence storage).

I'm worried about working with relationships though.

Imagine a simple Team/Player/Sport model:

   Team has players
   Players may be on several teams
   Each team has one sport

Here are the relationships:

   player.teams / team.players (junction)
   sport.teams (simple list)
   team.sport (simple reference)

The question is, if we remove the persistence ability from Strongbox, how
do we get the related objects?

For example:

&gt;&gt;&gt; aTeam = clerk.load(Team, ID=123)
&gt;&gt;&gt; aTeam.sport
???

What is sport? It's a Sport object, of course. But we can't just load dependent
objects all at once, because they could be connected in a huge graph. (Eg, we
load player 1, who's on several teams with multiple players each, and those 
players are on multiple teams, and so on....)  If we loaded dependent objects
as soon as we loaded the main object, we'd wind up with the whole database in
memory. That might be okay for a small database or an app server that stayed up 
for weeks, but it's no good at all in a CGI script.

Instead, we want to load the main object, and only load dependent objects if we
need them.

So in the example above, we don't want aTeam.sport to actually be a sport, but
some object representing a reference to a Sport in the same datastore that 
came from.

class ref(strongbox):
   _class = attr(type)
   _id = attr(long)
   _clerk = attr(object)

so maybe something like this:

class Sport(strongbox):
   pass
class Team(strongbox):
   sport = link(Sport)
class Player(strongbox):
   teams = join(Team)

Sport.teams = join(Team)
Team.players = join(Player)</t>
<t tx="T3">@
how do I go from zdc to strongbox?

- replace dbc with clerk.load() or clerk.new() (except cursors)
- double check by adding a required parameter that only clerk passes
- remove parameter when done testing...

- replace xxx.save() with clerk.save()

- look for dbc.cursor lines and replace with storing to a map


eventually: force load to have a where clause!

save() should be dbc.save(obj), which doesn't exist yet,
but which is probably similar to Recordobject.save....
In any case, we can just make dbc.save call obj.save for
now.

Those are pretty much the only changes we need to make.
It's a lot of them, but it shouldn't be too hard. (Actually,
it'll probably mostly be test cases)

This should also localize the need for robj(ds), as it will
always be passed in from dbc.load()

We can also move all the _tablename nonsense, but I guess that can
wait a minute or two, until we start pulling in attributes.

Okay, well... Let's try it.</t>
<t tx="T4">"""
test cases for Strongbox
"""
__ver__="$Id$"

import unittest
import types
from strongbox import Strongbox, attr

class StrongboxTest(unittest.TestCase):

    def setUp(self):
        pass
        
    @others
       
    def tearDown(self):
        pass</t>
<t tx="T5">@
Strongbox is a Metaclass

What's a metaclass? It's a class representing a class.

http://www.python.org/2.2/descrintro.html#metaclasses

For example, in python 2.2, there are old-style
classes and new-style classes. They don't work
exactly the same, but they're both types of classes.

Strongboxes are another type of class, which makes
Strongbox a metaclass. Make sense?

But it should look just like a normal class:
@code

def check_looks_like_a_class(self):
    class X(Strongbox):
        pass
    assert isinstance(X(), Strongbox)</t>
<t tx="T6">@
Attributes must be present in the class definition.

@TODO: maybe a "shared" notion for static variables?
@code

def check_slots(self):
    class Slotmachine(Strongbox):
        a = attr(int, default=1)
        b = attr(int, default=2)
        c = attr(int, default=3)
    xinst = Slotmachine() 
    xinst.a = 1 # should work
    try:
       err = 0
       xinst.d = 4
    except AttributeError:
       err = 1
    assert err, "assigning to nonexistent slot d should have failed."</t>
<t tx="T7">@
Specifically, it should automatically create properties from
methods called get_XXX and set_XXX:
@code

def check_properties(self):
    class X(Strongbox):
        def get_a(self): return 1
        get_b = lambda self: 2
        c = attr(int)
        d = attr(int)
        def set_c(self, value): self.d = 4
    instance = X()
    assert instance.a == 1
    assert instance.b == 2
    instance.c = 3
    assert instance.c == 0 # see check_default_defaults
    assert instance.d == 4, instance.d</t>
<t tx="T8">@
All strongbox instances have a "private" namespace, which
lets them store private variables explicitly. (This is necessary
because self.xxx = yyy would cause an AttributeError if xxx is
not defined up front as an attrbute)
@code 
def check_private(self):
    s = Strongbox()
    assert hasattr(s, "private")
    s.private.c = 1
    assert s.private.c == 1</t>
<t tx="T9">

def check_defaults(self):
    class Foo(Strongbox):
        bar = attr(int, default=5)  
    foo = Foo()
    assert foo.bar ==5

def check_constructor(self):
    class Foo(Strongbox):
        bar = attr(int, default=5)  
    foo = Foo(bar=12)
    assert foo.bar == 12</t>
<t tx="T10">
def check_default_defaults(self):
    class Foo(Strongbox):
        m_str = attr(str)
        m_int = attr(int)
        m_long = attr(float)
        m_float = attr(float)
        n_int = attr(int, default=None)
        n_str = attr(str, default=None)
    foo = Foo()
    assert foo.m_str == ''
    assert foo.m_int == 0
    assert foo.m_long == 0
    assert foo.m_float == 0
    assert foo.n_int is None
    assert foo.n_str is None</t>
<t tx="T11">
def check_othertypes(self):
    class UpCase:
        def __init__(self, value): self.value = str(value).upper()
        def __cmp__(self, other): return cmp(self.value, other)
        def __repr__(self): return value
    class Foo(Strongbox):
        bar = attr(UpCase, default="xyz")
        abc = attr(str, default="xyz")
    foo = Foo()
    assert foo.bar == "XYZ", foo.bar
    assert foo.abc == "xyz", foo.abc</t>
<t tx="T12">
def check_static_typing(self):
    class Foo(Strongbox):
       bar = attr(int)
    foo = Foo()
    try:
       goterr = 0
       foo.bar = "not an int value"
    except TypeError:
       goterr = 1
    assert goterr, "should get TypeError assigning string to int attr"


def check_okay_lambda(self):
    class Foo(Strongbox):
        bar = attr(int, lambda x: 5 &lt; x &lt; 10)
    foo = Foo()
    foo.bar = 7 # should work
    try:
       goterr = 0
       foo.bar = 10
    except ValueError:
        goterr = 1
    assert goterr, "the lambda should have rejected bar=10"


def check_okay_list(self):
    class Paint(Strongbox):
        color = attr(str, ["red", "green", "blue"])
    p = Paint()
    p.color = "red" # should work
    try:
        goterr = 0
        p.color = "orange"
    except ValueError:
        goterr = 1
    assert goterr, "values not in the list should be rejected"

    
def check_okay_regexp(self):
    class UsCitizen(Strongbox):
        ssn = attr(str, r"\d{3}-?\d{2}-?\d{4}")
    
    elmer = UsCitizen()
    elmer.ssn = "404-44-4040" # should work
    try:
        goterr = 0
        elmer.ssn = "867-5309"
    except ValueError:
        goterr = 1
    assert goterr, "ssn regexp should reject even the most famous phone number in america..."</t>
<t tx="T13">@
But of course, we can turn it off...

@code

def check_allowNone(self):
    class Foo(Strongbox):
       bar = attr(int)
    foo = Foo()
    try:
       goterr = 0
       foo.bar = None
    except ValueError:
       goterr = 1
    assert not goterr, "assigning None didn't work!"


def check_dontAllowNone(self):
    class Foo(Strongbox):
       bar = attr(int,allowNone=0)
    foo = Foo(bar=15)
    try:
       goterr = 0
       foo.bar = None
    except ValueError:
       goterr = 1
    assert goterr, "assigning None should have failed!"</t>
<t tx="T14">@
Subject from the GoF Observer pattern.
@code
__ver__="$Id$"

import unittest
import types
from Strongbox import ObservableStrongbox

class SubjectTest(unittest.TestCase):

    def setUp(self):
        pass
        
    @others
       
    def tearDown(self):
        pass</t>
<t tx="T15">

def check_attach(self):
    subject = ObservableStrongbox()
    observer = object()
    subject.attach(observer)
    assert observer in subject.private.observers


def check_detach(self):
    subject = ObservableStrongbox()
    observer = object()
    subject.attach(object)
    subject.detach(object)
    assert len(subject.private.observers) == 0</t>
<t tx="T16">
def check_notify(self):
    class Observer:
        def update(self, subject): self.updated = 1
    obs = Observer()
    sub = ObservableStrongbox()
    sub.attach(obs)
    sub.notify()
    assert obs.updated, "observer should have been updated"</t>
</tnodes>
</leo_file>
