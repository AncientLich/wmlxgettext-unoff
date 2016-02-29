The last step: writing the .po file
***********************************

When the dictionary of ``PoCommentedString`` object is done (the end of the
last file is reached and nothing is left unparsed) it is the time to write
all the dictionary into an actual .po file:

.. code-block:: python
   
   # ./wmlxgettext:164
   outfile = None
   if args.outfile is None:
       outfile = sys.stdout
   else:
       outfile_name = os.path.realpath(os.path.normpath(args.outfile))
       outfile = open(outfile_name, 'w')
   pkgversion = args.package_version + '\\n"'
   print('msgid ""\nmsgstr ""', file=outfile)
   print('"Project-Id-Version:', pkgversion, file=outfile)
   print('"Report-Msgid-Bugs-To: http://bugs.wesnoth.org/\\n"', file=outfile)
   now = datetime.now()
   cdate = str(now.year) + '-'
   if now.month < 10:
       cdate = cdate + '0'
   cdate = cdate + str(now.month) + '-'
   if now.day < 10:
       cdate = cdate + '0'
   cdate = cdate + str(now.day) + ' '
   if now.hour < 10:
       cdate = cdate + '0'
   cdate = cdate + str(now.hour) + ':'
   if now.minute < 10:
       cdate = cdate + '0'
   cdate = cdate + str(now.minute) + strftime("%z") + '\\n"'
   
   print('"POT-Creation-Date:', cdate, file=outfile)
   print('"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"', file=outfile)
   print('"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"', file=outfile)
   print('"Language-Team: LANGUAGE <LL@li.org>\\n"', file=outfile)
   print('"MIME-Version: 1.0\\n"', file=outfile)
   print('"Content-Type: text/plain; charset=UTF-8\\n"', file=outfile)
   print('"Content-Transfer-Encoding: 8bit\\n"\n', file=outfile)

This part of code (into ``wmlxgettext`` main script file) writes down the 
.po header informations::
   
   msgid ""
   msgstr ""
   "Project-Id-Version: PACKAGE VERSION\n"
   "Report-Msgid-Bugs-To: http://bugs.wesnoth.org/\n"
   "POT-Creation-Date: 2016-02-19 17:59+0100\n"
   "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
   "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
   "Language-Team: LANGUAGE <LL@li.org>\n"
   "MIME-Version: 1.0\n"
   "Content-Type: text/plain; charset=UTF-8\n"
   "Content-Transfer-Encoding: 8bit\n"

After writing the header, it is the time to write the translatable strings:

.. code-block:: python
   
   # ./pywmlx/wmlxgettext:196
   for posentence in sorted(sentlist.values(), key=lambda x: x.orderid):
       posentence.write(outfile, args.fuzzy)
       print('', file=outfile)

All ``PoCommentedString`` objects contained in dictionary will be written in 
the correct order (thank of ``sorted()`` that sorts ``PoCommentedString`` 
object by ``orderid`` value)

Every ``PoCommentedString`` object will be then written in .po file, calling
the ``PoCommentedString.write()`` function.

The ``PoCommentedString.write()`` function will:
   
   * write ``wmlinfos`` and ``addedinfos`` on ``PoCommentedString`` object,
     one by one, as ``#. <message to translator>``
   * write ``finfos`` on ``PoCommentedString`` object, one by one, as
     ``#: path/to/file:x`` infos
   * put the *fuzzy flag* if ``--fuzzy`` option was used in wmlxgettext command 
     line
   * write translatable string into ``msgid "..."`` parameter in the proper
     way
   * add an empty line ``msgstr ""`` (where the translator will put the 
     translation into another language).

Now it is the time for the very last explaination:

.. code-block:: python
   
   # ./pywmlx/wmlxgettext:199
   if args.outfile is not None:
       outfile.close()

If ``args.outfile`` is ``None``, then the option ``-o output-file-name`` was
not used (output should be written in ``stdout`` like in wmlxgettext 1.0, and
it can be redirected to a file)

If ``args.outfile`` is **not** ``None``, then an output file is directly 
created by wmlxgettext itself (and that file buffer must be closed).