import re
import unittest

import pywmlx.state.machine
import pywmlx.state.lua_states
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



class FakeWmlIdleState:
    def __init__(self):
        self.regex = None
        self.iffail = None
    
    def run(self, xline, lineno, match):
        return (xline, 'lua_idle')



class Test_LuaStates(unittest.TestCase):
    def check_glob_pendingstr(self, value):
        if value is not None and (
                 pywmlx.state.machine._pending_luastring is None):
            self.assertEqual(1,2, "pending luastring is None")
        elif value is not None:
            self.assertEqual(pywmlx.state.machine._pending_luastring.luastring,
                             value)
        else:
            self.assertIs(pywmlx.state.machine._pending_luastring, None)
    
    def check_var(self, var, checktype, value):
        if checktype == 'equal':
            self.assertEqual(var, value)
        elif checktype == 'is':
            self.assertIs(var, value)
    
    def check_delpending(self):
        pywmlx.state.machine._pending_luastring = None
    
    def verify_luastates(self, statename, xline, grp1, grp2, grp3, extra):        
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
    
    def test_setup_luastates(self):
        fake = FakeWmlIdleState()
        pywmlx.state.lua_states.setup_luastates()
        pywmlx.state.machine.addstate('wml_idle', 
                 State(fake.regex, fake.run, fake.iffail) )
        xstr1 = 'ciao, come va?\n' + 'tutto bene?\n' + 'vero?'
        for statename, xline, match_1, match_2, match_3, extra in [
                    ('lua_checkdom', '-- #textdomain qualcosa',
                     'qualcosa', None, None, None),
                    ('lua_checkpo', '-- # po-override: qualcosa',
                     'po-override', 'qualcosa', None, None),
                    ('lua_checkpo', '-- # po: qualcosa', 
                     'po', 'qualcosa', None, None),
                    ('lua_comment', '-- commento', None, None, None, None),
                    ('lua_gowml', 'caspi _ terina >> ecco', 
                      None, None, None, None),
                    ('lua_final', 'test', None, None, None, None),
                    ('lua_str03', '_ [==[test_lua3_str]==]', None,
                     'test_lua3_str', None, None),
                    ('lua_idle', 'test', None, None, None, 
                           (self.check_delpending, []) ) ]:
            self.verify_luastates(statename, xline, match_1, match_2, 
                                  match_3, extra)
        for (state_open, state_pending, state_pending2, open_marker, 
                  close_marker) in [ 
                      ('lua_str01', 'lua_str10', 'lua_str10', '"', '"'),
                      ('lua_str02', 'lua_str20', 'lua_str20', "'", "'"),
                      ('lua_str03o', 'lua_str31', 'lua_str30', 
                       '[==[', ']==]')]:
            xstr_x1 = '_ ' + open_marker + 'ciao, come va?'
            xstr_x2 = 'vero?' + close_marker
            for statename, xline, match_1, match_2, match_3, extra in [
                         (state_open, xstr_x1, None, 'ciao, come va?', 
                           None, None),
                         (state_pending, 'tutto bene?', None, None, None, None),
                         (state_pending2, xstr_x2, None, None, None,
                           (self.check_glob_pendingstr, 
                            ["ciao, come va?\ntutto bene?\nvero?"]) ),
                         ('lua_idle', 'test', None, None, None,
                           (self.check_var, ('luastr', 'equal', xstr1)) ),
                         ('lua_idle', 'test', None, None, None, 
                           (self.check_delpending, [] ) ) ]:
                self.verify_luastates(statename, xline, match_1, match_2, 
                                      match_3, extra)
        for (statename, xline, close_marker) in [ 
                        ('lua_str01', '_ "ciao\\""', '"'),
                        ('lua_str02', "_ 'ciao\\''",  "'") ]:
            match_2 = 'ciao\\' + close_marker
            match_3 = close_marker
            self.verify_luastates(statename, xline, None, match_2, 
                                  match_3, None)
            self.verify_luastates('lua_idle', 'test', None, None, None,
                                   (self.check_delpending, []) )
    
    #  def

