Introduction
************

This part of the documentation is useful also for end-users not interested to
learn how the source code internally work.

=============
Pros and Cons
=============

wmlxgettext 2.x (this version), compared with wmlxgettext 1.0 (the old perl
script), has its **pros**:
    
   * More flexible command line (the old one is however supported).
   * More explicit (and more understandable) warning/error messages returned
     to the end user.
   * Optionally, can display a warning message if a WML macro is found into a 
     translatable string (translatable string with WML macro will never be
     translated)
   * Supports ``[==[`` and ``]==]`` markers for Lua multi-line strings
   * Strings captured on a .lua file is reported to its **right** line of code
   * Any file reference is written in a single line (like expected in a .po 
     file)
   * Can be used also on windows (requires python 3.x, however)
   * User is not forced to list, one by one, every file that wmlxgettext must
     parse, but it can use instead the new ``--scandirs`` option.
   * Can be added to the python GUI for (used by all other wesnoth tools)
   * The code, even if complex and long, is more modular, and could be 
     fixed/changed/forked in an easier way
   * wmlxgettext 2.x sources are **very deeply** documented here.
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
   * execution speed is slower.
   * The output created by wmlxgettext 2.x is not exactly the same as the one
     created by wmlxgettext 1.0 (very small differences, however, nothing 
     really important).
     
====================
The new command line
====================

wmlxgettxt 2.x could be invoked in the classical way::
   
   ./wmlxgettext --domain=DOMAIN --directory=DIRECTORY [FILELIST] > file.po
   
this syntax is required by wesnoth in order to build the ``pot`` target. 
However this syntax must be considered deprecated for UMC developers.

This other syntax is suggested, instead::
    
   ./wmlxgettext -o file.po --domain=DOMAIN --directory=DIRECTORY [FILELIST]

Or, even better::
   
   ./wmlxgettext -o file.po --domain=DOMAIN --directory=YOUR_ADDON_DIRECTORY --recursive

Using those last two syntaxes, infact, the file ``file.po`` is directly created 
by wmlxgettext instead of redirecting the output from ``stdout`` to the 
desired file.

If you use the last syntax, wmlxgettext will scan for you (recursively) your
addon main directory and automaticly collect all .cfg and .lua files without
any need to list them one-by-one.

Moreover, wmlxgettext 2.x, supports more options, that can be listed with: 
    
   ``./wmlxgettext --help``
    
The most useful added options are:
    
    * ``--fuzzy``: allows to create a .po file with all fuzzy strings
    * ``--warnall``: show optional warnings

==============
Output "lacks"
==============

The .po file created with wmlxgettext 2.x may store the sentences in a 
different order. This becouse the list of the files could be read in a 
different order. However, every translatable string related to the same file is
stored in the right order.

Lua function information (inside a .lua file or inside a lua code inside a WML 
file) is more verbose (it is not so good as it may sounds, unluckly). 
Wmlxgettext 2.x remembers some function names that wmlxgettext 1.0 forgets.

