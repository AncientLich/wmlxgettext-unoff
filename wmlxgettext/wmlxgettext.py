#!/usr/bin/env python3


# encoding: utf8
#
# wmlxgettext -- generate a blank .po file for official campaigns translations 
#                    (build tool for wesnoth core)
#             -- if you are a UMC developer, you could use umcpo, instead
#                
#
# By Nobun, october 2015
#
#                              PURPOSE
#
# wmlxgettext is a python3 tool that replace the old (but very good) 
# perl script with the same name.
# Replacing perl with python3 will ensure more portability.
#
# wmlxgettext is a tool that is directly used during wesnoth build process 
# to generate the pot files for the core campaigns.
#
# If you are an UMC developer you might want to use umcpo instead of using
# wmlxgettext directly (but using wmlxgettext directly is however possible).
#
#                              BASIC PROCEDURE
#
# todo
#
#                              MAGIC COMMENTS
#
# todo
#
#                              DEVELOPER INFORMATION
#
# todo.
#


import os
import re
import sys
import warnings
import argparse
from datetime import datetime
from time import strftime
import pywmlx



def commandline(args):
    parser = argparse.ArgumentParser(
        description='Generate .po from WML/lua file list.',
        usage='''wmlxgettext --domain=DOMAIN [--directory=START_PATH]
                   [--scandirs <dir1, dir2...>]
                   [--initialdomain=INITIALDOMAIN] [-o OUTPUT_FILE]
                   [--package-version=PACKAGE_VERSION]
                   [--no-ansi-colors] [--fuzzy] [--warnall]
                   FILE1 FILE2 ... FILEN'''
    )
    parser.add_argument(
        '-o',
        default=None,
        dest='outfile',
        help= ('Destination file. By default the output ' +
               'will be printed on stdout')
    )
    parser.add_argument(
        '--domain', 
        default='wmlxgettext',
        required=True,
        dest='domain',
        help= ('The textdomain (on WML/lua file) wich contains the ' +
               'strings that will be actually translated ' +
               '[**REQUIRED ARGUMENT**]')
    )
    parser.add_argument(
        '--directory', 
        default='.',
        dest='start_path',
        help=('Complete path of your "start directory". ' +
              'The path to every source file should start from this ' +
              'directory.')
    )
    parser.add_argument(
        '--initialdomain', 
        default='wesnoth',
        dest='initdom',
        help=('Initial domain value on WML/lua file when no textdomain ' +
              'setted in that WML/lua file.\nBy default it is equal to ' +
              '"wesnoth" and usually you don\'t need to change this value')
    )
    parser.add_argument(
        '--package-version',
        default='PACKAGE VERSION',
        dest='package_version',
        help=('Version number of your wesnoth add-on. You don\'t actually ' +
              'require to set this option since you can directly edit the ' +
              'po file produced by wmlxgettext. However this option could ' +
              'help you to save a bit of time')
    )
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
    parser.add_argument(
        '--warnall',
        action='store_true',
        default=False,
        dest='warnall',
        help="Show all warnings. By default some warnings are hided"
    )
    parser.add_argument(
        '--fuzzy',
        action='store_true',
        default=False,
        dest='fuzzy',
        help=("If you specify this flag, all sentences contained on the POT " +
              "file created by wmlxgettext will be setted as fuzzy.\n" +
              "By default sentences are NOT setted as fuzzy")
    )
    parser.add_argument(
        '--scandirs',
        nargs='+',
        default=None,
        help=("If this option is used, wmlxgettext will scan all directories" +
              " listed after --scandirs option. Every directory must be a " +
              "subdirectory of the directory setted on --directory option. " +
              "If this option is used, EXPLICIT LIST of files will be " +
              "ignored.") 
    )
    parser.add_argument(
        'filelist',
        help='List of WML/lua files of your UMC (source files)',
        nargs='*'
    )
    return parser.parse_args(args)



def main():
    # nota: rimane scoperto il controllo dell' eventualità che l'ultimo #define
    # di un file WML non sia stato correttamente chiuso da un #enddef entro
    # la fine del file
    args = commandline(sys.argv[1:])
    pywmlx.ansi_setEnabled(args.ansi_col)
    pywmlx.set_warnall(args.warnall)
    startPath = os.path.realpath(os.path.normpath(args.start_path))
    sentlist = dict()
    fileno = 0
    pywmlx.statemachine.setup(sentlist, args.initdom, args.domain)
    filelist = None
    if args.scandirs is not None:
        filelist = pywmlx.autof.autoscan(startPath, args.scandirs)
    elif args.filelist is None:
        pywmlx.wmlerr("bad command line", "FILELIST must not be empty. " +
               "Please, run wmlxgettext again and, this time, add some file " +
               "in FILELIST or use the --scandirs option.")
    elif len(args.filelist) <= 0:
        pywmlx.wmlerr("bad command line", "FILELIST must not be empty. " +
               "Please, run wmlxgettext again and, this time, add some file " +
               "in FILELIST or use the --scandirs option.")
    else:
        filelist = args.filelist
    for fx in filelist:
        fileno += 1
        fname = os.path.join(startPath, os.path.normpath(fx))
        is_file = os.path.isfile(fname)
        if is_file:
            infile = None
            try: 
                infile = open(fname, 'r', encoding="utf8")
            except:
                wmlerr(fname, "cannot open file")
            if fname[-4:].lower() == '.cfg':
                pywmlx.statemachine.run(filebuf=infile, fileref=fx, 
                            fileno=fileno, startstate='wml_idle', waitwml=True)
            if fname[-4:].lower() == '.lua':
                pywmlx.statemachine.run(filebuf=infile, fileref=fx, 
                            fileno=fileno, startstate='lua_idle', waitwml=False)
            infile.close()
    outfile = None
    if args.outfile is None:
        outfile = sys.stdout
    else:
        outfile_name = os.path.realpath(os.path.normpath(args.outfile))
        outfile = open(outfile_name, 'w', encoding="utf8")
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
    for posentence in sorted(sentlist.values(), key=lambda x: x.orderid):
        posentence.write(outfile, args.fuzzy)
        print('', file=outfile)
    if args.outfile is not None:
        outfile.close()



if __name__ == "__main__":   main()



# def test_wmlerr_internal():
#     wmlwarn("file1:5", "testing warning...")
#     wmlerr("file2:7", "testing error...")
#     print("this string should not be printed")


# if __name__ == "__main__":   test_wmlerr_internal()

