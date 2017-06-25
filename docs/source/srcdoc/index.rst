.. _srcdoc_index:

Source Code Documentation
*************************

This the new release of wmlxgettext, rewritten from scratch in python 3.x.
Wmlxgettext is a python3 script that scans a list of .cfg (WML) and .lua files,
capturing all translatable string found in the files and creates a pot (.po) 
file.

From now on, the (old) perl script will be called "wmlxgettext 1.0", while the
new python3 script will be called "wmlxgettext 2.x".

**Warning:** this source documentation is a bit outdated. This documentation is
however still valid to understand the wmlxgettext source logic.
Please consider to take a look also to source code comments for a more updated
source documentation.


.. toctree::
   :maxdepth: 2
   :numbered:
   
   intro.rst
   errors.rst
   genparse.rst
   machine.rst
   write.rst
   regexes.rst

