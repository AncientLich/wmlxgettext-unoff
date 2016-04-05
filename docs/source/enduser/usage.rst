wmlxgettext: how to run
***********************

The previous chapter explained how to write a WML and a Lua file in the right
way:
   
   * Avoiding unwanted errors using the special comment ``# wmlxgettext:`` on
     WML code when you need to use unbalanced tags
   * Customizing the message informations displayed to the translator using
     the special comments ``# po:`` and ``# po-override:``
   * And remembering the ``#textdomain`` directive usage.

So we can assume here that all your .cfg and .lua files (*used by your wesnoth
add-on*) are ready to be parsed by wmlxgettext. But how to run wmlxgettext?

wmlxgettext requires to be called using some command line options (unless it 
will included in the wesnoth GUI tool; in that case, you could use the GUI
instead).

Unlike wmlxgettext 1.0 (perl version), this version can be used in **three**
possible ways. They will be explained starting from the most suggested one, 
finishing with the unsuggested one.

The last paragraph, instead, will explain the optional parameters that could
be used in any of the three usages explained in the previous paragraphs.

=======================================
Wmlxgettext with implicit list of files
=======================================

.. note:: 
  
  This is the **only** way that 100% works under windows.
   
You can avoid to explicitly tells what files must be parsed by wmlxgettext.
This is how you can do it on windows::

  c:\<pythondir>\python wmlxgettext --domain=DOMAIN_NAME --directory=YOUR_ADDON_DIRECTORY --recursive -o ./FILENAME.po

On linux/mac, you can simply use::
  
  ./wmlxgettext --domain=DOMAIN_NAME --directory=YOUR_ADDON_DIRECTORY --recursive -o ./FILENAME.po

without explicitly call the python 3.x interpreter.

--------------------
--domain=DOMAIN_NAME
--------------------

With the option ``--domain``, wmlxgettext will know wich is the 
``# textdomain`` used by your wesnoth add-on. For example, if your 
_main.cfg will have::
  
  [textdomain]
     name="wesnoth-xyz"
     path="data/add-ons/xyz/translations"
  [/textdomain]

This is what you have to write into the ``--domain`` parameter::
  
  --domain=wesnoth-xyz

---------------------------
--directory=ADDON_DIRECTORY
---------------------------

With the option ``--directory``, wmlxgettext will know the starting path
where all following files/scandirs should be searched.
This is a fake example for windows::

  --directory=c:\games\wesnoth\userdata\data\add-ons\YOUR_ADDON_DIRECTORY

-----------
--recursive
-----------

If ``--recursive`` option is used, wmlxgettext will scan recursively the 
directory typed on the ``--directory`` option and collect all .cfg and .lua
files automaticly::
  
  ./wmlxgettext --domain=domain_name --directory=/home/user/games/wesnoth/userdata/add-ons/Invasion_from_the_Unknown --recursive -o ./file.po

In the example showed above, infact, wmlxgettext will watch the directory 
``/home/user/games/wesnoth/userdata/add-ons/Invasion_from_the_Unknown``
and it will collect, recursively, all .cfg / .lua files inside that 
directories (and subdirectories). 

----------------
-o [OUTPUT_FILE]
----------------

If you use this option, wmlxgettext will actually create a .po file, saving it
as ``[OUTPUT_FILE]``.

The ``-o`` options accepts: 
  
  * either a file name with absolute path
  * or a file name with relative path (for example: ``./output.po``)
  
Also the parameter ``--directory`` discussed before can accept both an
absolute path or a relative path starting from the current working directory
(for exaple: ``--directory=.`` will assign to the ``--directory`` option the
path of the current working directory).
  
=======================================
Wmlxgettext with explicit list of files
=======================================

.. note:: 
  
  This method can work on windows **only if** the list of files is not very
  long (windows cannot read a very-long command line). 
  Under windows is **highly** suggested to use the method described
  in the previous paragraph (`Wmlxgettext with implicit list of files`_)
   
Instead of delegating to wmlxgettext the job for you, you can explicitly tells
the complete list of files that wmlxgettext must parse::
  
  ./wmlxgettext --domain=domain_name --directory=/home/user/wesnoth/userdata/add-ons -o ./file.po Invasion_from_the_Unknown/_main.cfg Invasion_from_the_Unknown/other.cfg [...]

As the example shows, it is **highly suggested** to put the list of files 
**after** all other options. This is why, in this case, the option 
``-o ./file.po`` is written before the file list starts.

Every file listed in list must be written as a relative path starting from the
``--directory`` directory. 

So, coming back to the example showed above:
  
  * ``--directory`` is ``/home/user/wesnoth/userdata/add-ons``
  * file n.1 is ``Invasion_from_the_Unknown/_main.cfg``
  * file n.2 is ``Invasion_from_the_Unknown/other.cfg``.
  
This means that those two files will be searched and parsed:
  * /home/user/wesnoth/userdata/add-ons/Invasion_from_the_Unknown/_main.cfg
  * /home/user/wesnoth/userdata/add-ons/Invasion_from_the_Unknown/other.cfg

.. note::
  
  DON'T use the ``--recursive`` option if you want to explicitly tell the 
  list of the files to parse. If the option ``--recursive`` is used, the 
  explicit list of file will be ignored.


==============================================================
Wmlxgettext with explicit list of files and output redirection
==============================================================

This is the **unsuggested** way to use wmlxgettext.

This syntax is supported only becouse wmlxgettext 2.x must be 
retro-compatible with the syntax used in past by wmlxgettext 1.0.

This syntax is to be considered **deprecated** and it should be used **only** 
by scons/cmake or autotools when buinding the core source... in brief words:
if you are a person who is developing his own wesnoth-addon **NEVER** use this
syntax.

The syntax is, more or less, the same showed in the previous paragraph, but
this time we don't directly create the .po file, but the .po file will be
written in console (stdout), wich redirect the output to the .po file::
  
  ./wmlxgettext --domain=domain_name --directory=/home/user/wesnoth/userdata/add-ons Invasion_from_the_Unknown/_main.cfg Invasion_from_the_Unknown/other.cfg [...] > ./file.po

Well... at a first look we could think there is actually no difference from
this syntax and the syntax showed before.

But it is not true: there is a huge difference:
  
  * if you use the ``-o`` option, you will let wmlxgettext to directly create
    for you the output file, wich will be correctly written using the
    ``UTF-8`` format, as expected by wesnoth
  * if you don't use the ``-o`` option, like showed here, the output will be
    printed to the console (stdout), wich will use its own text codify, 
    wich may leads to critical problems. The output redirection cannot fix
    those issues, if they happen.

This is expecially true under windows, where this last syntax **will never
work** (python will stops returning a traceback error).

So... **NEVER** use output redirection, but use instead the ``-o`` option.

===================
Optional parameters
===================

.. note:
  
  All options discussed here can be used in all the three usages explained
  in the previous paragraphs.

Wmlxgettext 2.0 supports also other optional parameters, not explained in the 
previous paragraphs:
  
  * ``--warnall``: if used, wmlxgettext will show also optional warnings.
  * ``--fuzzy``: if used, all sentences stored in the .po file will be
    marked as fuzzy. (By default, sentences will be **not** marked as fuzzy).
  * ``--package-version``: With this option, you can immediatly print the
    package version number into the .po header infos. Usually you will 
    add manually this info, so it is more an "easter egg" than a feature.
  * ``--no-ansi-colors``: if you use this flag, you disable colors shown
    in linux/mac console when a warning/error message occurs (windows will not 
    display colors). This option will become useful if wmlxgettext will be 
    added to the python GUI for wesnoth tools (since the ansi escape colors 
    could be not desired by the GUI)
  
Finally there is a last option, that an end-used should **never** use:

  * ``--initialdomain=INIT_DOMAIN``: It tells the name of the 
    current domain when no ``#textdomain`` still found in .cfg/.lua file.
    By default it is ``wesnoth`` (and don't need to be changed).

