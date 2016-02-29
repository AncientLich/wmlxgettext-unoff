import re
# import os

from pywmlx.wmlerr import wmlerr
from pywmlx.wmlerr import wmlwarn
from pywmlx.wmlerr import warnall
from pywmlx.postring import PoCommentedString
from pywmlx.state.state import State
from pywmlx.state.lua_states import setup_luastates
from pywmlx.state.wml_states import setup_wmlstates

import pywmlx.nodemanip



_dictionary = None
_states = None
_initialdomain = None
_currentdomain = None
_domain = None
_startstate = None
_xline = None
_waitwml = True

_pending_addedinfo = None
_pending_overrideinfo = None
_pending_winfotype = None

_pending_luafuncname = None

_pending_luastring = None
_pending_wmlstring = None

_current_lineno = 0
_linenosub = 0



def checkdomain():
    global _currentdomain
    global _domain
    global _pending_addedinfo
    global _pending_overrideinfo
    if _currentdomain == _domain:
        return True
    else:
        _pending_addedinfo = None
        _pending_overrideinfo = None
        return False



def checksentence(mystring, finfo, *, islua=False):
    m = re.match(r'\s*$', mystring)
    if m:
        wmlwarn(finfo, "found an empty translatable message")
        return 1
    elif warnall() and not islua:
        if "}" in mystring:
            wmsg = ("found a translatable string containing a WML macro." +
                    " Translation for this string will NEVER work")
            wmlwarn(finfo, wmsg)
            return 2
        else:
            return 0
    else:
        return 0



class PendingLuaString:
    def __init__(self, lineno, luatype, luastring, ismultiline, 
                 istranslatable):
        self.lineno = lineno
        self.luatype = luatype
        self.luastring = luastring
        self.ismultiline = ismultiline
        self.istranslatable = istranslatable
    
    def addline(self, value):
        self.luastring = self.luastring + '\n' + value
    
    def store(self):
        global _pending_addedinfo 
        global _pending_overrideinfo
        global _linenosub
        if checkdomain() and self.istranslatable:
            _linenosub += 1
            finfo = pywmlx.nodemanip.fileref + ":" + str(self.lineno)
            fileno = pywmlx.nodemanip.fileno
            errcode = checksentence(self.luastring, finfo, islua=True)
            if errcode != 1:
                # when errcode is equal to 1, the translatable string is empty
                # so, using "if errcode != 1" 
                # we will add the translatable string ONLY if it is NOT empty
                if self.luatype == 'luastr2':
                    self.luastring = re.sub(r"\'", r"'", self.luastring)
                self.luastring = re.sub(r'(?<!\\)"', r'\"', self.luastring)
                loc_wmlinfos = []
                loc_addedinfos = None
                if _pending_overrideinfo is not None:
                    loc_wmlinfos.append(_pending_overrideinfo)
                if (_pending_luafuncname is not None and 
                        _pending_overrideinfo is None):
                    winf = '[lua]: ' + _pending_luafuncname
                    loc_wmlinfos.append(winf)
                if _pending_addedinfo is None:
                    loc_addedinfos = []
                if _pending_addedinfo is not None:
                    loc_addedinfos = _pending_addedinfo
                loc_posentence = _dictionary.get(self.luastring.lower())
                if loc_posentence is None:
                    _dictionary[self.luastring.lower()] = PoCommentedString(
                                self.luastring, 
                                orderid=(fileno, self.lineno, _linenosub),
                                ismultiline=self.ismultiline,
                                wmlinfos=loc_wmlinfos, finfos=[finfo],
                                addedinfos=loc_addedinfos )
                else:
                    loc_posentence.update_with_commented_string(
                           PoCommentedString(
                                self.luastring, 
                                orderid=(fileno, self.lineno, _linenosub),
                                ismultiline=self.ismultiline,
                                wmlinfos=loc_wmlinfos, finfos=[finfo],
                                addedinfos=loc_addedinfos
                    ) )
        # finally PendingLuaString.store() will clear pendinginfos,
        # in any case (even if the pending string is not translatable)
        _pending_overrideinfo = None
        _pending_addedinfo = None



class PendingWmlString:
    def __init__(self, lineno, wmlstring, ismultiline, istranslatable):
        self.lineno = lineno
        self.wmlstring = wmlstring
        self.ismultiline = ismultiline
        self.istranslatable = istranslatable
    
    def addline(self, value):
        self.wmlstring = self.wmlstring + '\n' + value
    
    def store(self):
        global _pending_addedinfo 
        global _pending_overrideinfo
        global _linenosub
        global _pending_winfotype
        if _pending_winfotype is not None:
            if self.ismultiline is False and self.istranslatable is False:
                winf = _pending_winfotype + '=' + self.wmlstring
                pywmlx.nodemanip.addWmlInfo(winf)
            _pending_winfotype = None
        if checkdomain() and self.istranslatable:
            finfo = pywmlx.nodemanip.fileref + ":" + str(self.lineno)
            errcode = checksentence(self.wmlstring, finfo, islua=False)
            if errcode != 1:
                # when errcode is equal to 1, the translatable string is empty
                # so, using "if errcode != 1" 
                # we will add the translatable string ONLY if it is NOT empty
                _linenosub += 1
                self.wmlstring = re.sub('""', '"', self.wmlstring)
                pywmlx.nodemanip.addNodeSentence(self.wmlstring, 
                                             ismultiline=self.ismultiline, 
                                             lineno=self.lineno, 
                                             lineno_sub=_linenosub,
                                             override=_pending_overrideinfo, 
                                             addition=_pending_addedinfo)
        _pending_overrideinfo = None
        _pending_addedinfo = None



def addstate(name, value):
    global _states
    if _states is None:
        _states = {}
    _states[name.lower()] = value



def setup(dictionary, initialdomain, domain):
    global _dictionary
    global _initialdomain
    global _domain
    _dictionary = dictionary
    _initialdomain = initialdomain
    _domain = domain
    setup_luastates()
    setup_wmlstates()



def run(*, filebuf, fileref, fileno, startstate, waitwml=True):
    global _states
    global _current_lineno
    global _linenosub
    global _waitwml
    global _currentdomain
    global _dictionary
    global _pending_luafuncname
    _pending_luafuncname = None
    # cs is "current state"
    cs = _states.get(startstate)
    _current_lineno = 0
    _linenosub = 0
    _waitwml = waitwml
    _currentdomain = _initialdomain
    pywmlx.nodemanip.newfile(fileref, fileno)
    # debug_cs = startstate
    for xline in filebuf:
        xline = xline.strip('\n\r')
        _current_lineno += 1
        while xline is not None:
            # action number is used to know what function we should run
            # debug_file0 = open(os.path.realpath('./debug.txt'), 'a')
            # print("!!!", xline, file=debug_file0)
            # debug_file0.close()
            action = 0
            v = None
            m = None
            if cs.regex is None:
                # action = 1 --> execute state.run
                action = 1 
            else:
                # m is match
                m = re.match(cs.regex, xline)
                if m:
                    # action = 1 --> execute state.run
                    action = 1
                else:
                    # action = 2 --> change to the state pointed by 
                    #                state.iffail
                    action = 2
            if action == 1:
                # xline, ns: xline --> override xline with new value
                #            ns --> value of next state
                xline, ns = cs.run(xline, _current_lineno, m)
                # debug_cs = ns
                cs = _states.get(ns)
            else:
                # debug_cs = cs.iffail
                cs = _states.get(cs.iffail)
            # debug_file = open(os.path.realpath('./debug.txt'), 'a')
            # print(debug_cs, file=debug_file)
            # debug_file.close()
        # end while xline
    # end for xline
    pywmlx.nodemanip.closefile(_dictionary, _current_lineno)

