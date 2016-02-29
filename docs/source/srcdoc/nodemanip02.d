digraph nodemanip02 {
   node [shape="box", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"
   ]
   
   manip [fillcolor="orange",
      label="Nodemanip module"
   ]
   delnode [shape="ellipse", fillcolor="purple",
      label="a WML [/closing_tag] found"
   ]
   nodelistquestion [shape="diamond",
      label="Is that [/closing_tag] expected?"
   ]
   no1 [shape="record", fillcolor="#ffaaaa", color="red",
      label="{node list is empty|no closing tag expected}"
   ]
   no2 [shape="record", fillcolor="#ffaaaa", color="red",
      label="{current node is ROOT|no closing tag expected}"
   ]
   no3 [shape="record", fillcolor="#ffaaaa", color="red",
      label="{current node.tagname \ndoes not match [/tagname]|another closing tag expected}"
   ]
   err [color="red",
      label="critical error (wmlerr())"
   ]
   yes [fillcolor="green",
      label="the [/closing_tag]\nis the expected one"
   ]
   conv [
      label="take WmlNodeSentence objects\n and convert them in\ntemporary PoCommentedString objects"   
   ]
   upd [
      label="update dictionary using\n those temporary objects"
   ]
   cle [
      label="and finally\nclear the node\nremoving it from list"   
   ]
   
   manip -> delnode -> nodelistquestion
    
   nodelistquestion -> yes [label="yes", color="darkgreen"]
   nodelistquestion -> no1 [label="no", color="red"]
   nodelistquestion -> no2 [label="no", color="red"]
   nodelistquestion -> no3 [label="no", color="red"]
   yes -> conv -> upd -> cle
   no1 -> err 
   no2 -> err 
   no3 -> err 
} 

