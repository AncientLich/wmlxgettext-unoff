Comparing perl vs python versions
*********************************

wmlxgettext 2.x (this version), compared with wmlxgettext 1.0 (the old perl
script), has its **pros**:
    
   * More flexible command line (the old one is however supported).
   * More explicit (and **more understandable**) warning/error messages 
     returned to the end user.
   * Optionally, can display a warning message if a WML macro is found into a 
     translatable string (translatable string with WML macro will never be
     translated)
   * Recognizes and captures lua bracketed strings
   * Strings captured on a .lua file are reported to their **right** line 
     of code
   * Additional comments for translators are added to the **right sentence
     only**, avoiding to display it where it should not appear.
   * Any file reference is written in a single line (like expected in a .po 
     file)
   * Can be used **also on windows** (requires python 3.x, however)
   * User is not forced to list, one by one, every file that wmlxgettext must
     parse, but it can use instead the new ``--scandirs`` option.
   * Can be added to the python GUI for (used by all other wesnoth tools)
   * The code, even if complex and long, is more modular, and could be 
     fixed/changed/forked in an easier way
   * wmlxgettext 2.x sources are **very deeply** documented, in the
     :ref:`srcdoc_index`.
   * Supports another custom directive: ``# po-override:`` that allows you to 
     override the automated WML/Lua list of informations, replacing it with
     your own custom message. The ``# po:`` directive is still available,
     since it allows you to ADD informations directed to the translator, 
     WITHOUT touching the automated WML/Lua list of informations. ``# po:`` and
     ``# po-override:`` directives can be used together on the same 
     translatable string. However only ONE occurrence of ``# po-override:`` can
     be defined for every translatable string.

But it has also its **cons**:
   * code is much more huge (about 1400 lines of code splitted in several files)
     against the 300-400 lines of code required by the perl version
   * execution speed is a bit slower.
   * The output created by wmlxgettext 2.x is not exactly the same as the one
     created by wmlxgettext 1.0 (very small differences, however, nothing 
     really important).
     
In the following paragraphs of this page we will show deeply some of the 
differences listed here above (only the most important ones that affect the
resulting output .po file) from this rewritten version of wmlxgettext (2.x) vs 
the old version of wmlxgettext (1.0)

==================================================
Error/Warning Messages are more understandable now
==================================================

All type of error messages displayed by wmlxgettext 2.x is clear and intuitive,
unlike the error messages displayed by perl wmlxgettext (1.0).
We will show here only an example about what happens when unbalanced tags are 
found by perl wmlxgettext (1.0) and by python wmlxgettext (2.x). 

We will use this WML file (ztest.cfg)::
    
  #textdomain wesnoth-mytest
  
  # WML with unbalanced tag [scenario] ---> parsing this file will return an error
  [scenario]
     id=my_scenario

As you can see the [scenario] tag is not closed, so both perl wmlxgettext (1.0)
and python wmlxgettext (2.x) will return an error.
Here is the error message displayed by perl wmlxgettext (1.0)::

  non-empty node stack at end of ztest.cfg at ./wmlxgettext line 203, <FILE> line 5.
  WML seems invalid for ztest.cfg, node info extraction forfeited past the error point at ./wmlxgettext line 210.

Here, instead, is the most user-friendly error message displayed by python
wmlxgettext (2.x)::
  
  error: ztest.cfg:5: End of WML file reached, but some tags were not properly closed.
  (nearest unclosed tag is: [scenario])

========================================================================
Additional comments for translators are added to the right sentence only
========================================================================

Additional comments for translator are additional informations useful to
instructs translators how to translate better a particular sentence.
Here we analyze the _main.cfg file of the mainline campaign Liberty (focus your
attention at lines from 22 to 27):
    
.. code-block:: none
  :linenos:
  :emphasize-lines: 22-27
  
  #textdomain wesnoth-l
  # This version forked from 1.2, 2/10/2007, and prepared for mainline by ESR
  [textdomain]
     name="wesnoth-l"
  [/textdomain]
  
  # wmlscope: set export=no
  [campaign]
    id=Liberty
    name= _ "Liberty"
    abbrev= _ "Liberty"
    rank=110
    first_scenario=01_The_Raid
    define=CAMPAIGN_LIBERTY
    icon="units/human-outlaws/fugitive.png~RC(magenta>red)"
    image="data/campaigns/Liberty/images/campaign_image.png"
  
    {CAMPAIGN_DIFFICULTY EASY   "units/human-peasants/peasant.png~RC(magenta>red)" ( _ "Peasant") ( _ "Easy")} {DEFAULT_DIFFICULTY}
    {CAMPAIGN_DIFFICULTY NORMAL "units/human-outlaws/outlaw.png~RC(magenta>red)" ( _ "Outlaw") ( _ "Normal")}
    {CAMPAIGN_DIFFICULTY HARD   "units/human-outlaws/fugitive.png~RC(magenta>red)" ( _ "Fugitive") ( _ "Difficult")}
  
    #po: Yes, that is "marchlanders", not "marshlanders".
    #po: "marchlander" is archaic English for an inhabitant of a border region.
    # wmllint: local spelling marchlanders
    description= _ "As the shadow of civil war lengthens across Wesnoth, a band of hardy marchlanders revolts against the tyranny of Queen Asheviere. To win their way to freedom, they must defeat not just the trained blades of Wesnothian troops but darker foes including orcs and undead.

  " + _"(Intermediate level, 8 scenarios.)"
  
    [about]
        title = _ "Campaign Design"
        [entry]
            name = "Scott Klempner"
        [/entry]
    [/about]
    [about]
        title = _ "Prose-doctoring and preparation for mainline"
        [entry]
            name = "Eric S. Raymond (ESR)"
        [/entry]
    [/about]
    [about]
        title = _ "Campaign Maintenance"
        [entry]
            name = "Eric S. Raymond (ESR)"
            comment = "current maintainer"
        [/entry]
        [entry]
            name = "Lari Nieminen (zookeeper)"
            comment = "current maintainer"
        [/entry]
    [/about]
    [about]
        title = _ "Artwork and Graphics Design"
        [entry]
            name = "Brendan Sellner"
        [/entry]
        [entry]
            name = "Kathrin Polikeit (Kitty)"
            comment = "portraits"
        [/entry]
        [entry]
            name = "Shadow"
        [/entry]
        [entry]
            name = "Blarumyrran"
            comment = "story images, Rogue Mage line sprites"
        [/entry]
        [entry]
            name = "Sonny T Yamada (SkyOne)"
            comment = "Sprite animations (defense and attack) of Rogue Mage line"
        [/entry]
    [/about]
  [/campaign]
  
  #ifdef CAMPAIGN_LIBERTY
  
  [binary_path]
     path=data/campaigns/Liberty
  [/binary_path]
  
  {campaigns/Liberty/utils}
  {campaigns/Liberty/scenarios}
  
  [+units]
      {campaigns/Liberty/units}
  [/units]
  
  #endif
  
  # wmllint: directory spelling Grey Relana Helicrom Fal Khag

As you can see, at line 22 and 23, there are two ``#po:`` special comments wich
add the additional information for translator about the usage of the 
"marchlanders" word. It is an explaination related to the sentence used in the
description of the campaign where the "marchlanders" word is actually used.

So, in this case, you espect that the additional information is added only at
the description string::
  
  "As the shadow of civil war lengthens across Wesnoth, a band of hardy marchlanders revolts against the tyranny of Queen Asheviere. To win their way to freedom, they must defeat not just the trained blades of Wesnothian troops but darker foes including orcs and undead.
  "

Whell... perl wmlxgettext (1.0) add too many additional informations, as 
it showed here:

.. code-block:: none
  :linenos:
  :emphasize-lines: 52-59
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:10 _main.cfg:11
  msgid "Liberty"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:18
  msgid "Easy"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:18
  msgid "Peasant"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:19
  msgid "Normal"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:19
  msgid "Outlaw"
  msgstr ""

  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:20
  msgid "Fugitive"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:20
  msgid "Difficult"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:25
  msgid ""
  "As the shadow of civil war lengthens across Wesnoth, a band of hardy marchlanders revolts against the tyranny of Queen Asheviere. To win their way to freedom, they must defeat not just the trained blades of Wesnothian troops but darker foes including orcs and undead.\n"
  "\n"
  ""
  msgstr ""
  
  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:27
  msgid "(Intermediate level, 8 scenarios.)"
  msgstr ""

perl wmlxgettext print the additional information not only in the right 
sentence (where the code is emphatize, that is the only point where the 
additional information should be added: [line: 52-59]),
but also print the additional info where it makes no sense, for example on 
msgid "Difficult" (where the detail about the usage of "marchlanders" word is
useless).

This functionality, instead, work correctly on python wmlxgettext (2.x):

.. code-block:: none
  :linenos:
  :emphasize-lines: 37-43
  
  #. [campaign]: id=Liberty
  #: _main.cfg:10
  #: _main.cfg:11
  msgid "Liberty"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:18
  msgid "Peasant"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:18
  msgid "Easy"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:19
  msgid "Outlaw"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:19
  msgid "Normal"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:20
  msgid "Fugitive"
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:20
  msgid "Difficult"
  msgstr ""

  #. [campaign]: id=Liberty
  #. Yes, that is "marchlanders", not "marshlanders".
  #. "marchlander" is archaic English for an inhabitant of a border region.
  #: _main.cfg:25
  msgid ""
  "As the shadow of civil war lengthens across Wesnoth, a band of hardy marchlanders revolts against the tyranny of Queen Asheviere. To win their way to freedom, they must defeat not just the trained blades of Wesnothian troops but darker foes including orcs and undead.\n"
  "\n"
  ""
  msgstr ""
  
  #. [campaign]: id=Liberty
  #: _main.cfg:27
  msgid "(Intermediate level, 8 scenarios.)"
  msgstr ""

As you can see, this time the additional information is added **only** when it
is expected to be stored (on the sentence where the "marchlanders" word 
is used). 