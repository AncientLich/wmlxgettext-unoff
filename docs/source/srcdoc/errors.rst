Error and Warning messages
**************************

When a WML or a Lua file contains a problem, wmlxgettext returns a warning
(*if the problem is not critical*) or an error (*critical problem*) to the 
end-user to allow him/her to fix his own wesnoth addon.

When wmlxgettext must return an error, it calls ``wmlerr`` function; it calls
``wmlwarn`` function when it should simply display a warning. Both ``wmlerr``
and ``wmlwarn`` function are defined in ``./pywmlx/wmlerr.py`` module.

When importing *pywmlx*, wmlxgettext will import only ``wmlerr`` and 
``wmlwarn`` functions (and ``ansi_setEnabled``), since all other 
classes/functions in ``./pywmlx/wmlerr.py`` module are only internally required 
by ``wmlerr`` and ``wmlwarn`` functions to work properly.

==============================
About ansi_setEnabled function
==============================

When you ``import pywmlx``, also ``ansi_setEnabled`` function is imported from
``./pywmlx/wmlerr.py`` module.

``ansi_setEnabled`` accepts a boolean value (``True`` or ``False``). By default
it is setted to ``True``, but it will be ``False`` if the flag 
``--no-ansi-colors`` was used in the command line:

.. code-block:: python
   
   # ./wmlxgettext:100
   parser.add_argument(
       '--no-ansi-colors',
       action='store_false',
       default=True,
       dest='ansi_col',
       help=("By default warnings are displayed with colored text. You can " +
             "disable this feature using this flag.\n" +
             "This option doesn't have any effect on windows, since it " +
             "doesn't support ansi colors (on windows colors are ALWAYS" +
             'disabled).')
   )
   # ...
   # ./wmlxgettext:141
   pywmlx.ansi_setEnabled(args.ansi_col)

When calling this function, wmlxgettext instructs ``wmlerr`` and ``wmlwarn`` to
use (*or to don't use*) ansi colors when displaying error messages. 
Ansi colors, however, will be displayed only on Posix OSes (Linux and Mac) and
not on Windows, which doesn't support ansi escape codes.

On windows platform, ``ansi_setEnable`` will be interally ignored, and 
warning/error messages will be always displayed non-colored.

============================
wmlerr() and wmlwarn() usage
============================

``wmlerr`` and ``wmlwarn`` functions requires the same parameters and they
will display the error/warning message in the same way.

``wmlerr`` and ``wmlwarn`` requires those two *string* parameters:
    
   * **finfo**: wich is *filename:X* (where *filename* is the 
     .cfg/.lua file that contains the problem, and *X* is the line number of
     that file)
   * **message**: the message to display
   
For example, when printing a warning, the warning message will displayed in
this way::
    
    warning: filename:x: my_message
    
If coloured, "*warning*" will be blue, "*filename:x*" will be yellow, and 
*warning message* will be white. The same colors will be applied to error 
message, except the world "*error*" (wich replace the world "*warning*") that 
will be red.

The last difference:
    
    * ``wmlerr`` stops wmlxgettext execution; 
    * ``wmlwarn``, instead, does **not** stop wmlxgettext execution.

===========================================
How wmlerr() and wmlwarn() internally works
===========================================

``wmlerr`` and ``wmlwarn`` internally behave very differently, since they 
use python Exceptions / warning system.

``wmlwarn`` calls ``warnings.warn`` function, wich was previously 
overridden by ``my_showwarning`` fuction defined in ``./pywmlx/wmlerr.py`` 
module (line 67). Override was possible thank of::
    
    # ./pywmlx/wmlerr.py: 75
    warnings.showwarning = my_showwarning

``wmlerr``, instead, raise a python exception (that could be checked on 
unittest: see `Using unittest with wmlerr()`_) and replace its default 
behaviuour with a custom one.

Python exception system, infact, is very useful while debugging code (it can
trace both errors and warnings), but needed the ovverrides already explained.
This becouse, by default, python shows line code **of the script** (in this 
case: line code of *wmlxgettext* itself) when displaying and warning, and adds 
tracback infos **returned by the script**.

Those kind of infos are completely undersired, since the warnings and errors 
that *wmlxgettext* should return to the end-user, must say only infos that
end-user actually needs (only the errors and messages infos related to WML and 
Lua files parsed by *wmlxgettext*)

Overrides made by ``my_showwarning`` (for warns) and by manually raising an 
exception with a coustom behaviour (in ``wmlerr`` function, when an error
occurs) ensures that errors and messages will show **only** the infos that
are actually expected to be announced to the end-user.

**Both** ``wmlerr`` and ``wmlwarn``, however, internally use 
``dualcol_message(finfo, message)`` and ``print_wmlerr(message, iserr)`` 
functions. Those functions will correctly print error/warning message

.. graphviz:: wmlerr.d

``dualcol_message`` and ``print_wmlerr`` will **not** add colors:
   
   * if current OS is Windows (even if ``ansi_setEnabled`` is ``True``)
   * **or** if ``--no-ansi-colors`` flag was used in command line 
     (``ansi_setEnabled`` is ``False``)

============================
Using unittest with wmlerr()
============================

``wmlerr`` behave differently if the global variable ``is_utest`` (global 
variable of module ``./pywmlx/wmlerr.py``)  is ``False`` (default value) or if 
it is ``True`` (must be ``True`` **only** on a unittest session).

During an unittest session, infact, it is required to change that value from
``True`` to ``False``, calling ``wmlerr_debug()`` function from your unittest
module. For this reason, unittest that requires to check ``wmlerr`` and 
``wmlwarn`` should also explicitly add this import:
    
.. code-block:: python
 
   from pywmlx.wmlerr import wmlerr_debug()

since ``wmlerr_debug()`` is not imported when you simply ``import pywmlx``.
The function ``wmlerr_debug()`` must then be called somewhere on your unittest 
function  **before** using ``wmlerr()``.

After setting ``is_utest`` to ``False`` calling ``wmlerr_debug()``, *wmlerr* 
can raise the exception, maintaining the traceback infos required (on unittest
session) to verify that the exception was correctly raised.

