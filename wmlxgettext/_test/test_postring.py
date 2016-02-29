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

from pywmlx.postring import *



class Test_PoCommentedString(unittest.TestCase):
    # test PoCommentedString.__init__ and check if initializer was 
    # corrupted during a change.
    # during this test we use "improper values" becouse we need only 
    # to match if the init parameter order / name is changed or not
    def test_pocomstr_init(self):
        ps = PoCommentedString("sentence", orderid=(1,2,3), 
                         ismultiline="multiline", wmlinfos="infos",
                         finfos="finfos", addedinfos="added")
        self.assertEqual(ps.sentence, "sentence")
        self.assertEqual(ps.orderid, (1,2,3))
        self.assertEqual(ps.wmlinfos, "infos")
        self.assertEqual(ps.finfos, "finfos")
        self.assertEqual(ps.addedinfos, "added")
        self.assertEqual(ps.ismultiline, "multiline")
  
    # test PoCommentedString.update_fileline
    def test_pocomstr_update_orderid(self):
        ps = PoCommentedString("test", ismultiline=True, 
                          orderid=(1000,1000,0), 
                          wmlinfos=[], finfos=[], addedinfos=[])
        values = [ ("up, up: ", (1001,1100,0), (1000,1000,0) ),
                   ("up, down: ", (1001,1,0), (1000,1000,0) ),
                   ("equal, up: ", (1000,1100,0), (1000,1000,0) ),
                   ("equal, down: ", (1000,900,0), (1000,900,0) ),
                   ("down, up: ", (900,1100,0), (900,1100,0) ),
                   ("down, equal: ", (800,1100,0), (800,1100,0) ),
                   ("down, down: ", (600,700,0), (600,700,0) ),
                   ("float test(1): ", (600,600,9), (600,600,9) ),
                   ("float test(2): ", (600,600,15), (600,600,9) ),
                   ("float test(3): ", (600,600,3), (600,600,3) )  ]
        for (errorstr, orderid, expected_orderid) in values:
                ps.update_orderid(orderid)
                self.assertEqual(ps.orderid, expected_orderid, errorstr)
            
    # test PoCommentedString.update_with_commented_string
    def test_pocomstr_updcstr(self):
        # test1: verify string, update_fileline, 
        #        and cloning (wml_infos, added_infos)
        # It doesn't matter testing finfos, since the
        # line_by_line parsing makes impossible to have the same file 
        # and the same line twice
        ps0 = PoCommentedString("string", ismultiline=True, 
                           orderid=(100,1,0),
                           wmlinfos=["#. [message]: speaker = Daruan"],
                           finfos=["#: path/file/100: 1"], 
                           addedinfos=["#. added_infos"])
        ps1 = PoCommentedString("string2", ismultiline=False, 
                           orderid=(1,100,0), 
                           wmlinfos=["#. [message]: speaker = Daruan"],
                           finfos=["#: path/file/100: 1"], 
                           addedinfos=["#. added_infos"])
        ps2 = PoCommentedString("string3", ismultiline=False, 
                    orderid=(12,13,0),
                    wmlinfos=["#. [message]: speaker = Daruan, gender = male"],
                    finfos=["#: path/file/100: 1"], 
                    addedinfos=["#. added_infos2"])
        ps0.update_with_commented_string(ps1)
        ps0.update_with_commented_string(ps2)
        self.assertEqual(ps0.sentence, "string")
        self.assertEqual(ps0.orderid, (1,100,0))
        self.assertEqual(len(ps0.wmlinfos), 2) #2 and not 3 (clones erased)
        self.assertEqual(len(ps0.finfos), 3)
        self.assertEqual(len(ps0.addedinfos), 3)
        self.assertEqual(ps0.wmlinfos[1], 
                         "#. [message]: speaker = Daruan, gender = male")
        self.assertEqual(ps0.finfos[2], "#: path/file/100: 1")
        self.assertEqual(ps0.addedinfos[2], "#. added_infos2")
        self.assertTrue(ps0.ismultiline)
        
    #def altro
  
    # def test_isupper(self):
        # self.assertTrue('FOO'.isupper())
        # self.assertFalse('Foo'.isupper())

    # def test_split(self):
        # s = 'hello world'
        # self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        # with self.assertRaises(TypeError):
          # s.split(2)



class Test_WmlNodeSentence(unittest.TestCase):
    def test_init(self):
        wns = WmlNodeSentence("sentence", ismultiline="multiline", 
                              lineno="lineno", lineno_sub="lineno_sub", 
                              override="override", addition="addition")
        self.assertEqual(wns.sentence, "sentence")
        self.assertEqual(wns.ismultiline, "multiline")
        self.assertEqual(wns.lineno, "lineno")
        self.assertEqual(wns.lineno_sub, "lineno_sub")
        self.assertEqual(wns.overrideinfo, "override")
        self.assertEqual(wns.addedinfo, "addition")



class Test_WmlNode(unittest.TestCase):
    def test_init(self):
        wn = WmlNode(fileref="fileref", fileno="fileno", 
                     tagname="tagname", autowml="autowml")
        wn2 = WmlNode(fileref="fileref", fileno="fileno", 
                      tagname="tagname")
        self.assertEqual(wn.fileref, "#: fileref:")
        self.assertEqual(wn.fileno, "fileno")
        self.assertEqual(wn.tagname, "tagname")
        self.assertEqual(wn.autowml, "autowml")
        self.assertTrue(wn2.autowml)
       
    def test_addsentence(self):
        vn = WmlNode(fileref="fileref", fileno="fileno", 
                     tagname="tagname", autowml="autowml")
        vn.add_sentence("sentence", ismultiline=True, lineno="lineno", 
                        lineno_sub="lineno_sub", override="override", 
                        addition="addition")
        vn.add_sentence("sentence1", ismultiline=False, lineno=11)
        s1, s2 = vn.sentences
        self.assertEqual(s1.sentence, "sentence")
        self.assertEqual(s1.lineno, "lineno")
        self.assertEqual(s1.lineno_sub, "lineno_sub")
        self.assertEqual(s1.overrideinfo, "override")
        self.assertEqual(s1.addedinfo, "addition")
        self.assertTrue(s1.ismultiline)
        self.assertEqual(s2.lineno_sub, 0)
        self.assertEqual(s2.overrideinfo, None)
        self.assertEqual(s2.addedinfo, [])
    
    def test_assemble_wmlinfo(self):
        vn = WmlNode(fileref="fileref", fileno="fileno", 
                     tagname="[tagname]", autowml="autowml")
        vn.wmlinfos = []
        vn.wmlinfos.append("speaker = Daruan")
        vn.wmlinfos.append("gender = male")
        vn.wmlinfos.append("role = hero")
        self.assertEqual(vn.assemble_wmlinfo(), 
                  "#. [tagname]: speaker = Daruan, gender = male, role = hero")
                  
    def test_assemble_orderid(self):
        vn = WmlNode(fileref="fileref", fileno=255, tagname="tagname")
        vns1 = WmlNodeSentence("sentence", ismultiline=True, 
                      lineno=10, lineno_sub=5,
                      override="override", addition="addition")
        vns2 = WmlNodeSentence("sentence", ismultiline=True, 
                      lineno=15, lineno_sub=90, 
                      override="override", addition="addition")
        vns3 = WmlNodeSentence("sentence", ismultiline=True, lineno=51)
        vns4 = WmlNodeSentence("sentence", ismultiline=True, lineno=70, 
                               override="override", addition="addition")
        self.assertEqual(vn.assemble_orderid(vns1), (255,10,5) )
        self.assertEqual(vn.assemble_orderid(vns2), (255,15,90) )
        self.assertEqual(vn.assemble_orderid(vns3), (255,51,0) )
        self.assertEqual(vn.assemble_orderid(vns4), (255,70,0) )
    
    def test_nodesentence_to_posentence(self):
        # here we simply translate EVERY WmlNodeSentence(s) into 
        # PoCommentedString(s) without caring if it is a duplicated 
        # PoCommentedString or not.
        # this test iterates various controls.
        # it tests all PoCommentedString(s) values in 6 major cases 
        # tested two times: with node1.autowml = true and with 
        # node1.autowml = false
        #
        # the inputs we gave to node1.add_sentence in the 6 cases
        keys = ["sentence", "ismultiline", "lineno",
                "lineno_sub", "override", "addition" ]
        inputs = [ ("sono Daruan", True, 47),
                   ("sono Daruan - empty_override", False, 101, 0, ""),
                   ("sono Daruan - overridden", True, 102, 0, "#. override"),
                   ("sono Daruan - overridden + addition", False, 103, 1, 
                             "#. override", ["#. addition", "#. addition2"]),
                   ("sono Daruan - empty_override + addition", True, 104, 2, 
                             "", ["#. addition"]),
                   ("sono Daruan - addition only", False, 105, 7, 
                             None, ["#. addition"])]
        # the "debug name" (showed as "type") of the 6 cases.
        # used by assertEqual message error, if an error encountered
        nodetype = ("standard", "'empty override'", "'override'",
                    "'override + addition'", "'empty override + addition'",
                    "'addition'")
        # expected node1.multiline value on every test case
        multi = (True, False, True, False, True, False)
        # expected node1.lineno value on every test case
        orderid = [ (1,47,0), (1,101,0),  (1,102,0), (1,103,1),  
                    (1,104,2), (1,105,7) ]
        # expected node1.finfos value on every test case
        finfos = (["#: path/to/file1:47"], ["#: path/to/file1:101"], 
                  ["#: path/to/file1:102"], ["#: path/to/file1:103"],
                  ["#: path/to/file1:104"], ["#: path/to/file1:105"])
        # expected node1.wml_infos value on every test case 
        # (when autowml = true)
        wmlinfs = (["#. [message]: speaker = Daruan, gender = male"], [], 
                   ["#. override"], ["#. override"], [],
                   ["#. [message]: speaker = Daruan, gender = male"])
        # expected node1.wml_infos value on every test case 
        # (when autowml = false)
        wmlinfs2 = ([], [], ["#. override"], ["#. override"], [], [])
        # expected node1.sentence value on every test case
        sent = ("sono Daruan", "sono Daruan - empty_override", 
                "sono Daruan - overridden", 
                "sono Daruan - overridden + addition", 
                "sono Daruan - empty_override + addition", 
                "sono Daruan - addition only")
        # expected node1.added_infos value on every test case
        addedinfo = ([], [], [], ["#. addition", "#. addition2"],
                     ["#. addition"], ["#. addition"])
        # we should repeat the 6 major cases two times:
        # when autowml = True; when autowml = False
        autowmlii = [True, False]
        #
        # Here we start the loops where the actual test is executed
        # first do the checks with autowml == true 
        #    (executing the 6 major test cases, first time)
        # than do again the checks with autowml == false
        #    (executing the 6 major test cases, second time)
        for autowml in autowmlii:
            node1 = WmlNode(fileref="path/to/file1", fileno=1, 
                            tagname="[message]", autowml=autowml)
            node1.wmlinfos = []
            node1.wmlinfos.append("speaker = Daruan")
            node1.wmlinfos.append("gender = male")
            for value in inputs:
                node1.add_sentence( **dict(zip(keys,value)) )    
            if autowml == True:
                errormsg = "\n\nWmlNode: nodesentence_to_posentence " \
                            "(when node autowml=true): "
            else:
                errormsg = "\n\nWmlNode: nodesentence_to_posentence " \
                            "(when node autowml=false): "
            for i in range(6):
                mystr = node1.nodesentence_to_posentence(node1.sentences[i])
                myerr = errormsg + "nodetype = " + nodetype[i] 
                self.assertEqual(mystr.sentence, sent[i], myerr)
                self.assertIs(mystr.ismultiline, multi[i], myerr)
                self.assertEqual(mystr.orderid, orderid[i], myerr)
                self.assertEqual(mystr.finfos, finfos[i], myerr)
                self.assertEqual(mystr.addedinfos, addedinfo[i], myerr)
                if autowml is True:
                    self.assertEqual(mystr.wmlinfos, wmlinfs[i], myerr)
                else:
                    self.assertEqual(mystr.wmlinfos, wmlinfs2[i], myerr)
        

