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
        description=('Reorder python.po putting sentences in same sequence '
                     'as perl.po')
    )
    parser.add_argument(
        '--perl', 
        default='./perl.po',
        required=True,
        dest='perl',
        help=('the .po file created with PERL wmlxgettext '
               '[**REQUIRED ARGUMENT**]')
    )
    parser.add_argument(
        '--python', 
        default='./python.po',
        required=True,
        dest='python',
        help=('the .po file created with PYTHON3 wmlxgettext '
               '[**REQUIRED ARGUMENT**]')
    )
    parser.add_argument(
        '--log', 
        default=None,
        dest='logfile',
        help=('(optional) output file where every error messages will be saved.'
              '\nNOTE: every error will be appended to the existing file (if '
              'any), so it is HIGLY suggested to save the log to a new file')
    )
    parser.add_argument(
        '-o', 
        default='./python_reordered.po',
        required=True,
        dest='outfile',
        help=('reordered output file (path and name) '
               '[**REQUIRED ARGUMENT**]')
    )
    return parser.parse_args(args)



def main():
    args = commandline(sys.argv[1:])
    sentlist = dict()
    fi = None
    fo = None
    try:
        fi = open(os.path.realpath(os.path.normpath(args.python)), 'r', 
                  encoding='utf-8')
    except OSError as e:
        errmsg = ('fatal error: cannot open ' + e.filename + 
                  ' (' + e.args[1] + ')' )
        print(errmsg, file=sys.stderr)
        sys.exit(1)
    try:
        fo = open(os.path.realpath(os.path.normpath(args.outfile)), 'w',
                  encoding='utf-8')
    except OSError as e:
        errmsg = ('fatal error: cannot create ' + e.filename + 
                  ' (' + e.args[1] + ')' )
        print(errmsg, file=sys.stderr)
        sys.exit(1)
    finfo = None
    wmlinfo = None
    mystring = None
    is_multiline = False
    actual_header_started = False
    header_skipped = False
    for xline in fi:
        xline = xline.strip('\n\r')
        if not header_skipped:
            print(xline, file=fo)
            if not actual_header_started and xline == 'msgid ""':
                actual_header_started = True
            elif actual_header_started and '"' not in xline:
                header_skipped = True
        else:
            # storing comments for translator (wmlinfos)
            m = re.match(r'#\.\s+(.+)', xline)
            if m:
                if wmlinfo is None:
                    wmlinfo = [ m.group(1) ]
                else:
                    wmlinfo.append(m.group(1))
            # storing file info references (finfos)
            m = re.match(r'#\:\s+(.+)', xline)
            if m:
                if finfo is None:
                    finfo = [ m.group(1) ]
                else:
                    finfo.append(m.group(1))
            # when msgstr "" is found, the msgid (wich defined the string)
            # ended, so we know it is time to store the PoSentence in the
            # dictionary
            if xline == 'msgstr ""':
                xline = ''
                # orderid=(1,1,1): this script doesn't care of posentences' 
                #    internal ordering,since the posentences will follow the 
                #    same order of the parameter file. 
                #    So why orderid is not actually used here, and this is why 
                #    we set it to a fixed value (1,1,1)
                # addedinfos=[]: during reading the .po file we collected all
                #    `#. infos` into wmlinfos list. So we not need to 
                #     distinguish from wmlinfos and addedinfos. This is why
                #     addedinfos is not used here.
                sentlist[mystring.lower()] = pywmlx.PoCommentedString(mystring,
                        orderid=(1,1,1), ismultiline=is_multiline, 
                        wmlinfos=wmlinfo , finfos=finfo, addedinfos=[] )
                mystring = None
                wmlinfo = None
                finfo = None
                is_multiline = False
            # on msgid (and following lines) we need to store the string
            rx = re.compile(r'(?:msgid\s+)?"(.*)', re.I)
            m = re.match(rx, xline)
            if m:
                # we must remove the litteral \n" characters at the end of
                # every line since they will be added again by 
                # PoCommentedString.write()
                # [or the reordered .po file will be wrong]
                value = re.sub(r'(?:\\n)?"$', '', m.group(1))
                if mystring is None:
                    mystring = value
                else:
                    is_multiline = True
                    mystring = mystring + '\n' + value
    fi.close()
    fi = None
    # When we previously collected all strings stored into the original 
    # python.po file, we correctly removed all the litteral \n" characters
    # at the end of every line.
    # But, on multiline strings, we also collected an unwanted empty line
    # since the regex r'(?:msgid\s+)?"(.*)' collected also msgid "".
    # This is why we need to remove the first empty line from multi-line
    # strings stored into the dictionary
    for key, val in sentlist.items():
        if val.ismultiline:
            val.sentence = re.sub('^\n', '', val.sentence)
    # Now it is time to open the perl file
    # perl file will allow us to know the order that we will follow
    # in the final output file
    try:
        fi = open(os.path.realpath(os.path.normpath(args.perl)), 'r',
                  encoding='utf-8')
    except OSError as e:
        errmsg = ('fatal error: cannot open ' + e.filename + 
                  ' (' + e.args[1] + ')' )
        print(errmsg, file=sys.stderr)
        sys.exit(1)
    mystring = None
    lineno = 0
    for xline in fi:
        xline = xline.strip('\n\r')
        lineno += 1
        if lineno > 12:
            if xline == 'msgstr ""':
                # when msgstr "" is found, the msgid (wich defined the string)
                # ended, so we have the complete key that we will 
                # search in the sentlist dictionary. 
                # So we can get the PoCommentedString with sentlist.get()
                # and we can write it into the reordered .po file
                postring = sentlist.get(mystring.lower())
                if postring is None:
                    print("error: cannot find:", mystring, file=sys.stderr)
                    if args.logfile is not None:
                        logfile = None
                        try:
                            logfile = open(args.logfile, 'a', encoding='utf-8')
                        except OSError as e:
                            errmsg = ('cannot write on file ' + e.filename + 
                                      ' (' + e.args[1] + ')' )
                            print('fatal error:', errmsg, file=sys.stderr)
                            sys.exit(1)
                        print('[cannot find]:', mystring, file=logfile)
                        print('', file=logfile)
                        logfile.close()
                else:
                    # poreorder always create non-fuzzy strings, since perl
                    # pot file will be always non-fuzzy. So why the second
                    # parameter (is_fuzzy?) of postring.write is setted 
                    # to False
                    postring.write(fo, False)
                    print("", file=fo)
                mystring = None
            # on msgid (and following lines) we need to store the string
            rx = re.compile(r'(?:msgid\s+)?"(.*)', re.I)
            m = re.match(rx, xline)
            if m:
                value = re.sub(r'(?:\\n)?"$', '', m.group(1))
                if mystring is None:
                    mystring = value
                else:
                    mystring = mystring + '\n' + value
        # end if lineno > 12
    # end for xline
    fi.close()
    fo.close()


if __name__ == "__main__":   main()

