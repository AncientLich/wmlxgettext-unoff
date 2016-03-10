.. _The State Machine:

The State Machine
*****************

While developing this tool, one big issue was the WML parsing, since WML allow 
to add nested Lua code.
The classical (perl) approach was to use two separate functions, one dedicated 
to lua code, and one for WML.
The classical approach, however, can lead to some problems, when we face WML 
file with nested Lua code, so why another approach is used here.

This release has an unique "parser", using a finite state machine that reads 
every line of a file (Lua or WML) and perform the proper action (running 
a concrete state) when an important thing was found (for example, 
a translatable string).

.. code-block:: python
   
   # ./wmlxgettext:146
   pywmlx.statemachine.setup(sentlist, args.initdom, args.domain)
   for fx in args.filelist:
       # omissing some code
       # ./wmlxgettext:157
       if fname[-4:].lower() == '.cfg':
           pywmlx.statemachine.run(filebuf=infile, fileref=fx, 
                          fileno=fileno, startstate='wml_idle', waitwml=True)
       if fname[-4:].lower() == '.lua':
           pywmlx.statemachine.run(filebuf=infile, fileref=fx, 
                          fileno=fileno, startstate='lua_idle', waitwml=False)
        
First of all, the state machine is initialized with the **statemachine.setup()** 
function (called one time only during all the script execution).

Then wmlxgettext will execute **statemachine.run()** function every times we
open a new file (listed on args.filelist). This is the **statemachine.run()** 
parameters list:

   * **filebuf**: the file buffer to read 
   * **fileref**: the name of file (relative path to --directory)
   * **fileno**: a progressive (and unique) **id** value assigned to the file
   * **startstate**: the name of the state where the state machine must start.
     Its value is assigned to \'*wml_idle*\' for WML (.cfg) files or assigned
     to \'*lua_idle*\' for .lua files
   * **waitwml**: Its value is *True* if we are parsing a WML file. It is
     *False* if we are parsing a Lua file. Infact, only if a Lua code is 
     indented in a WML file you could "expect" to exit from lua parsing and
     returning to WML parsing. In a .lua file, instead, you will have only
     Lua code.

===============
The State class
===============

Now it is time to start to explain more deeply how the state machine works.
The State class has 3 properties:
    
   * **regex**: it is the regular expression to match. If the regex matches,
     than the run function will be executed. 
   * **run** (*self, xline, lineno, match*):
      * *xline*: the line of the file we are parsing
      * *lineno*: current line number
      * *match*: the match object returned by ``re.match(regex)``
   * **iffail**: the state (state name) to reach if the regex does not match 
     (usually the next state).

The State class prototype (*./pywmlx/state/state.py*) does not contain any
actual code.
The concrete states are defined in *./pywmlx/state/lua_states.py* and in 
*./pywmlx/state/wml_states.py* using temporary classes (for better code 
readability).

All states are stored in statemachine into a dictionary (**_states**) with:

   * key = State name (example: *'wml_idle'*)
   * value = concrete State object

---------------
Standard States
---------------

Standard states works exactly as previously explained:
    
.. graphviz:: stdstate.d

The regexp is verified through ``re.match``, so it maches only if the rule is 
True at the *very start* of the line. If it  matches, than **run()** is 
executed.

Run() returns a pair of values (tuple):
   * **xline**: the non-consumed part of the line. If the line is to be
     considered consumed, then xline will be setted to *None*
   * **nextstate**: label of the next state to go. Usually it is *'wml_idle'*
     or *'lua_idle'* since the parsing is recursive.
     
If the regexp does not match, the **iffail** state will be reached. Usually the
iffail is equal to the "*next state*". See `State Sequence`_
     
-----------------
Always-Run States
-----------------

Always-run states are special states with ``regexp = None``

Unlike standard states, an always-run state will **always** execute its own
**run()** function. An example of always-run state is *'wml_idle'* state.

An always-run state does not actually require the **iffail** parameter. This
is why always-run states have ``iffail = None``

==============
State Sequence
==============

Now it is the time to show the generic state sequence:
    
.. graphviz:: machine01.d

This is, more or less, the design that is applied both for WML and Lua states.
However the flow chart already displayed is mainly focused to WML states:
    
   * Arrows:
      * green -> Always-run states (IDLE and FINAL) **always** go into the
        state pointed by the green arrow 
      * blue -> Standard state reach the State pointed by blue arrow when the
        regex found a match.
      * black -> Standard state reach the State pointed by black arrow when the 
        regex **DOESN'T** match
   * Boxes/Ellipses:
      * IDLE and FINAL states are special states that appears both in WML and in 
        Lua code. They are displayed in green circle since they are "always run" 
        states.
      * Preprocessing States appears both in WML and Lua code, even if WML and 
        Lua use different states (for example, *#wmlxgettext* is not needed in 
        Lua code). They are standard states (grey box)
      * *'wml_getinf'* and *'wml_tag'* states appears only in WML states 
        (yellow box)
      * String States (red boxes) behave very differently in WML and in Lua.
      * Change Language State checks if WML code switch to Lua or vice-versa.
        If the language is changed, the IDLE state of the other language will
        be reached (cyan box).
      
---------------------
IDLE and FINAL States
---------------------

Both IDLE and FINAL states check if there is a pending string, and if it is so,
pending string will be stored in memory.

   * **WML**: checks ``pymlx.state.machine._pending_wmlstring``. If 
     ``pymlx.state.machine._pending_wmlstring is None`` there is no pending
     WML string to store
   * **Lua**: checks ``pymlx.state.machine._pending_luastring``. If 
     ``pymlx.state.machine._pending_luastring is None`` there is no pending
     Lua string to store

Both Lua and WML pending strings, before actually storing its own value, 
perform some cheks:
    
    * verify if it is a translatable string
    * verify if the current domain is the same of the addon domain name
    * if so, it fixes the string for storage, and then store it
    
However WML pending string is stored in a very different way then Lua pending
string:
    
    * Lua pending string is directly stored, as a ``PoCommentedString``, in the 
      *"posentence dictionary"*.
    * WML pending string is, instead, stored in the current WML node as a 
      ``WmlNodeSentence``. Only when the current WML node will be closed, all 
      ``WmlNodeSentence`` objects contained in the node will be stored in the 
      *"posentence dictionary"*. (See: :ref:`nodemanip_module` and
      :ref:`PoCommentedString_conv`)
      
*WmlFinalState* always return the pair ``(xline, 'wml_idle')`` while 
*LuaFinalState* always return the pair ``(xline, 'lua_idle')``, 
where ``xline`` is setted to ``None`` in both cases. 
As previously explained, infact, when ``xline`` is ``None``, the line is 
considered completely consumed and the statemachine will read the next line 
of the file.
    
Finally, the *'lua_final'* state perform another action, but it will be 
explain later. See `About storing the last Lua function name`_.

-----------------------
*Capture String* States
-----------------------

When a string (translatable or not) is found, then the regexp of the proper
"*Capture String*" state matches. Captured string will be stored as 
``pymlx.state.machine._pending_wmlstring`` (WML string), or as 
``pymlx.state.machine._pending_luastring`` (Lua string).

Now it is the time to discuss deeply about those capturing string states.

++++++++++++++++++++++++++++
*Capture String*: WML States
++++++++++++++++++++++++++++

WML accepts only one syntax:
    
.. code-block:: none

   _ "translatable_string"
   
Only two states, then, required to capture strings:


.. code-block:: python
   
   # ./pywmlx/state/wml_states:161
   class WmlStr01:
       # ...
   # ./pywmlx/state/wml_states:190
   class WmlStr10:
           
.. graphviz:: wmlstr.d

More in details:

    * **WmlStr01** (*'wml_str01'*): This state capture a single-line string 
      and also capture the FIRST LINE of a WML multiline string.
      
       * If it is a single line string, the string will be stored in
         ``pymlx.state.machine._pending_wmlstring``. (Change to *'wml_idle'* 
         state).
       * If the closing quote ``"`` 
         does not exist (*multiline string*) , then the matched string will be 
         saved in ``pymlx.state.machine._pending_wmlstring``.
         Following lines will be added to the pending string by the WmlStr10
         State (change to *'wml_str10'* state)
    
    * **WmlStr10** (*'wml_str10'*): All following lines of the multiline 
      string will be added to pending string by this state 
      until the closing quote ``"``
      will be finded. This states recursively come back to itself, and, when
      the string ends, state will be changed again to *'wml_idle'*
      
++++++++++++++++++++++++++++
*Capture String*: Lua States
++++++++++++++++++++++++++++

Unlike WML, Lua accepts three different syntaxes:
    
.. code-block:: lua
   
   "string: type 1"
   
   'string: type 2'
   
   [[string: type 3]]
   
The third way (mostly suggested for multi-line lua strings) is even more
flexible than showed in the sample code above, as you can type any number
of equals symbols (from 0 to n) between the two brackets ``[[`` and ``]]``

.. note::
    
  In the example above, we wrote ``[[string: type3]]``, since it is the most 
  common way of defining a bracketed lua string, but we could also put any 
  number of equals symobols between brackets. 
  
  For example, we could have printed ``[==[string: type3]==]`` placing the 
  equal symbol two times. In that case, both opening and closing delimiter
  must use the same amount of equal symbols.
  
Coming back to wmlxgettext, we shoud now notice that all this flexibility 
allowed by the lua language (three ways to identify a string) means 
"*more states are required*". There are, infact, seven states this time:
    
.. code-block:: python
   
   # ./pywmlx/state/lua_states:71 (syntax "1": single-line or start multiline)
   class LuaStr01:
       # ...
   # ./pywmlx/state/lua_states:173 (syntax "1": multiline)
   class LuaStr10:
       # ...
   # ./pywmlx/state/lua_states:99 (syntax "2": single-line or start multiline)
   class LuaStr02:
       # ...
   # ./pywmlx/state/lua_states:193 (syntax "2": multiline)
   class LuaStr20:
       # ...
   # ./pywmlx/state/lua_states:127 (syntax "3": single-line ONLY)
   class LuaStr03:
       # ...
   # ./pywmlx/state/lua_states:149 (syntax "3": start multiline)
   class LuaStr03o:
       # ...
   # ./pywmlx/state/lua_states:211 (syntax "3": multiline [from line 2])
   class LuaStr30:
       # ...
   
.. graphviz:: luastr.d

This time the flow chart is not so easy to understand at a first sight, so
it requires a little explaination:
    
    * Boxes/Ellipses:
       * green -> always-run states (green arrow rule applied)
       * orange -> used for "Next State", for a better look
       * red (LuaStr10 and LuaStr20): LuaStr10 and LuaStr20 are recursive 
         standard states. They can go back to theirself, until the end of the 
         multi-line string is matched 
         (when the multi-line string ends, *'lua_idle'* state will be reached)
         (no arrow rule: all arrows are black)
       * red (LuaStr30): LuaStr30 is indeed an always-run state, but it 
         acts like a recursive standard state. The regular expression 
         evaluation is moved in the run() function since the regexp rule is 
         calculated on runtime.
         If the regexp doesn't match (current line of code does not end the
         multiline string) than LuaStr30 comes back to itself (recursive 
         state). If the regexp does match, the multi-line string finished, 
         and LuaStr30 goes to LuaIdleState.
       * grey -> standard states (black, blue and dotted blue arrow rules 
         applied)
       * purple (ellipse) -> LuaStr30 can find (or not) the ``]==]`` symbol.
         Purple ellipses shows what happen if ``]==]`` was found and if 
         ``]==]`` was NOT found (see where the black arrows will go).
    * Arrow rules (when applied):
       * green -> LuaStr31 is an always-run state. LuaStr31 will **always**
         come back to LuaStr30 state
       * blue -> when the state finds what it is searching, go to the state 
         pointed by blue arrow
       * blue (dotted) -> LuaStr01 and LuaStr02 regex rule can match both
         a single-line string AND the start of a multi-line string. If 
         the a multi-line string matched, than go to the state pointed by the 
         dotted blue arrow instead of the standard blue arrow
       * black -> When the regex rule of the state fails (the state does
         not find what it is searching). [except for red boxes]

------------------------------------------
About storing the last *Lua function name*
------------------------------------------

Unlike the WML states, there isn't any Lua state that captures lua infos.
The only extra info that could be auto-cached inside a lua code is the name
of the last function opened / defined.

This kind of search required to use a specific regexp search, using 
``re.search`` instead of ``re.match``.
Unlike all other searches, infact, we need to capture function name at
any point of the line we are parsing, or the regexp will not work properly.

But, as explained at the beginning of this page, the state machine relies on
``re.match`` (best performance) to verify the regexp rule of every state. For
this reason, 
``LuaFinalState`` 
searches by itself if there is a function name somewhere, and, if so, stores 
the value into ``pywmlx.state.machine._pending_luafuncname``.

===========================
State Machine and nodemanip
===========================

The previous chapter (:ref:`wmllua_intro`) explained a lot of things, and
expecially:
   
   * how WML nodes are stored in memory
   * how ``nodemanip`` module manage WML nodes (See: :ref:`nodemanip_module`).

But, an important thing was omissed: **nodemanip** is used by the statemachine.

.. graphviz:: machine02.d

When wmlxgettext ``import pywmlx``, nodemanip module is **not** loaded in 
``pywmlx`` namespace: ``nodemanip`` is only internally used by state machine
(module ``./pywmlx/state/machine.py``).

