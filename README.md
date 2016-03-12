# wmlxgettext-unoff
unofficial version of wmlxgettext (wesnoth utility), rewritten from scratch using python 3.x

Written by Nobun (registered as "AncientLich" on github site)

http://wif.altervista.org

-------------------------------------------------------------------

The directory wmlxgettext contains the python files of the actual prject.
However:
   
   * wmlxgettext/poreorder.py is not a part of the wmlxgettext sources but it
     is a little utility used to help to verify that the output produced by 
     wmlxgettext is safe.
   * test_wmlxgettext.py and the _test directory contains the unittests used
     while wmlxgettext was developed
   
So the real sources, in the wmlxdirectory, are:
   * wmlxgettext.py
   * the directory pywmlx and all python files and directories contained there.

--------------------------------------------------------------------

Documentation:
    
wmlxgettext is deeply documented. See the online documentation at:
  
http://wmlxgettext-unoff.readthedocs.org/


The complete source code used to write the online documentation is stored 
under the "docs/source" directory of this repository 

(only makefile missed, but it can be created with sphinx using the 
sphinx-quickstart utility).

