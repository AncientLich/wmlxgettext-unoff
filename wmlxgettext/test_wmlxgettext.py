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

from _test.test_postring import Test_PoCommentedString
from _test.test_postring import Test_WmlNodeSentence
from _test.test_postring import Test_WmlNode

from _test.test_nodeman import Test as Test_nodeman
from _test.test_state import Test_State
from _test.test_luastates import Test_LuaStates
from _test.test_wmlstates import Test_WmlStates

'''
        
    def check_closenode(self, autowml):
        my_dict = {'sono daruan': PoCommentedString("sono daruan", 
                                 is_multiline=False, orderid=(1,1,0),
                                 wml_infos=["#. [message] speaker = Daruan"],
                                 finfos=["#: path/to/file1:1"],
                                 added_infos=[]) }
        node1 = WmlNode(fileref="path/to/file2", fileno=2, 
                        tagname="[message]", autowml=autowml)
        node1.wml_infos.append("speaker = Daruan2")
        # empty override
        node1.add_sentence("sono daruan", is_multiline=False, my_lineno=15, 
                           my_override="")
        # standard
        node1.add_sentence("sono daruan", is_multiline=False, my_lineno=18)
        # addition
        node1.add_sentence("sono darUan", is_multiline=False, my_lineno=21, 
                           my_lineno_sub=3, my_addition=["#. added1"])
        # new sentence: (override + addition)
        node1.add_sentence("dax", is_multiline=True, my_lineno=30, 
                           my_override=["override"], my_addition=["add1"])
        # sent2: empty override + addition)
        node1.add_sentence("dax", is_multiline=False, my_lineno=31,
                           my_override= "", my_addition=["add2"])
        
        # sent2: override only
        node1.add_sentence("dax", is_multiline=False, my_lineno=31,
                           my_override= "override2")
        
        node1.close_node(my_dict)
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
        self.assertEqual(len(strl0.added_infos), 1)
        if autowml is True:
            self.assertEqual(len(strl0.wml_infos), 2)
            self.assertEqual(strl0.wml_infos[1], 
                             '#. [message]: speaker = Daruan2')
        else:
            self.assertEqual(len(strl0.wml_infos), 1)
        # other test, if needed
    
    def test_closenode_true(self):
        self.check_closenode(True)
    
    def test_closenode_false(self):
        self.check_closenode(False)
        
    # def nuovo    
        
        
        
class TestNodeManip(unittest.TestCase):
    def test_init(self):
        nm = NodeManip("fileref", "fileno")
        self.assertEqual(nm.fileref, "fileref")
        self.assertEqual(nm.fileno, "fileno")
        self.assertEqual(len(nm.nodes), 1)
        nod = nm.nodes[0]
        self.assertEqual(nod.fileref, "#: fileref:")
        self.assertEqual(nod.fileno, "fileno")
        self.assertEqual(nod.tagname, "")
        self.assertFalse(nod.autowml)
        
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
 

'''

if __name__ == '__main__':
    unittest.main()

