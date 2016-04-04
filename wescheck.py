#! /usr/bin/env python3

import re
import os
import sys
import argparse
import subprocess
from glob import glob



# clean all results you eventually created in past
# this allows to have a clean 
def my_cleandirs():
    currentdir = os.path.realpath('.')
    for xdir, ext in [('./data/cache/perl', '*.po'), 
                      ('./data/cache/python', '*.po'), 
                      ('./data/cache/reordered', '*.po'),
                      ('./data/cache/logs', '*.log'),
                      ('./data/results', '*')]:
        os.chdir(os.path.realpath(xdir))
        filelist = glob(ext)
        for f in filelist:
            os.remove(f)
        os.chdir(currentdir)



# we get all the domains that wesnoth core uses, with a simple trick:
# we will walk on wesnoth/po directory and we will search for
# <domain>/FINDCFG
# Then we invoke explicitly 'bash', executing those FINDCFG files.
# in that way we also obtain the filelist related to each domain
#
# NOTE: all domains without the FINDCFG file (domains where wmlxgettext is not 
#       called) are not included in this process
def get_domains(podir):
    domains = {}
    for root, dirs, files in os.walk(podir, topdown=False):
        for name in files:
            m = re.search(r'FINDCFG$', name)
            if m:
                p = subprocess.check_output(
                    ['bash', os.path.join(root, name)])
                filelist = p.decode('utf-8').split('\n')
                # after running FINDCFG script, and after splitting the
                # output in a list, we will have an extra unwanted item at
                # the end (it is an empty string). Se we will remove it from
                # the list
                del filelist[-1]
                domain = os.path.join(root, name)
                domain = domain [ len(podir) +1 : ]
                domain = re.sub(r'\/.*', '', domain)
                domains[domain] = filelist
                # domains 
    return domains



# This function will create the command sequences we will use with
# PERL wmlxgettext and PYTHON wmlxgettext.py
# wesnoth = path of wesnoth source directory
# domains = dictionary: key=domain, value=file_list
# perl_wmlx = path of PERL wmlxgettext
# py_wmlx = path of PYTHON wmlxgettext
def get_commands(wesnoth, domains, perl_wmlx, py_wmlx):
    # commands is a dictionary where key = domain, value = command list
    pycommands = {}
    perlcommands = {}
    wesnothdir = '--directory=' + wesnoth
    cmd = None
    for domain, filelist in domains.items():
        cmd = None
        domainname = '--domain=' + domain
        cmd = [perl_wmlx, wesnothdir, domainname]
        if domain == 'wesnoth':
            cmd.append('--initialdomain=wmlxgettext')
        try:        
            for f in filelist:
                cmd.append(f)
        except:
            print(domain)
            print(filelist)
            print('----------')
            sys.exit(1)
        perlcommands[domain] = list(cmd)
        cmd = None
        cmd = [py_wmlx, '--no-ansi-colors', wesnothdir, domainname]
        if domain == 'wesnoth':
            cmd.append('--initialdomain=wmlxgettext')
        for f in filelist:
            cmd.append(f)
        pycommands[domain] = list(cmd)
    return (perlcommands, pycommands)



# wescache will check for 'wes.inf' file into the data/cache file
# wescache will manage reading/writing the 'wes.inf' file
# 'wes.inf' file (if exists) contain the path of wesnoth source directory
# in this way you can avoid to use the --wesnoth option any time you run
# wescheck.
# If --wesnoth option is used, the new path will be written in 'wes.inf'
#    (if the file does not exist, it will be created)
# If --wesnoth option is NOT used, than wescache will try to load from
#    'wes.inf' the path of the wesnoth source directory.
#    if 'wes.inf' does not exist (first time you run wescheck.py)
#    then an error is raised
#
# wescache also return wesnoth, domains where:
#   wesnoth --> string with wesnoth source directory
#   domains --> dictionary with keys=domains values=list_of_files
def wescache(cachefile, wesnoth):
    cache = None
    if wesnoth:
        try:
            cache = open(cachefile, 'w', encoding='utf-8')
        except OSError as e:
            errmsg = ('\033[31mfatal error:\033[0m cannot write: ' + 
                         e.filename + ' (' + e.args[1] + ')' )
            print(errmsg, file=sys.stderr)
            sys.exit(1)
        print('wesnoth srcpath =', wesnoth, file=cache)
        cache.close()
    else:
        try:
            cache = open(cachefile, 'r', encoding='utf-8')
        except OSError:
            print('\033[31merror:\033[0m wesnoth path is neither setted with '
                  '--wesnoth option, nor it is stored in cache.\n'
                  'Please run ./wescheck --wesnoth WESNOTH_SRC_DIR',
                  file=sys.stderr)
            sys.exit(1)
        for xline in cache:
            xline = xline.strip('\n\r')
            rx = re.compile('wesnoth\s+srcpath\s*=\s*(.*)', re.I)
            m = re.match(rx, xline)
            if m:
                wesnoth = m.group(1)
        cache.close()
    # end else (if wesnoth is None)
    currentdir = os.path.realpath('.')
    os.chdir(wesnoth)
    domains = get_domains(os.path.join(wesnoth, 'po'))
    os.chdir(currentdir)
    return (wesnoth, domains)




# wesceck.py command line parser
def commandline(args):
    parser = argparse.ArgumentParser(
        description=('This tool emulates the pot-update build rule checking '
                     'the builtin pot files in wesnoth sources and than '
                     'executing perl wmlxgettext, then python wmlxgettext, '
                     'and finally comparing results with poreorder.py utility '
                     'and creating diff files')
    )
    parser.add_argument(
        '--wesnoth', 
        default=None,
        dest='wesnoth',
        help=('The (root) directory where wesnoth sources are stored. '
              'This parameter is required the very first time you run this '
              'tool; it may be omitted, instead, if it is not the first time '
              'you are running it (wesnoth path will be loaded from wescheck '
              'cache files)')
    )
    return parser.parse_args(args)



def main():
    # this script can be runned also on linux or mac
    # so an error returned if the HOST OS is neither linux nor mac
    if (not sys.platform.startswith('linux') and 
        not sys.platform.startswith('darwin')):
            print('FATAL ERROR: wescheck.py can be runned '
                  'only on Linux or Mac', file=sys.stderr)
            sys.exit(1)
    # starting the actual script
    args = commandline(sys.argv[1:])
    print('\n\033[36m(1/4)\033[0m cleaning directories and calculating '
          'commands... \033[33m(wait...)\033[0m', file=sys.stderr)
    wesnoth = None
    domains = None
    filelist = None
    if args.wesnoth is not None:
        wesnoth = os.path.realpath(os.path.normpath(args.wesnoth)) 
    wesnoth, domains = wescache(
        os.path.realpath('./data/cache/wes.inf'), wesnoth)
    perl_wmlx = os.path.join(wesnoth, 'utils', 'wmlxgettext')
    py_wmlx = os.path.realpath('./wmlxgettext/wmlxgettext.py')
    pycommands = None
    perlcommands = None
    perlcommands, pycommands = get_commands(wesnoth, domains, 
                                            perl_wmlx, py_wmlx)
    # tot_creations is two times perlcommands becouse we must count
    # also the execution of pycommands (+1 is to avoid 100% to be displayed)
    my_cleandirs()
    print('\033[1A\033[36m(1/4)\033[0m cleaning directories and calculating '
          'commands... \033[32mDone\033[0m               ', file=sys.stderr)
    tot_creations = (len(perlcommands.items()) * 2) +1
    creations_done = 0
    print('\033[36m(2/4)\033[0m running perl/python wmlxgettext... 0 %', 
          file=sys.stderr)
    # ---------------------------------------------------------
    #  create pot files using PERL wmlxgettext on
    #  data/cache/perl
    # ---------------------------------------------------------
    for xdomain, cmd in perlcommands.items():
        potfilename = xdomain + '.po'
        potfile = os.path.realpath(
            os.path.join('.', 'data', 'cache', 'perl', potfilename))
        logfilename = 'perl_' + xdomain + '.log'
        logfile = os.path.realpath(
            os.path.join('.', 'data', 'cache', 'logs', logfilename))
        with open(potfile, 'w') as xpo:
            with open(logfile, 'w') as xlog:
                subprocess.call(cmd, stdout=xpo, stderr=xlog)
        creations_done += 1
        perc = int((creations_done * 100) / tot_creations)
        print('\033[1A\033[36m(2/4)\033[0m running perl/python wmlxgettext...',
              str(perc), '%   ', file=sys.stderr)
    # ---------------------------------------------------------
    #  create pot files using PYTHON3 wmlxgettext on
    #  data/cache/python
    # ---------------------------------------------------------
    for xdomain, cmd in pycommands.items():
        potfilename = xdomain + '.po'
        potfile = os.path.realpath(
            os.path.join('.', 'data', 'cache', 'python', potfilename))
        logfilename = 'python_' + xdomain + '.log'
        logfile = os.path.realpath(
            os.path.join('.', 'data', 'cache', 'logs', logfilename))
        with open(potfile, 'w') as xpo:
            with open(logfile, 'w') as xlog:
                subprocess.call(cmd, stdout=xpo, stderr=xlog)
        creations_done += 1
        perc = int((creations_done * 100) / tot_creations)
        print('\033[1A\033[36m(2/4)\033[0m running perl/python wmlxgettext...',
              str(perc), '%   ', file=sys.stderr)
    print('\033[1A\033[36m(2/4)\033[0m running perl/python wmlxgettext...',
          '\033[32mDone\033[0m        ', file=sys.stderr)
    # ---------------------------------------------------------
    #   now we can run poreorder.py
    #   running poreorder.py
    # ---------------------------------------------------------
    tot_creations = len(perlcommands.items()) +1
    creations_done = 0
    # debug: 
    # ['/home/user/programmi/my/git/wmlxgettext-unoff/wmlxgettext/poreorder.py', 
    #  '--perl', 
    #  './data/cache/perl/wesnoth-l.po', 
    #  '--python', 
    # './data/cache/python/wesnoth-l.po', 
    # '-o', './data/cache/reordered/wesnoth-l.po', 
    # '--log', './data/results/poreorder.err']

    print('\033[36m(3/4)\033[0m running poreorder.py... 0%', 
          file=sys.stderr)
    for xdomain in perlcommands.keys():
        mycommands = None
        mycommands = [ os.path.realpath(
                os.path.join('.', 'wmlxgettext', 'poreorder.py'))]
        potfilename = xdomain + '.po'
        mycommands.append('--perl')
        mycommands.append(
            os.path.join('.', 'data', 'cache', 'perl', potfilename) )
        mycommands.append('--python')
        mycommands.append(
            os.path.join('.', 'data', 'cache', 'python', potfilename) )
        mycommands.append('-o')
        mycommands.append(
            os.path.join('.', 'data', 'cache', 'reordered', potfilename) )
        mycommands.append('--log')
        mycommands.append(
            os.path.join('.', 'data', 'results', 'poreorder.err' ))
        with open(os.devnull, 'w') as nil:
            subprocess.call(mycommands, stdout=nil, stderr=nil)
        creations_done += 1
        perc = int((creations_done * 100) / tot_creations)
        print('\033[1A\033[36m(3/4)\033[0m running poreorder.py...',
              str(perc), '%   ', file=sys.stderr)
    print('\033[1A\033[36m(3/4)\033[0m running poreorder.py...',
          '\033[32mDone\033[0m        ', file=sys.stderr)
    print('\033[36m(4/4)\033[0m Creating diffs... '
          '\033[33m(wait...)\033[0m', file=sys.stderr)
    # ------------------------------------------------------
    #  creating perl_wmlx.err file
    #  and python_wmlx.err file
    # ------------------------------------------------------
    pylogs = None
    pylogs = []
    perlogs = None
    perlogs = []
    # creating pylogs, perlogs (list of python and perl log files)
    for xfile in os.listdir('./data/cache/logs'):
        m = re.match('perl_', xfile)
        if m:
            perlogs.append(xfile)
        else:
            pylogs.append(xfile)
    # reading logs and writing perl_wmlx.err and python_wmlx.err
    for loglist, logpath in [(perlogs, './data/results/perl_wmlx.err'),
                             (pylogs, './data/results/python_wmlx.err')]:
        fo = None
        fo = open(logpath, 'w', encoding='utf-8')
        for log in loglist:
            xfile = None
            xfile = open(os.path.join('.', 'data', 'cache', 'logs', log), 
                         'r', encoding='utf-8')
            for xline in xfile:
                xline = xline.strip('\n\r')
                m = re.match(r'\s*$', xline)
                if not m:
                    print(xline, file=fo)
            xfile.close()
            xfile = None
        fo.close()
        fo = None
    # --------------------------------------------------------
    #  creating diff files
    # --------------------------------------------------------
    with open('./data/results/normal.diff', 'w') as out:
        with open(os.devnull, 'w') as nil:
            subprocess.call(['diff', '-ruN',
                             './data/cache/perl/',
                             './data/cache/python/'], stdout=out, stderr=nil)
    with open('./data/results/reordered.diff', 'w') as out:
        with open(os.devnull, 'w') as nil:
            subprocess.call(['diff', '-ruN',
                             './data/cache/perl/',
                             './data/cache/reordered/'], 
                            stdout=out, stderr=nil)
    print('\033[1A\033[36m(4/4)\033[0m Creating diffs... '
          '\033[32mDone\033[0m        ', file=sys.stderr)
    print('', file=sys.stderr)
    print('\033[32mALL WORK IS FINISHED!\033[0m             ',
          file=sys.stderr)
    print('', file=sys.stderr)



if __name__ == "__main__":
    main()

