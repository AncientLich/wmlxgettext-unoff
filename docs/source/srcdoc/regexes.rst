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

.. code-block:: python
   
   self.regex = re.compile(r'\s*\[\s*([\/+-]?)\s*([^\]]*?)\s*\]')

At the **start of the string** will search for:
   
   * spaces/tabs (from 0 to n)
   * the character ``[``
   * spaces/tabs (from 0 to n)
   * **zero or one** of any of this signs: ``\``, ``/`` or ``-``. If one of 
     this character is used, it is captured into group 1.
   * spaces/tags (from 0 to n)
   * any number of any kind of character **different from** ``]``. This is the
     (open/close) tagname and it will captured into group 2.
   * and finally the character ``]``

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
   
   rx = r'(?:[^["' + r"'" + r']*?)(_?)\s*"((?:\\"|[^"])*)("?)'
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


-----------------------------
LuaStr03 and LuaStr03o States
-----------------------------

LuaStr03 regexp can is equal to the following regexp rule::
   
   ^(?:[^["']*?)(_?)\s*\[==\[(.*?)]==]
        
The first part of regexp (``^(?:[^["']*?)``) is already explained in
`LuaStr01 and LuaStr02 States`_.

The second part of regexp(``(_?)\s*``) captures ``_`` on group 1 and collect
any following spaces/tabs (without storing them in groups).

The third part of the regexp (``\[==\[(.*?)]==]``) capture all characters
contained in ``[==[`` and ``]==]`` delimiters, storing them in group 2 (text).

   * the group ``(.*?)`` captures less characters than possible until the
     ``]==]`` end-delimiter is found
   * wich means that the regexp is **False** (does not match) if it is a 
     multi-line string (where the delimiter ``]==]`` is not in the current
     parsed line, bit it will be found in another following line of the parsed
     file).

This is why, unlike ``LuaStr01`` and ``LuaStr02`` it was needed an explicit
rule when the lua string type 3 is multiline. And this is the rule defined
on LuaStr03o::
   
   ^(?:[^["']*?)(_?)\s*\[==\[(.*)

The state LuaStr03 will capture, on group 1, the ``_`` symbol (if is used), and
on group 2, ALL characters AFTER the ``[==[`` delimiter.
This time the group 2 use **greedy** rule, capturing all following characters.
This is why, this time, the regexp will be **True** (will match) even if 
nothing follows the ``[==[`` marker (multiline string).
                          
--------------
State LuaStr30
--------------

The regexp used by LuaStr30 (is multiline string type 3 closed?) from line 2
of a multi-line string behave differently than the other multi-line states
seen before::
    
   ^(.*?)]==]

The idea is very similar to the one used by LuaStr03 state. It collects all
characters before ``]==]`` using the "**less greedy than possible**" rule.
Those characters will be stored on group 1.

This also mean, like explained in the previous subparagraph, that the regexp 
**does not match** if the ``]==]`` marker was not found.

So:
   
   * if the ``]==]`` marker is found, regexp will match and group 1 will 
     contain the last line of the multi-line string to add to the pending 
     string
   * if the ``]==]`` marker is **not** found, regexp will **not** match and
     statemachine will go to the **iffail** State (LuaStr31)
   * so why, LuaStr31 is required to store all middle-lines of the multi-line
     string type 3. LuaStr31 (always-run state) will store all the file line
     in the multiline string, than consume the string, and come back to 
     LuaStr30 state.

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

