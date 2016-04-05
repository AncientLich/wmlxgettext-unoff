.. _wmllua_intro:

Introducing WML and Lua parser
******************************

Wmlxgettext parse .lua and .cfg (WML) files line-by-line through his own 
Finite State Machine (Deeply explained in the chapter :ref:`The State Machine`).
                          
This chapter, instead, will explain, in general, how differently WML and Lua 
codes are managed, and it will explain also:
   
   * ``PoCommentedString`` class (module: ``./pywmlx/postring.py``)
   * ``WmlNode`` class (module: ``./pywmlx/postring.py``)
   * ``WmlNodeSentence`` class (module: ``./pywmlx/postring.py``)
   * the ``./pywmlx/nodemanip.py`` module

========================
WML parsing fundamentals
========================

WML (Wesnoth Markup Language) is a "*tagged*" language, like XML.
Every .cfg (WML) file contains a list of nested [tags] wich must be properly 
closed. Here is a (fake) example of a WML file::
   
   #textdomain your-textdomain-name
   [scenario]
      id=scenario_id
      name= _ "scenario name (translatable)"
      map_data = ...

      [objective]
          description= _ "objective text (translatable)"
      [/objective]

      [event]
        name = "start"
        
        [message]
           message = _"I am saying something (translatable)"
           speaker = id_of_the_speaker
        [/message]
        
      [/event]
   [/scenario]

wmlxgettext must collect all translatable strings, and must keep all important
infos contained inside every opened tag. For example, look at the following
tag::
   
   [message]
      message = _"I am saying something (translatable)"
      speaker = id_of_the_speaker
   [/message]
   
wmlxgettext must remember that the translatable string 
*"I am saying something (translatable)"* appeared at line 15 of your file
``some-file.cfg``, inside a ``[message]`` tag with 
``speaker=id_of_the_speaker`` and store properly those infos into the .po 
file.

Since the State Machine parser reads any file line-by-line, it is required to
store in memory all those infos, on **memory nodes**

=========
WML nodes
=========

Everytime a new open tag is found, a new node is added in memory.

.. note::
   
   All the three cases showed here are managed in the same way. A new [tag] 
   node is always created:
   
   * [tag]  --> A new standard [tag] is opened.
   * [+tag] --> A new updating [tag] is opened.
   * [-tag] --> Another possible syntax
   
   (+ and - starting sign will be ignored)
   
When a ``[tag]`` node has to be added in memory, a new ``WmlNode`` object is
created and added in memory.

A ``WmlNode`` object will contain those data infos:
    
    * **tagname**: name of tag (it will be saved as *"[tagname]"*)
    * **fileref**: filename containing the node (relative path)
    * **fileno**: unique **id value** assigned by wmlxgettext for current file
    * **sentences**: list of translatable strings found inside the node, stored
      as WmlNodeSentence objects
    * **wmlinfos**: list of wml infos (example: ``speaker=id_of_the_speaker``).
    * **autowml**: usually ``True``. If ``False`` the ``wmlinfos`` list will
      be not used.

This node will be closed when the right *"tag-end-markup"* (``[/tag]``) will 
be found.

The class ``WmlNode`` also provides some functions that will be discussed later.

----------------------------
Storing translatable strings
----------------------------

When a translatable string will be found, it will be added in the current node.

Each time a new translatable string found, a new ``WmlNodeSentence`` object 
will be added to the current WML node (but only if the current domain is equal 
to the addon domain).

A ``WmlNodeSentence`` will have those properties:
   
   * **sentence**: the translatable string (text)
   * **ismultiline**: ``True`` if it is a multi-line string
   * **lineno**: line number where the translatable string was located. (if
     multi-line, the line number where the the string started).
   * **lineno_sub**: The name is ambigous. This parameter (integer value) is a 
     progressive value, expecially useful when more than one string was stored
     in the same line of the same file.
   * **overrideinfo**: ``None`` or *'string'*. If 
     ``# po-override: overrideinfo`` directive was found, the overrideinfo will
     be stored here.
   * **self.addedinfo**: ``None`` or *list of strings*. If one or more
     ``# po: addedinfo`` directive(s) found, the info will be added in this
     list.

=======================
The postring dictionary
=======================

Writing a .po file is the final objective of wmlxgettext. Every translatable
string in a .po file must appear **one time only**, and must contain all 
important useful infos (auto-captured infos and added infos by
the UMC developer with ``# po: addedinfos`` directive in .cfg file source).

Python dictionaries are pair of values (key, value) where *'key'* is **always**
unique. Moreover it will allow to quickly search if a translatable string was
already stored in memory.

This dictionary is:
    
.. code-block:: python
   
   # ./wmlxgettext:144
   sentlist = dict()

wich is also known and managed by the state machine parser (wich is discussed
in the next chapter).

The dictionary contains all sentences that wmlxgettext will actually write in 
the .po file
   
   * **key**: the key is a copy of the plain sentence (using only lower 
     letters). Since it is expected that all wesnoth extensions will use 
     english in their .cfg files the string.lower() python function was used
     here.
   * **value**: the value is the sentence, with all additional infos that will
     be written in the .po file. This value is a ``PoCommentedString`` object.
     
So, before actually writing the .po file, wmlxgettext needs to create and 
update its dictionary of ``PoCommentedString`` objects.

.. _PoCommentedString_conv:

===============================================
Converting WmlNodeSentence to PoCommentedString
===============================================

When wmlxgettext parse a WML file, it must store WML nodes in memory.
Each ``WmlNode`` object may contain (or not) one or more translatable strings,
stored in ``node.sentences`` list (list of ``WmlNodeSentence`` objects).

Each time a WML node is closed, before removing the node from memory, 
wmlxgettext will look at the ``WmlNode`` object, checking if it contains
``WmlNodeSentence`` objects or not.

Every ``WmlNodeSentence`` object contained in ``WmlNode`` object will be 
converted in a temporary ``PoCommentedString`` thank of the  
``nodesentence_to_posentence`` function provided by ``WmlNode`` class.

This function is very complex, since it must assemble a ``PoCommentedString``
searching the required values in different places:
   
   * some infos are stored in the ``WmlNode`` itself
   * other infos are stored in ``WmlNode`` itself, but must be *"assembled"*.
   * other infos are stored in the single ``WmlNodeSentece`` contained in the 
     ``WmlNode`` object.

----------------------------
PoCommentedString data infos
----------------------------

Now it is time to explain all data infos contained in a ``PoCommentedString``:
   
   * **sentence** = translatable string text.
   * **wmlinfos** = list of wmlinfos.
   * **addedinfos** = infos added with ``# po: something`` directives
   * **finfos** = list of files and line number where any occurence of the 
     string was found.
   * **orderid** = it is an (unique) tuple of three values:
      * *fileno*: the file where the string was found the first time (file 
        with lower fileno id value.
      * *lineno*: the line numeber, in *fileno*, where the string was found 
        the first time.
      * *lineno_sub*: line_sub is a progressive value. It will be helpful to
        assign the correct order of the sentences, when two or more sentences
        were stored in the same file and in the same line.
   * **ismultiline** = ``True`` if it is a multiline string.

The **orderid** tuple is very important, becouse, when wmlxgettext must write 
down all ``PoCommentedString`` objects from the "*postring*" dictionary to the
.po file, it must print them in the right order (and not randomly):

.. code-block:: python
   
   # ./wmlxgettext:196
   for posentence in sorted(sentlist.values(), key=lambda x: x.orderid):
   
When converting a ``WmlNodeSentence`` object to a ``PoCommentedString`` object, 
``WmlNode.assemble_orderid`` create the tuple of three values to pass to 
``PoCommentedString.orderid`` parameter:
   
   * **fileno** (first value) --> comes from the ``WmlNode`` object containing 
     the ``WmlNodeSentence``.
   * **lineno** and **lineno_sub** --> comes from the single 
     ``WmlNodeSentence``.

``PoCommentedString`` and ``WmlNode`` both have a ``wmlinfos`` list,
but they are conceptually different:
   
   * ``WmlNode.wlinfos`` contains **single pieces** of infos captured
     on the WML node (example: ``speaker=speaker_name`` or ``id=value``).
   * Those single pieces must be assembled (with ``WmlNode.assemble_wmlinfo``) 
     to create a **single** ``PoCommentedString.wmlinfos`` element.
   * So, when converting a ``WmlNodeSentence`` to a ``PoCommentedString``, all
     *wmlinfos* contained in the ``WmlNodeSentence`` will add a **single**
     ``PoCommentedString`` *wmlinfo*.
     
---------------------------------
About overrideinfo and addedinfos
---------------------------------

A ``WmlNodeSentence`` object can contain an override info. This will happen if
``# po-override: overrideinfo`` directive was found in the WML/Lua file.

The override info, if exists, will be written directly on ``PoCommentedString``
as a ``PoCommentedString.wmlinfos`` element. ``WmlNode`` wmlinfos list will be
ignored for that ``WmlNodeSentence`` and ``assemble_wmlinfos`` will not 
executed on that single conversion.

"*Addedinfos*", instead, behave in the same way both in ``WmlNodeSentence`` and
in ``PoCommentedString`` objects. Those are additional infos to display to 
translator. If a ``WmlNodeSentence`` object contains elements in ``addedinfos``
list, those elements will be added in the ``PoCommentedString-addedinfos`` 
list. This will happen if one or more ``# po: addedinfo`` directive(s) was
found in WML/Lua file.

------------------------------------------------------
Create a new dictionary key or update an existing one?
------------------------------------------------------

So, when closing a WML node, all ``WmlNodeSentence`` objects contained in that
``WmlNode`` object will be converted to temporary ``PoCommentedString`` 
objects.

Those temporary ``PoCommentedString`` objects will be not immediately stored
in the dictionary, since the dictionary must contain **one instance only** 
of any sentence.

This why all temporary ``PoCommentedString`` objects created by
``WmlNode.nodesentence_to_posentence`` function will be "scanned".
   
  * If a temporary ``PoCommentedString`` objects contains an instance of an 
    **already existing** translatable string, the dictionary key will be 
    updated (*no new key will be added*). The function
    ``update_with_commented_string`` of the ``PoCommentedString`` object 
    contained in the dictionary key will be executed to update that
    ``PoCommentedString`` object.
  * If a temporary ``PoCommentedString`` object contains a **new** translatable
    string not previously stored in the dictionary, this object will be simply
    added in the dictionary
    
.. code-block:: python
   
   # ./pywmlx/nodemanip.py:15
   def _closenode_update_dict(podict):
       if nodes[-1].sentences is not None:
           for i in nodes[-1].sentences:
               posentence = podict.get(i.sentence.lower())
               if posentence is None:
                   podict[i.sentence.lower()] = ( 
                       nodes[-1].nodesentence_to_posentence(i) )
               else:
                   posentence.update_with_commented_string(
                       nodes[-1].nodesentence_to_posentence(i) )

As you can see this check is actually performed inside the 
``./pywmlx/nodemanip.py`` module, explained in the next paragraph.

.. _nodemanip_module:
  
====================
The nodemanip module
====================

.. note:: 
    
   Until now this chapter explained:
   
   * The structure of WML language and why wmlxgettext use ``WmlNode`` objects
     to store the WML tree structure in memory.
   * ``WmlNodeSentence`` objects: the data type used by ``WmlNode`` objects
     to internally store translatable string(s) found inside the WML node
     stored in memory by that ``WmlNode`` object.
   * ``PoCommentedString`` dictionary: where the translatable strings will be
     stored, as ``PoCommentedString`` objects (where a ``PoCommentedString``
     object describe how actually the translatable string will be writte in
     .po file)
   * ``PoCommentedString`` objects data infos
   * How and when ``WmlNodeSentence`` objects will be converted into
     ``PoCommentedString`` objects

Now it is time to talk about ``./pywmlx/nodemanip.py`` module, the module wich
actually manage when and how to store/clear WML nodes in memory.

Wmlxgettext main script file (*or better, the state machine*), infact, does 
not directly create/delete WML nodes in memory, but it delegates this job to
the ``./pywmlx/nodemanip.py`` module (from now on: ``nodemanip``).

This approach ensure that wmlxgettext internal code will be safer and easier to 
maintain than managing directly nodes in all the part of code where it will 
be required to manipulate WML nodes.

----------------------
Storing a new WML node
----------------------

.. graphviz:: nodemanip01.d

``nodemanip`` stores all WML nodes in a list, and not in a real tree structure.
This becouse, as explained in the very beginning of this chapter, WML language
is structured by **nested tag**, where any new *child* tag must be closed 
before its *parent* tag. Coming back to the WML sample code showed on the
beginning of this chapter (with added comments)::
   
   # [scenario] is the first tag encountered in the WML.
   # [scenario] tag is the parent of all following (nexted) WML tags and
   #            it will be closed after all its child tags
   [scenario]
      id=scenario_id
      name= _ "scenario name (translatable)"
      map_data = ...
      
      # [objective] tag does not have childs, so it will be closed immediately
      # after its opening
      [objective]
          description= _ "objective text (translatable)"
      [/objective]

      # again... [event] tag will have a child: the tag [message].
      # the tag [message] must be closed before the parent [event] tag.
      [event]
        name = "start"
        
        [message]
           message = _"I am saying something (translatable)"
           speaker = id_of_the_speaker
        [/message]
        
      [/event]
   [/scenario]
   
So why WML nodes can be stored in a list:
   
   * everytime a new node is added, we can simply add an element in the list.
     The last item in the list is the last WML node opened.
   * the last node in list, is the current node and it is the node we will must
     close before all other nodes in memory
   * when the current node (last node in list) is closed, it will be removed by
     the list, so the last item on the list (the new current node) will be the
     parent node, for example, look at the WML sample code above:
      
      * when [event] tag is opened a new [event] node is added in node list.
      * when [message] tag is opened, a new [message] node is added in node
        list.
      * when [/message] found, then the [message] node is removed from list and
        the [event] tag will be now the last node in list (current node)

Coming back to the already displayed flow chart, we could notice that there is
a special **ROOT** node that it will be created by nodemanip. It is a fake node
required to avoid memory leaks and it will store all translatable strings 
stored outside any tag (for example a translatable string inside a macro 
definition). All captured ``wmlinfos`` in ROOT node will be ignored, since 
``autowml`` is setted to ``False``.

ROOT node is also special becouse, when created, cannot be deleted until 
the end of the WML file reached.

-------------------------------
Deleting a WML node from memory
-------------------------------

Clearing a WML node is the most important work performed by ``nodemanip`` 
module since, before actually clearing the node from memory, we must verify
if the WML code is correctly written:
   
   * the closing tag ``[/tagname]`` must be equal to the last ``[tagname]`` in
     list (current WML node). Else, a critical error must be returned 
     (calling ``wmlerr`` function - wmlxgettext should stop execution)
   * a critical error should be also returned when a close tag is unexpected at 
     all, since no tags are openend (the list of WML node is still empty **or** 
     the current WML node is the ROOT node).
     
All those checks is done by the ``closenode`` function on ``nodemanip`` module: 

.. code-block:: python
   
   # ./pywmlx/nodemanip.py:73
   def closenode(closetag, mydict, lineno):

But, even if the closing tag ``[/tagname]`` is the expected one, ``nodemanip``
module does not immediately clear the node from the nodes' list.

.. code-block:: python
   
   # ./pywmlx/nodemanip.py:15
   def _closenode_update_dict(podict):
       if nodes[-1].sentences is not None:
           for i in nodes[-1].sentences:
               posentence = podict.get(i.sentence.lower())
               if posentence is None:
                   podict[i.sentence.lower()] = ( 
                       nodes[-1].nodesentence_to_posentence(i) )
               else:
                   posentence.update_with_commented_string(
                       nodes[-1].nodesentence_to_posentence(i) )

.. note::
   
   ``_closenode_update_dict()`` function is internally called by 
   ``closenode()`` function of the ``nodemanip`` module.
   
As previously explained in `Converting WmlNodeSentence to PoCommentedString`_
and all its subparagraphs, infact, ``nodemanip``, before closing the node:
   
   * it will convert all ``WmlNodeSentence`` objects contained into the pending 
     ``WmlNode`` object, before removing it from the list.
   * all the ``PoCommentedString`` temporary values created by the conversion
     will be used to update the dictionary (more details about this process 
     can be found at `Converting WmlNodeSentence to PoCommentedString`_ and 
     all its subparagraphs).

.. graphviz:: nodemanip02.d

----------------------------------------------------------
Adding a new translatable string into the current WML node
----------------------------------------------------------

Every translatable string found inside a WML file must be stored in the
current WML node as a ``WmlNodeSentence`` object.

Every time a new WML file is opened, the node list ``_nodes`` on ``nodemanip``
module is empty (or better, is ``None``).

Usually, a ROOT WML node is created before creating the first actual WML node.
This allows to store translatable strings located outside any tag.

But it could happen that a translatable string is found when node list is still
empty (and when ROOT node does not still exist).

This why the ``nodemanip.addNodeSentence`` function, before trying to add the
translatable string in current WML node, checks if the node list is not empty
(or better, ``is not None``). If the node list is empty, it creates the ROOT
WML node and add the translatable string into that node.

------------------------------------------------
What nodemanip does when end of WML file reached
------------------------------------------------

When end of WML reached, ``nodemanip`` module will run its own ``closefile()``
function. There are three possible cases, as showed in the following flow
chart:

.. graphviz:: nodemanip03.d

Since the root node is not a standard WML node, and since it cannot be closed
by any tag, ``nodemanip`` needs to explicitly explore it when the end of the 
WML file reached (otherwise the translatable strings stored in root node will 
be not added in dictionary).

==============================
Parsing Lua file (or lua code)
==============================

Parsing a lua file (or a .lua code inside a WML file) is somewhat *"easier"*.
Here there is a sample .lua code (on an actual .lua file used by a wesnoth
addon (Invasion from the Unknown) ).

.. code-block:: lua
   
   -- Invasion From The Unknown campaign
   -- note: the original code is slightly different than this one we are
   --       showing in this sample code
   -- original code can be found on file: lua/gui/bug.lua:163
   local function preshow()
        local _ = wesnoth.textdomain('wesnoth-Invasion_from_the_Unknown')
        local msg = _ "An inconsistency has been detected"

        if report then
            msg = msg .. "\n\n" .. _ "Please report this to the maintainer!"
        end
        -- (other code here, omissed)
   end

As the sample code shows, lua is a **procedural** language.
Wmlxgettext does not *"parse"* .lua code, but:
   
   * captures translatable strings, **directly** as ``PoCommentedString`` 
     objects.
   * the only *"wmlinfo"* captured inside a lua code is the last function
     name found in the .lua file

Lua code used on wesnoth add-ons can recognize those directives:
   
   * ``# po: <addedinfo>`` to add infos to write to translators
   * ``# po-override: <override>`` to override wmlinfo

Unlike WML code the textdomain is changed with the line

.. code-block:: lua
   
   local _ = wesnoth.textdomain('wesnoth-Invasion_from_the_Unknown')


.. note::
   
   All *"WML directives recognized by lua code"* showed above must be written
   inside lua comments (introduced by ``--``), like the following code 
   sample::
      
      -- # po: my additional info
   
   You must write **ONE** directive at time, into a new line::
      
      -- this is a good example
      -- # po: my additional info
      
      -- this is, instead, a bad example
      somecode = somevalue -- # po: my additional info

The directive ``# wmlxgettext: <WML code>`` is instead **not** supported in Lua 
code, since it is required by wmlxgettext only when parsing WML code (usually 
that directive is used when it is required to use unbalanced tags, avoiding 
error messages produced by unbalanced tags).

