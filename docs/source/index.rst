WMLxGettext 2.x
***************

.. toctree::
   :hidden:
   
   enduser/index.rst
   srcdoc/index.rst

Wmlxgettext is a python3.x tool that create a gettext translation file 
(.po file) for a wesnoth campaign / era / add-on.

It will parse a list .cfg and .lua files and stores the info required to 
create a nice .po file, than create the files.

From now on, the (old) perl script will be called "wmlxgettext 1.0", while the
new python3 script will be called "wmlxgettext 2.x"


======================
End-User documentation
======================

The :ref:`enduser_index` eplains how to **use** the wmlxgettext tool.
It will explain what you can use into your .cfg (WML) and .lua files and
it will explain how to invoke wmlxgettext tool.

=========================
Source Code Documentation
=========================

The :ref:`srcdoc_index` is directed to those ones that wants to contribute to
wmlxgettext development, or to those ones that wants to modify/fork this tool
for his own purposes.

The :ref:`srcdoc_index` is **not useful** if you only need to learn how to use 
wmlxgettext.

==================
Special Thanks To:
==================

   * Elvish Hunter (wesnoth developer) for his very precious help.
   * \|Wolf\| (python Italia) for his deep knowledge on python and his 
     precious help.
   * celticminstrel (wesnoth developer) for explaining me how
     to use the original perl wmlxgettext tool and for helping me to 
     improve the script.
   * loonycyborg: for testing the script and reporting bugs.

.. note::
   
   If you can find something crap in wmlxgettext code, it is **only** my fault.
   People listed above are not responsible :)
   
   Nobun

