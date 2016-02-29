#! /usr/bin/env python3

# Allora... 250 grammi di farina, 100 grammi di burro, 100 di zucchero, un uovo, mezza bustina di lievito e 50 grammi di gocce di cioccolato.
# In una ciotola si impastano farina, zucchero, lievito, burro ammorbidito e uovo.
# Fatto questo, incorpori all'impasto le gocce di cioccolato. Poi metti l'impasto in frigorifero per una mezz'ora.
# A questo punto, rivesti due teglie di carta forno e dai la forma ai biscotti. Puoi stenderli con un mattarello e tagliarli con delle formine.
# Poi li devi cuocere in forno a 180 gradi per 15-20 minuti - appena vedi che il bordo è dorato puoi toglierli.
# Appena li sforni sono morbidi, ma quando si raffreddano diventano belli croccanti.

# Tieni presente che ogni forno è una storia a sé, quindi potresti dover alzare o abbassare leggermente la temperatura, 
# o modificare la durata della cottura.
# switch --force per forzare la generazione dei po


#  if iserror is False:
#   # warning
#  with self.assertWarns(WmlWarning) as w:
#  nm.close_node(**closevals)
#  self.assertEqual(w.warnings[0].message.args[0], mymessage)

# parsingintro.sourceforge.net

# import re
import unittest
import re

# from wmlxgettext import *

from pywmlx.wmlerr import wmlerr
from pywmlx.wmlerr import wmlwarn
from pywmlx.wmlerr import ansi_setEnabled
from pywmlx.wmlerr import wmlerr_debug
from pywmlx.wmlerr import WmlError
from pywmlx.wmlerr import WmlWarning

import pywmlx.nodemanip as nm

from pywmlx.postring import *



class Test(unittest.TestCase):
    def test_newfile(self):
        nm.newfile('fileref', 'fileno')
        self.assertEqual(nm.fileref, "fileref")
        self.assertEqual(nm.fileno, "fileno")
        self.assertIs(nm.nodes, None)
    
    def test_newnode(self):
        nm.newfile('fileref', 'fileno')
        nm.newnode('message')
        self.assertEqual(len(nm.nodes), 2)
        root = nm.nodes[0]
        nod = nm.nodes[1]
        self.assertEqual(root.fileref, "#: fileref:")
        self.assertEqual(root.fileno, "fileno")
        self.assertEqual(root.tagname, "")
        self.assertFalse(root.autowml)
        self.assertEqual(nod.tagname, "message")
        self.assertTrue(nod.autowml)
    
    def test__closenode_update_dict(self):
        nm.newfile('fileref', 2)
        nm.newnode('message')
        nm.nodes[-1].add_sentence("frase_test", ismultiline=False, 
                lineno=5, lineno_sub=1, override="override",
                addition=["addition1", "addition2"])
        my_dict = {'sono daruan': PoCommentedString("sono daruan", 
                                 ismultiline=False, orderid=(1,1,0),
                                 wmlinfos=["#. [message]: speaker = Daruan"],
                                 finfos=["#: path/to/file1:1"],
                                 addedinfos=[]) }
        nm._closenode_update_dict(my_dict)
        self.assertEqual(len(my_dict), 2)
        i = 0
        for val in sorted(my_dict.values(), 
                          key=lambda x: x.orderid):
            i+=1
            if i == 2:
                self.assertEqual(val.sentence, 'frase_test')
                self.assertFalse(val.ismultiline)
                self.assertEqual(val.orderid, (2,5,1))
        nm.newnode('[message]')
        nm.nodes[-1].add_sentence("sono daruan", ismultiline=False,
                lineno=9, lineno_sub=1)
        nm.nodes[-1].wmlinfos = [ "speaker = Daruan" ]
        nm._closenode_update_dict(my_dict)
        self.assertEqual(len(my_dict), 2)
        
        posentence = my_dict['sono daruan']
        self.assertIn("#: path/to/file1:1", posentence.finfos)
        self.assertIn("#: fileref:9", posentence.finfos)
        self.assertEqual(len(posentence.wmlinfos), 1)
        self.assertEqual(posentence.orderid, (1,1,0))
    
    
    def check_closenode(self, autowml):
        wmlerr_debug()
        nm.newfile("path/to/file2", 2)
        my_dict = {'sono daruan': PoCommentedString("sono daruan", 
                                 ismultiline=False, orderid=(1,1,0),
                                 wmlinfos=["#. [message] speaker = Daruan"],
                                 finfos=["#: path/to/file1:1"],
                                 addedinfos=[]) }
        nm.newnode("[message]")
        nm.closenode("[/message]", my_dict, 1)
        self.assertEqual(len(nm.nodes), 1)
        
        node1 = WmlNode(fileref="path/to/file2", fileno=2, 
                        tagname="[message]", autowml=autowml)
        node1.wmlinfos = [ "speaker = Daruan2" ]
        # empty override
        node1.add_sentence("sono daruan", ismultiline=False, lineno=15, 
                           override="")
        # standard
        node1.add_sentence("sono daruan", ismultiline=False, lineno=18)
        # addition
        node1.add_sentence("sono darUan", ismultiline=False, lineno=21, 
                           lineno_sub=3, addition=["#. added1"])
        # new sentence: (override + addition)
        node1.add_sentence("dax", ismultiline=True, lineno=30, 
                           override=["override"], addition=["add1"])
        # sent2: empty override + addition)
        node1.add_sentence("dax", ismultiline=False, lineno=31,
                           override= "", addition=["add2"])
        
        # sent2: override only
        node1.add_sentence("dax", ismultiline=False, lineno=31,
                           override= "override2")
        
        nm.nodes.append(node1)
        nm.closenode('[/message]', my_dict, 10)
        strl = list(my_dict.values())
        strl0 = None
        strl1 = None
        if strl[0].sentence == "sono daruan":
            strl0 = strl[0]
            strl1 = strl[1]
        else:
            strl0 = strl[1]
            strl1 = strl[0]
        self.assertEqual(len(my_dict), 2)
        self.assertEqual(len(strl0.finfos), 4)
        self.assertEqual(len(strl0.addedinfos), 1)
        if autowml is True:
            self.assertEqual(len(strl0.wmlinfos), 2)
            self.assertEqual(strl0.wmlinfos[1], 
                             '#. [message]: speaker = Daruan2')
        else:
            self.assertEqual(len(strl0.wmlinfos), 1)
        # other test, if needed
    
    def test_closenode_true(self):
        self.check_closenode(True)
    
    def test_closenode_false(self):
        self.check_closenode(False)
        
    def test_closenode_errors(self):
        wmlerr_debug()
        ansi_setEnabled(False)
        my_dict = { }
        nm.newfile("path/to/file2", 2)
        rx0 = re.compile(r'[^[]*\[\/tag].*?outside any scope', re.I)
        rx1 = re.compile(r'[^[]*\[\/tag][^[]*\[\/message]', re.I)
        with self.assertRaisesRegex(WmlError, rx0):
            nm.closenode("[/tag]", my_dict, 5)
        nm.newnode("[tag]")
        with self.assertRaisesRegex(WmlError, rx1):
            nm.closenode("[/message]", my_dict, 5)
        nm.closenode("[/tag]", my_dict, 5)
        with self.assertRaisesRegex(WmlError, rx0):
            nm.closenode("[/tag]", my_dict, 5)
        self.assertEqual(len(nm.nodes), 1)
        
    '''    
    def test_newnode(self):
        nm = NodeManip("fileref", 1)
        values = [("[lua]", False), ("[message]", True)]
        for value in values:
            tag, autowml = value
            nm.new_node(tag)
            self.assertEqual(nm.nodes[-1].tagname, tag)
            self.assertIs(nm.nodes[-1].autowml, autowml, tag)
        root = nm.nodes[0]
        self.assertEqual(len(nm.nodes), 3)
        self.assertEqual(root.tagname, "")
        self.assertFalse(root.autowml)
            
    def check_closenode(self, *, open_tag, close_tag, iserror, msg=""):
        debug_set_ansi(False)
        my_dict = {'sono daruan': PoCommentedString("sono daruan", 
                           is_multiline=False, orderid=(1,1,0),
                           wml_infos=["#. [message] speaker = Daruan"],
                           finfos=["#: filex:123"],
                           added_infos=[]) }
        nm = NodeManip("fileref", 3)
        if not open_tag == "":
            nm.new_node(open_tag)
            nm.nodes[-1].add_sentence("dax", is_multiline=False, my_lineno=5)
        closevals = {"close_tagname": close_tag, "mydict": my_dict,
                             "lineno": 7 }
        if iserror:
            # error
            with self.assertRaisesRegex(WmlError, msg):
                nm.close_node(**closevals)
        else:
            # without errors
            nm.close_node(**closevals)
            strl = list(my_dict.values())
            self.assertEqual(len(strl), 2)
            for posent in strl:
                if(posent.sentence == "sono daruan"):
                    self.assertEqual(posent.orderid, (1,1,0) )
                elif(posent.sentence == "dax"):
                    self.assertEqual(posent.orderid, (3,5,0) )
                else:
                    self.assertEqual(posent.sentence, "dax", 
                                  "sentence should be 'dax' or 'sono daruan'")
        #else:
            
        
    
    def test_closenode(self):
        values = [ {"open_tag": "[tag]", "close_tag": "[/tag]", 
                          "iserror": False },
                   {"open_tag": "[tag]", "close_tag": "[/wrong]",
                          "iserror": True,
                          "msg": re.compile(
                              r'\:7\:\s*expected[^[]*\[\/tag\]') },
                   {"open_tag": "", "close_tag": "[/tag]",
                          "iserror": True,
                          "msg": re.compile(
                              r'\:7\:\s*unexpected[^[]*\[\/tag\]') } ]
        for value in values:
            self.check_closenode(**value)
 



if __name__ == '__main__':
    unittest.main()

'''