import os
import sys
import warnings

enabled_ansi_col = True
is_utest = False
_warnall = False


def wmlerr_debug():
    global is_utest
    is_utest = True



def ansi_setEnabled(value):
    global enabled_ansi_col
    enabled_ansi_col = value
 


def warnall():
    return _warnall



def set_warnall(value):
    _warnall = value



class WmlError(ValueError):
    pass

class WmlWarning(UserWarning):
    pass



def print_wmlerr(finfo, message, iserr):
    # red if error, blue if warning
    ansi_color = '\033[91;1m' if iserr else '\033[94m'
    errtype = "error:" if iserr else "warning:"
    # now we have ascii_color and errtype values
    # here we print the error/warning. 
    # 1) On posix we write "error" in red and "warning" in blue
    if os.name == "posix" and enabled_ansi_col is True:
        msg = ansi_color + errtype + ' \033[0m\033[93m' + finfo + ':\033[0m ' \
              + message
    # 2) On non-posix systems (ex. windows) we don't use colors
    else:
        msg = errtype + ' ' + finfo + ': ' + message
    print(msg, file=sys.stderr)



def my_showwarning(message, category, filename, lineno, file=None, line=None):
    try:
        finfo, msg = message.args[0].split(": ", 1)
        print_wmlerr(finfo, msg, False)
    except OSError:
        pass # the file (probably stderr) is invalid - this warning gets lost.



warnings.showwarning = my_showwarning



def wmlerr(finfo, message, errtype=WmlError):
    if not is_utest:
        try:
            raise errtype(finfo + ": " + message)
        except errtype as err:
            print_wmlerr(finfo, message, True)
            sys.exit(1)
    else:
        raise errtype(finfo + ": " + message)



def wmlwarn(finfo, message):
    warnings.warn(finfo + ": " + message, WmlWarning)

