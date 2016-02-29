import os
import sys
import re


def autoscan(pathdir, scandirs):
    filelist = None
    for scandir in scandirs:
        normscan = os.path.normpath(scandir)
        scan = os.path.join(pathdir, normscan)
        for root, dirs, files in os.walk(scan, topdown=False):
            for name in files:
                rx = re.compile(r'\.(cfg|lua)$', re.I)
                m = re.search(rx, name)
                if m:
                    value = os.path.join(root, name)
                    value = value [ len(pathdir) : ]
                    if os.name == "posix":
                        value = re.sub(r'^\/', '', value)
                    else:
                        value = re.sub(r'^(?:[A-Za-z]\:)?\\', '', value)
                    if filelist is None: 
                        filelist = [ value ]
                    else:
                        filelist.append(value)
                # end if m
            # end for name
        # end for root
    # end for scandir
    return filelist
# end autoscan

