import re
import unittest

import pywmlx.state.machine
import pywmlx.state.wml_states
from pywmlx.state.state import State


''' 
-----------------------------------------------------------------------------
this test is pretty complex... I know...
And, moreover, it is nearly impossible to properly test every state 
on statemachine.

This test (and the other tests focused on state testing) tries to verify
the most important things around the states used on state machine

1) If the all expected states actually exist
2) If every state calls an existing states when calling run() or when changing
   state with iffail. 
   Iffail will not checked in "always run" states (when state.regex is None)

3) On this lua states we are also checking 70% of the aspects around
   translated string on lua code...
   We will test if a pending lua string is correctly setted and if matches
   the test sentence
   
 4) since lua can migrate to WML and viceversa, a fake wml idle state is
    provided on testing luastates only
    
Explaining in-deep the complex tests:

The code tryes to avoid multiple repetitions, and can be not easy to read:

basicly, the "test_setup_luastates" is divided in three parts, and
every part is structured in the same way.

Every part, infact is a list of tuple. Every tuple will be used by
"verify_luastates" for a single state_check

every tuple has those parameters:
1) statename -> the state to test (example 'lua_idle') this is the dictionary
                key where the state is stored in the statemachine
2) xline -> a fake line to test if the regex matches or not.
3) match_1 -> value -> value expected on regex match.group(1)
              None -> don't check match.group(1) (example: it does not exists)
4) match_2 -> exactly as match_1, but for regex match.group(2)
5) match_3 -> exactly as match_1, but for regex match.group(3)
6) extra -> this is the most complex thing.
            It can be None (do nothing special)
            or it can be a tuple of two values.
            If it is a tuple of two values, extra will be used to launch a 
            function. First value of the tuple is the function to launch,
            the second value of the tuple is a list (or a tuple) of values
            to pass to the function

one of the most common usage of extra is to reset PendingString from 
statemachine after every test thet creates a lua string.
In this way we can reset PendingString to None, verify if the new string is
correctly setted as PendingString and finally if the string is stored correctly
with the expected value.

In those cases we use 'lua_idle' state as a fake state to test, since we
are more concerned of the action performed by extra than actually testing
a string.

--------------------------------------------------------------------------
'''



class FakeLuaIdleState:
    def __init__(self):
        self.regex = None
        self.iffail = None
    
    def run(self, xline, lineno, match):
        return (xline, 'wml_idle')

         


class Test_WmlStates(unittest.TestCase):
    def check_delpending(self):
        pywmlx.state.machine._pending_wmlstring = None
    
    def verify_wmlstates(self, statename, xline, grp1, grp2, grp3, extra):        
        mystate = pywmlx.state.machine._states.get(statename)
        if mystate is None:
            errmsg = "state " + statename + " does not exist!"
            self.assertEqual(1,2, errmsg)
        else:
            if mystate.regex is not None:
                m = re.match(mystate.regex, xline)
                if not m:
                    errmsg = ( "error on state: " + statename + "\n" + 
                               "regex does not match" )
                    self.assertEqual(1,2, errmsg)
                else:
                    new_xline, new_stname = mystate.run(xline, 1, m)
                    new_state = pywmlx.state.machine._states.get(new_stname)
                    if new_state is None:
                        errmsg = ( "state " + new_state + " does not exist!" +
                                   " (called on return)" )
                        self.assertEqual(1,2, errmsg)
                    if grp1 is not None:
                        try:
                            self.assertEqual(grp1, m.group(1))
                        except IndexError:
                            self.assertEqual(1,2, ( "group 1 does not exist" +
                                  "\n" + xline) )
                    if grp2 is not None:
                        try:
                            self.assertEqual(grp2, m.group(2))
                        except IndexError:
                            self.assertEqual(1,2, ( "group 2 does not exist" +
                                  "\n" + xline) )
                    if grp3 is not None:
                        try:
                            self.assertEqual(grp3, m.group(3))
                        except IndexError:
                            self.assertEqual(1,2, ( "group 3 does not exist" +
                                  "\n" + xline) )
                    if extra is not None:
                        f = extra[0]
                        v = extra[1]
                        f(*v)
                    iffail = pywmlx.state.machine._states.get(mystate.iffail)
                    if iffail is None:
                        errmsg = ( "state " + statename + " does not exist!" +
                                   " (on iffail)" )
                        self.assertEqual(1,2, errmsg)
            else:
                new_xline, new_stname = mystate.run(xline, 1, None)
                if new_stname is None:
                    errmsg = ( "state " + statename + " does not exist!" +
                                   " (called on return)" )
                    self.assertEqual(1,2, errmsg)
    
    def test_setup_wmlstates(self):
        pywmlx.nodemanip.newfile("fileref", 1)
        fake = FakeLuaIdleState()
        pywmlx.state.wml_states.setup_wmlstates()
        pywmlx.state.machine.addstate('lua_idle', 
                 State(fake.regex, fake.run, fake.iffail) )
        xstr1 = 'ciao, come va?\n' + 'tutto bene?\n' + 'vero?'
        for statename, xline, match_1, match_2, match_3, extra in [
                    ('wml_idle', 'test', None, None, None,
                      (pywmlx.nodemanip.newfile, ("fileref", 1)) ),
                    ('wml_define', '#define QUALCOSA', 'define',
                      None, None, None),
                    ('wml_define', '#enddef', 'enddef',
                      None, None, None),
                    ('wml_define', '# wmlxgettext: WMLCODE', None,
                      None, None, None),
                    ('wml_tag', '[+tag]', None, None, None, None),
                    ('wml_getinf', ' speaker = Foo', 'speaker', 'Foo', 
                      None, None),
                    ('wml_getinf', ' id = Foo', 'id', 'Foo', 
                      None, None),
                    ('wml_getinf', ' role = Foo', 'role', 'Foo', 
                      None, None),
                    ('wml_getinf', ' description = Foo', 'description', 'Foo', 
                      None, None),
                    ('wml_getinf', ' condition = Foo', 'condition', 'Foo', 
                      None, None),
                    ('wml_getinf', ' type = Foo', 'type', 'Foo', 
                      None, None),
                    ('wml_getinf', ' race = Foo', 'race', 'Foo', 
                      None, None),
                    ('wml_tag', '[/tag]', None, None, None, None),
                    ('wml_idle', 'test', None, None, None,
                      (pywmlx.nodemanip.newfile, ("fileref", 1)) ),
                    ('wml_checkdom', '#textdomain qualcosa',
                     'qualcosa', None, None, None),
                    ('wml_checkpo', '# po-override: qualcosa',
                     'po-override', 'qualcosa', None, None),
                    ('wml_checkpo', '# po: qualcosa', 
                     'po', 'qualcosa', None, None),
                    ('wml_comment', '# commento', None, None, None, None),
                    ('wml_golua', 'caspi _ terina << ecco', 
                      None, None, None, None),
                    ('wml_final', 'test', None, None, None, None) ]:
            self.verify_wmlstates(statename, xline, match_1, match_2, 
                                  match_3, extra)
    
    def test_sentences(self):
        pywmlx.state.wml_states.setup_wmlstates()
        pywmlx.nodemanip.newfile("fileref", 1)
        for statename, s1, s2, g2 in [ 
                 ('wml_str01', '_ "ciao "" come', 'ciao "" come', False),
                 ('wml_str10', 'va? "" bene?"', 'ciao "" come\nva? "" bene?',
                   True) ]:
            mystate = pywmlx.state.machine._states.get(statename)
            m = re.match(mystate.regex, s1)
            new_xline, new_stname = mystate.run(s1, 1, m)
            self.assertEqual(pywmlx.state.machine._pending_wmlstring.wmlstring,
                             s2)
            new_state = pywmlx.state.machine._states.get(new_stname)
            if new_state is None:
                errmsg = ( "state " + new_stname + " does not exist!" +
                           " (called on return)" )
                self.assertEqual(1,2, errmsg)
            iffail = pywmlx.state.machine._states.get(mystate.iffail)
            if iffail is None:
                errmsg = ( "state " + mystate.iffail + " does not exist!" +
                           " (on " + statename + ".iffail)" )
                self.assertEqual(1,2, errmsg)
            if g2:
                self.assertEqual(m.group(2), '"')

