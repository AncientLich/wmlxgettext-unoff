#! /usr/bin/env python3

# NOTE: this file is neither a part of wmlxgettext source files, nor a part of
#       wmlxgettext test files.

# This script helps to check the differences from perl.po and python.po
# it will reorder python.po into python_reordered.po.
# In this way python_reordered will show translated sentences in the same order
# as perl.po

import re
import os
import sys
import argparse
import pywmlx



def commandline(args):
    parser = argparse.ArgumentParser(
        description=('Reorder python.po putting sentences in same sequence ' +
                     'as perl.po')
    )
    parser.add_argument(
        '--perl', 
        default='./perl.po',
        required=True,
        dest='perl',
        help=('the .po file created with PERL wmlxgettext ' +
               '[**REQUIRED ARGUMENT**]')
    )
    parser.add_argument(
        '--python', 
        default='./python.po',
        required=True,
        dest='python',
        help=('the .po file created with PYTHON3 wmlxgettext ' +
               '[**REQUIRED ARGUMENT**]')
    )
    parser.add_argument(
        '-o', 
        default='./python_reordered.po',
        required=True,
        dest='outfile',
        help=('reordered output file (path and name) ' +
               '[**REQUIRED ARGUMENT**]')
    )
    return parser.parse_args(args)



def main():
    args = commandline(sys.argv[1:])
    sentlist = dict()
    fi = open(os.path.realpath(os.path.normpath(args.python)), 'r' )
    fo = open(os.path.realpath(os.path.normpath(args.outfile)), 'w' )
    finfo = None
    wmlinfo = None
    mystring = None
    is_multiline = False
    lineno = 0
    for xline in fi:
        xline = xline.strip('\n\r')
        lineno += 1
        if lineno <= 12:
            print(xline, file=fo)
        else:
            m = re.match(r'#\.\s+(.+)', xline)
            if m:
                if wmlinfo is None:
                    wmlinfo = [ m.group(1) ]
                else:
                    wmlinfo.append(m.group(1))
            m = re.match(r'#\:\s+(.+)', xline)
            if m:
                if finfo is None:
                    finfo = [ m.group(1) ]
                else:
                    finfo.append(m.group(1))
            if xline == 'msgstr ""':
                xline = ''
                sentlist[mystring.lower()] = pywmlx.PoCommentedString(mystring,
                        orderid=(1,1,1), ismultiline=is_multiline, 
                        wmlinfos=wmlinfo , finfos=finfo, addedinfos=[] )
                mystring = None
                wmlinfo = None
                finfo = None
                is_multiline = False
            rx = re.compile(r'(?:msgid\s+)?"(.*)', re.I)
            m = re.match(rx, xline)
            if m:
                value = re.sub(r'(?:\n)?"$', '', m.group(1))
                if mystring is None:
                    mystring = value
                else:
                    is_multiline = True
                    mystring = mystring + '\n' + value
    fi.close()
    fi = None
    fi = open(os.path.realpath(os.path.normpath(args.perl)), 'r' )
    mystring = None
    lineno = 0
    for xline in fi:
        xline = xline.strip('\n\r')
        lineno += 1
        if lineno > 12:
            if xline == 'msgstr ""':
                postring = sentlist.get(mystring.lower())
                if postring is None:
                    print("error: cannot find:", mystring, file=sys.stderr)
                    sys.exit(1)
                postring.write(fo, False)
                print("", file=fo)
                mystring = None
            rx = re.compile(r'(?:msgid\s+)?"(.*)', re.I)
            m = re.match(rx, xline)
            if m:
                value = re.sub(r'(?:\n)?"$', '', m.group(1))
                if mystring is None:
                    mystring = value
                else:
                    mystring = mystring + '\n' + value
        # end if lineno > 12
    # end for xline
    fi.close()
    fo.close()


if __name__ == "__main__":   main()

