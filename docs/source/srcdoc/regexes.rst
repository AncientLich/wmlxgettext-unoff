Deep explaination of all regular expressions
********************************************

This part of the source documentation is a kind of an "appendix", where all
regular expressions used in source code will be explained deeply

==========================
Regexes used on WML States
==========================

--------------
WML IDLE State
--------------

.. code-block:: python
   
   m = re.match(r'\s*$', xline)

If the line is actually empty (only contains tabs/spaces) it will be consumed
immediately. It is equal to that regular expression::
   
   ^\s*$

----------------
WmlCheckdomState
----------------

.. code-block:: python
   
   self.regex = re.compile(r'\s*#textdomain\s+(\S+)', re.I)

this is equal to that (case insensitive) regex::
   
   ^\s*#textdomain\s+(\S+)

At the **start of the string** will search for:
   
   * spaces/tabs (from 0 to n)
   * the character ``#``.
   * the word ``textdomain`` followed by one or more spaces
   * one or more NO-SPACE characters, captured into group 1

---------------
WmlCheckpoState
---------------

.. code-block:: python
   
   rx = r'\s*#\s+(wmlxgettext|po-override|po):\s+(.+)'
   self.regex = re.compile(rx, re.I)

wich is equal to that (case insensitive) regex::
   
   ^\s*#\s+(wmlxgettext|po-override|po):\s+(.+)

At the **start of the string** will search for:
   
   * spaces/tabs (from 0 to n)
   * the character ``#``
   * one or more space before an actual word
   * one of those words: *wmlxgettext, po-override* or *po* captured into
     group 1.
   * followed by the character ``:`` and one or more spaces/tabs.
   * followed by any number of any characters (at least 1) captured on group 2.

---------------
WmlCommentState
---------------

.. code-block:: python
   
   self.regex = re.compile(r'\s*#.+')

At the **start of the string** will search for:
   
   * spaces/tabs (from 0 to n)
   * the character ``#`` followed by any character

-----------
WmlTagState
-----------

.. note::
  
  Special Thanks to:
      
    * **Soliton**
      
      * for pointing me that a tag name could, in theory, a number
      * for having a very nice idea about how to distinguish a tag from an 
        array index (see the regexp explaination)
    
    * **celticminstrel**
      
      * for providing me a good regexp rule, that allowed me to
        write down the regexp used in this state

.. code-block:: python
   
   rx = r'\s*(?:[^"]+\(\s*)?\s*\[\s*([\/+-]?)\s*([A-Za-z0-9_]+)\s*\]'
   self.regex = re.compile(rx)

Before explaining what the regex searches, we need to explain why the regexp
was written in this way.

We must take mind that a WML tag (we now focus on open tag, but the discussion
is the same also on close tags) can appear in two different ways; this is the 
first one::
  
  # first way: tagname can be defined at the start of the line 
    [tagname]

In this case, the WML line we are parsing may have an arbitrary number of
spaces (or tabs) before the tagname, but nothing else must appear before the
[tagname]. This is the most common case where a tag is defined, but it is not
the only one; a tag can be added also in the body of a WML macro call as a part
of WML code passed as parameter to the macro.

So why a WML tag can also apper inside the body of a macro call, like showed
in this example::
  
  {MACRO ([foo]
               bar = "baz"
          [/foo])}

So, wmlxgettext had to face two corner problems:
  * it should record the ``[foo]`` open tag inside the macro call,
    or it will return an error when closing ``[/foo]`` tag will be found
  * it should, however avoid to collect array indexes, thinking they are
    tags, for example::
     
     # [$i], here, is not a tag, but it is an index value of the array my_array
     value = my_array[$i]

So... how to distinguish tag from an array using a regexp? Well... a tagname,
when placed inside a WML macro call, should be ALWAYS immediately preceded by 
``(``; nothing else than spaces can be putted before the parenthesis and the 
tag definition.

After all those explainations we have almost all the informations required to
understand why the regexp used on WmlTagState is::
  
  ^\s*(?:[^"]+\(\s*)?\[\s*([\/+-]?)\s*([A-Za-z0-9_]+)\s*\]

As usual, at the start of the string, an arbitrary number of spaces or tabs 
(``^\s*``) can be found.

After that the regexp will consider two different scenarios:
  * first scenario: [tagname] is defined inside a macro call
  * second scenario: [tagname] stays alone (most common case)

On the fist scenario, the [tagname] is contained into a MACRO CALL, so we must
verify that the [tagname] definition immediately follows a parenthesis ``(``, 
except for spaces or tabs that can separates ``(`` and ``[tagname]``::
  
  (?:[^"]+\(\s*)?

This check is performed by the non-capturing group written above, wich can 
occur one-time only (when tagname is contained in the macro definition) 
**or** it can occur **zero** times (when the tagname stays alone in the line,
second scenario).

The non-capturing group will search for the last opening parenthesis 
encountered (and following spaces) that satisfies the remaining part of the
regexp (explained later) wich search for [tagname].

This is, in particular, made by the second part of the non-capturing group::
  
  \(\s*
    
But the non-capturing group will verify that no quote symbols (``"``)
were found in the meantime::
  
  [^"]+

The reason of this exclusion is related to the wmlxgettext state machine 
design: the WmlTagState, infact, is evaluated before the WmlStr01 state 
(wich will search WML strings, translatable or not).

Wich means: if we allowed WmlTagState to match a line containing a quotation,
we would let WmlTagState to consume all the matched line, including the
WML string, wich will never been evalated by WmlStr01 State. But we don't 
want that this event could happen.

.. graphviz:: wmlstr_regex.d

So, coming back to the regexp::
  
  ^\s*(?:[^"]+\(\s*)?\[\s*([\/+-]?)\s*([A-Za-z0-9_]+)\s*\]
       
We said:
    
  * ``^\s*`` will search for arbitrary number of spaces (or tabs) at the start 
    of the line
  * ``(?:[^"]+\(\s*)?`` is the **zero or one** time non-campturing group that
    verifies if the tag is included inside a macro call. Wmlxgettext will
    search for a ``[tagname]`` wich is directly preceded by an opening 
    parenthesis and an arbitrary number of spaces (or tabs). In the meantime
    it will verify that no quotations symbols (``"``) can be found in the 
    meantime. If a quotation symbol will be found, the regexp will be fail, so
    the WmlStr01 state can do its work (see the flow chart here above).
  * ``\[\s*([\/+-]?)\s*([A-Za-z0-9_]+)\s*\]`` is the final part of the regexp
    (valid both for tags placed alone and for tags placed inside a macro call)
    that actually identify the tag. It will discussed here now.

The final part of the regular expression will search for ``[tagname]``, 
``[/tagname]``, ``[+tagname]`` or ``[-tagname]`` where any number of spaces can
be placed between ``[``, tagname and ``]``.

If ``+``, ``-`` or ``/`` symbol is used, any number of spaces can be placed
between the symbol, the ``[`` and the tagname.

The regular expression, in this final part will also do those tasks:
  
  * it will store, on group(1), the symbol ``+``, ``-`` or ``/``. 
    If no symbol will be used, the group(1) will be an empty string.
  
  * it will store, on group(2), the tagname. Characters allowed are only 
    letters, numbers, or underscore, so why the expression ``([A-Za-z0-9_]+)``
    is used there (note that tagname must contain at least one character, this
    is why the ``+`` quantifier was used).
    
.. note::
  
  On group(1), as we said, we can find an empty string (no symbol used) or one
  of those symbols: ``+``, ``-`` and ``/``.
  
    * if ``/`` is found, then the tag is a closing tag
    * if ``+`` is found, the tag is considered like a normal open tag, ignoring
      the ``+`` symbol.
    * if ``-`` is found, the tag is treated like [+tag].
  
  Note that the ``[-tag]`` is not currently supported in WML code. Wmlxgettext
  included the rule for the ``-`` symbol if, in a future, also the [-tag]
  feature will ever included (thinking the chance of doing the opposite thing
  that is done by the [+tag]).

--------------
WmlGetinfState
--------------

.. code-block:: python
   
   rx = ( r'\s*(speaker|id|role|description|condition|type|race)' +
          r'\s*=\s*(.*)' )
   self.regex = re.compile(rx, re.I)
   
This **case-insensitive** regex will be search, **start of the string**, for:
   
   * spaces/tabs (from 0 to n)
   * one of the following words: *speaker, id, role, description, condition,
     type* or *race*. The word will be captured into group 1.
   * spaces/tabs (from 0 to n)
   * the ``=`` character
   * spaces/tabs (from 0 to n)
   * any number of any character, captured by group 2. (this will be the value
     assigned to the parameter captured by group 1).

.. note::
   
   The ``WmlGetinfState`` and the state ``WmlStr01`` could generate a bug, 
   without the proper cautions.
   This is the reason why you can find this code into ``WmlGetinfState``
   
   .. code-block:: python
   
      if '"' in match.group(2):
          _nextstate = 'wml_str01'
          pywmlx.state.machine._pending_winfotype = match.group(1)
   
   If a ``"`` sign was found in group 2, it means that the value assigned to
   the parameter (for example, ``name="something"``) is a quoted string.
   This string must be managed then by the state ``WmlStr01``. State Machine
   will remember that there is a pending wml info with quoted string. 
   the ``winfotype`` will store only the parameter at the moment, waiting for
   ``WmlStr01`` (that will process the quoted string)

--------------
State WmlStr01
--------------

.. code-block:: python
   
   rx = r'(?:[^"]*?)\s*(_?)\s*"((?:""|[^"])*)("?)'
   self.regex = re.compile(rx)

the regexp used here is a bit complex, so it will be atomized::
    
   ^(?:[^"]*?)
   
without creating group (``(?:)`` creates a non-capturing group), any number of
characters **different than** ``"`` will be found. But the search will be less
greedy than possible (thank the very last ``?`` putted after ``*``).
The "*less greedy than possible*" rule is necessary, othewhise the following 
rule will be ignored::
   
   \s*(_?)\s*"

we need, infact, to know if a string is translatable or not. We must see if a
``_`` sign was found before opening the quote. But the ``_`` sign is different
than ``"`` sign, so if the previous rule was greedy, the regexp could never
capture on group 1 the ``_`` sign.
Instead, since the non-capturing group ``(?:[^"]*?)`` is "*less greedy than 
possible*" it will stops as soon the following rule
``\s*(_?)\s*"`` will be true.

Since the rule ``\s*(_?)\s*"`` will check:
   
   * spaces/tabs (from 0 to n)
   * **zero or one** ``_`` sign, captured on group 1, followed by spaces/tabs
     (from 0 to n)
   * followed by ``"`` sign
   
this means that the regexp, until now:
   
   * is true even if something was found before ``_ "translatable string"``
   * will see if ``_`` is used (group 1). Group 1 will be ``_`` if the ``_``
     will be found, or it will be an empty string if the ``_`` will not be 
     found (string is not translatable)
   * it will check for opening quote ``"`` where the string actually starts.

Finally, the regexp continues with::
   
   ((?:""|[^"])*)("?)

This part of the regexp must be explained a bit. A WML string can contain two
following ``"`` signs if you want to use the ``"`` character inside your 
string (for example, using a ``"`` sign in a message).
For this reason, if you find ``""`` into a WML string, the string is not yet
finised.

So, this part of the regexp:
   
   * create a new group 2 (with the **outer** parenthesis on
     ``((?:""|[^"])*)`` )
   * that group 2 will capture any number of the things captured by the
     **inner** parenthesis, wich doesn't create any additional groups 
     (thank of the starting ``?:``).
   * the "things" that can be captured on group 2, so, can be:
      
      * either `""`
      * **or** any character **different than** ``"``

   * finally checks if there is the enclosing ``"`` sign and capture it to
     group 3.
     
This is how this complex regexp works.

.. note::
   
   it is the time to remember what the regexp capturing groups:
      
      * group 1 -> can be ``_`` or an empty string (to understand it the string
        is translatable or not).
      * group 2 -> it is the text
      * group 3 -> can be ``"`` or an empty string. If it is an empty string, 
        (closing ``"`` sign not found) than the string is multi-line.

--------------
State WmlStr10
--------------

.. code-block:: python
   
   self.regex = re.compile(r'((?:""|[^"])*)("?)')
   
The regexp is musch more simplier than the one used by the state ``WmlStr01``
even if it works in a very similar way.

The basic idea of this regexp is: <<*we are parsing a multi line string and 
this is NOT the first line of the string, so the starting part of the file line
must be contained into the string until the ending ``"`` will be found*>>.

It will save, on group 1 and group 2, what the regexp used by WmlStr01 capture
on group 2 and group 3.

-------------
WmlGoluaState
-------------

.. code-block:: python

   self.regex = re.compile(r'.*?<<\s*')

It will be check, from the start part of the string, any number of any
character (less greedy then possible) until ``<<`` found (followed by any 
number of spaces/tabs - from 0 to n).

If the regexp will mach, the State will consume the line until the last space
of the ``<<`` symbol, and than switch to ``lua_idle`` state 
(parse Lua language).

==========================
Regexes used on Lua States
==========================

Unlike WML states, we will not explain **all** the regexp used, since most of 
them are **very similar** to the ones used on WML states

-----------------------
*"Preprocessor"* States
-----------------------

``LuaCheckdomState``, ``LuaCheckpoState`` and ``LuaCommentState`` use regexpes 
very similar to the ones used on `WmlCheckdomState`_, `WmlCheckpoState`_ and
on `WmlCommentState`_.

Here the differences:
   
   * ``#textdomain``, ``# po:`` and ``# po-override:`` must be preceded by
     the lua comment marker ``--`` followed by any number of spaces\tabs.
   * ``# wmlxgettext:`` is **not** supported on lua code (it is useless)
   * lua comment starts with ``--`` and not with ``#``

----------------------------
LuaStr01 and LuaStr02 States
----------------------------

We will display the LuaStr01 python code

.. code-block:: python
   
   rx = r'''(?:[^["']*?)(_?)\s*"((?:\\"|[^"])*)("?)'''
   self.regex = re.compile(rx)
   
wich is equal to the following regexp::
   
   ^(?:[^["']*?)(_?)\s*"((?:\\"|[^"])*)("?)

The regexp used by LuaStr02 is more or less the same, infact it is equal to
the following regexp::
   
   ^(?:[^["']*?)(_?)\s*'((?:\\'|[^'])*)('?)

The basic logic of those regexp is more or less the same as the one used by
`State WmlStr01`_.

As the regexp used by `State WmlStr01`_, it can be divided in three parts:
   
   * *things* before the strings starts
   * check if the string is translatable, searching for ``_`` sign rigtly
     before the string starts (followed by any number of spaces-tabs).
     (group 1 = ``_`` or empty string)
   * check for start quote (``"`` for LuaStr01, ``'`` for LuaStr02).
   * check for text (group 2)
   * check for quotation end (group 3) (if empty, is a multiline string).
   
The actual difference from the regexp used by `State WmlStr01`_ is the 
**first** part of the regexp rule::
   
   (?:[^["']*?)

Instead of searching of all characters different than only the ``"`` symbol, 
this regex will search all characters that will be **neither** ``"``, 
nor ``'``, nor ``[``.

This will avoid conflicts from the three possible syntaxes and it will ensure
that, if any of the regexp match, it will really match the first string, 
avoiding that a lua string will be skipped.

Another difference is that the "non enclosing quote" is not ``""`` like WML, 
but it is escaped in a different way (``\"`` or ``\'``), this is why the
rule is a bit different also in the third part of the regexp rule.

----------------------------
LuaStr10 and LuaStr20 States
----------------------------

The basic idea is the same as the one used by `State WmlStr01`_.

(See also: `State WmlStr01`_ and `LuaStr01 and LuaStr02 States`_).

--------------
LuaStr03 State
--------------

.. note:
    
  Special thank to celticminstrel for improving my old regex into the
  current regex.

LuaStr03 regexp can is equal to the following regexp rule::
   
   ^(?:[^["']*?)(_?)\s*\[(=*)\[(.*?)]\2]
        
The first part of regexp (``^(?:[^["']*?)``) is already explained in
`LuaStr01 and LuaStr02 States`_.

The second part of regexp(``(_?)\s*``) captures ``_`` on group 1 and collect
any following spaces/tabs (without storing them in groups).

The third part of regexp (``\[(=*)\[``) captures all equal symbols placed 
between the two brackets and store them into group 2.

The fourth part of regexp (``(.*?)``) captures all characters contained between
the lua bracketed string delimiters (*ending delimiter is defined by the last
part of the regexp*). It captures the less charcaters than possible until the
end delimiter found

The last part of regexp (``]\2]``) will search the right lua bracketed string
end delimiter, checking how many equals symbols were captured on group 2 
(``\2`` will search exactly what group 2 matched). So, if the group 2 is an
empty string, than ``]]`` will be the end delimiter searched by regexp. 
If the group 2 is ``===`` (3 equals symbols) than the end delimiter will be
``]===]``... and so on.

.. note::
 
  This regexp, unlike the one used on ``LuaStr01`` and ``LuaStr02``, does not
  match at all if the right end-delimiter will be not found in the parsed line.
  This is why lua bracketed strings (lua string type 3) require another state
  that explicitly tells when the lua string type 3 is multiline. 
  And this is the rule defined on LuaStr03o, explained in the next 
  subparagraph.

---------------
LuaStr03o State
---------------

LuaStr03o State will match when the beginning of a lua multiline bracketed
string is found::
   
   ^(?:[^["']*?)(_?)\s*\[(=*)\[(.*)

The state LuaStr03o will capture:
  * on group 1: the ``_`` symbol (if is used)
  * on group 2: how many equal symbols where placed in the *starting string
    delimiter* (for example the delimiter ``[=[`` will contain one equal 
    symbol between the two brackets)
  * on group 3: the text of the first line of the string. This time the group 3 
    use **greedy** rule, capturing all following characters.
    This is why, this time, the regexp will be **True** (will match) even if 
    nothing follows the ``[=[`` marker (multiline string).
                          
.. note::
  
  LuaStr03o, when creating the pending string (PendingLuaString object on
  state machine), stores the amount of equals signs in the 
  PendingLuaString.numequals variable, wich will be used by LuaState30 to
  calculate (on runtime) wich regexp should be actually used.

--------------
State LuaStr30
--------------

The LuaStr30 is a very particular state, wich is structured as an always-run 
state, but it works like a standard state.

The regexp definition, infact, is not placed (as usual) in the State.regexp
parameter, defined in the __init__ function. This becouse all states are
stored in the state machine during the setup phase, before starting to parse
WML and Lua files. Wich means that all State.regexp values can be defined only
on the setup phase itself and they cannot change anymore.

But, this time, we require to use a regexp rule that search exactly wich is
the end delimiter for that one lua bracketed multiline string started on the
previous LuaStr03o state.

This why the regexp is defined directly in the run() function, wich explicitly
performs all actions usually done by statemachine when evaluating a 
State.regexp.

This is the regexp that will be evaluated in the run() function::
    
   ^(.*?)]={n}]

where ``n`` is the exact number of equals symbols stored in the
PendingLuaString.numequals variable by LuaStr03o.

So, for example, if LuaStr03o.regex previously matched ``==`` on group 2 (wich
means that ``[==[`` was the opening delimiter used), then the regexp searched
by the run function will be::
  
  ^(.*?)]={2}]

Now it is the time to actually explain the regexp. We will focus the 
explaination around this last concrete example (end delimiter must have exactly 
two equal symbols between close brackets). So why, from now on, we will 
explain the regexp::
  
  ^(.*?)]={2}]

This regexp will match if the line contains somewhere the ``]==]`` delimiter.
the final part of the regexp (``]={2}]``), infact, means:
  
  * litteral ``]``
  * followed by ``=`` (two times)
  * followed by ``]``

If the delimiter ``]==]`` will be found, the regexp will match, the last part
of the string will be stored on group 1, than it will be added to the pending
string. LuaStr30 will go to LuaIdleState (parsed line will be not completely 
consumed. Only what it will be matched will be removed from the parsed line.

If the delimiter ``]==]`` will not be found, than the regexp will not mach.
LuaStr30 will store all the parsed line into the pending lua string and consume
it at all, so the statemachine will be able to read the next line of code. 
LuaStr30 will come back again to itself (it acts like a recursive state, in a
very similar way like the LuaStr10 and LuaStr20 states).

.. note::
  
  The first part of the regexp ``(.*?)`` capture all characters using the
  **less greedy than possible** rule, with the same effects explained on
  `State WmlStr01`_ (first part of the regexp where the *less greedy* rule
  was used).
  

-------------
LuaFinalState
-------------

Lua Final States checks if the current parsing line contains a function name:

.. code-block:: python
   
   rx_str = ( r'function\s+([a-zA-Z0-9_.]+)|' +
                   r'([a-zA-Z0-9_.]+)\s*=\s*function'
            )
   rx = re.compile(rx_str, re.I)
   m = re.search(rx, xline)
   
So it use ``re.search`` and not ``re.match`` as usual. This mean that we 
don't have a sort of an implicit caret symbol at the start of the regexp rule,
so the resulting regexp rule is::
    
   function\s+([a-zA-Z0-9_.]+)|([a-zA-Z0-9_.]+)\s*=\s*function
   
.. note:: 
   
   the regexp showed above is **case insensitive** (option ``re.I`` used on
   ``re.compile`` function).

the regex will search:
   
   * **function** <*name_of_function*>: where <*name_of_function*> will be 
     stored on group 1.

**or** it will search:
   
   * <*name_of_function*> = **function**: this time <*name_of_function*> will
     be stored on group 2.

=======================
"*Escape*" regexp rules
=======================

Translatable strings will be "reformatted" two times. The first time when they
will be stored from pending string to a ``PoCommentedString`` (or to a 
``WmlNodeSentece``)  object.

.. code-block:: python
   
   # ./pywmlx/state/machine.py (class PendingLuaString, function store)
   if self.luatype == 'luastr2':
       self.luastring = re.sub(r"\'", r"'", self.luastring)
   self.luastring = re.sub(r'(?<!\\)"', r'\"', self.luastring)
   
   # --------------------------------------
   
   # ./pywmlx/state/machine.py (class PendingWmlString, function store)
   self.wmlstring = re.sub('""', '"', self.wmlstring)

Those part of code will be replace the *escaped quote* found in that kind of
string (``""`` on WML and ``\"`` on Lua type 1 for symbol ``"``; ``\'`` on
Lua type 2 for symbol ``'``).

Those escape code will be replaced in those way:
   
   * ``""`` found on WML will be replaced by ``\"``
   * ``"``, if not preceded by ``\`` will be replaced by ``\"``, on lua string
   * ``\'``, found on Lua type 2, will be replaced by ``'``.
 
 This becouse, in the final .po file the quote string ``"`` must be escaped by
 ``\``, so the right escape code is ``\"``. The ``'`` symbol, instead, don't
 require any escape.
 
 So it's the time to explain the regexp used on lua to verify if a ``"`` symbol
 is not preceded by ``\``::
 
    (?<!\\)"
  
This is the regexp rule used by the last ``re.sub`` used by the function
``PendingLuaString.store()``.

the ``(?<!\\)`` is a **negative look-before** rule. So the regex will match if
the ``"`` is found, but if the previous character is not ``\`` infact:
    
    * ``(?<! )`` identify the negative look-before
    * ``\\`` checks for the litteral character ``\``.

We said that the translatable string is "reformatted" two times.

   * the first time, when a new ``PoCommentedString`` or ``WmlNodeSentece`` 
     object is stored in memory.
   * the second time when every single ``PoCommentedString`` object contained
     in the dictionary will be written in the .po file, rightly before actually
     writing it.
     
On this last step the sentence will be translated from::
    
   this is the \"sentence\" before second formatting
   
to::
    
   "this is the \"sentence\" before second formatting"

If the string is multiline, for example::
   
   this is
   a \"multiline\" string
   stored here
   
they will be formatted to::
   
   ""
   "this is\n"
   "a \"multiline\" string\n"
   "stored here"

It is possible to notice that, on multiline string, the new "formatting" will
create a first line with only ``""``. It is not an error: it is expected since,
if the string is multiline, it is expected that ``""`` will follow ``msgid``
on the first line.

All other lines (except the very last one) will end with ``\n`` (new line
code).

All lines (included the very last one) will be enclosed in quotes (``"``).

