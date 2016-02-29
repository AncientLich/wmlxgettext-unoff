digraph nodemanip03 {
   rankdir=LF
   node [shape="box", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"
   ]
   
   manip [fillcolor="orange"
      label="Nodemanip module"
   ]
   endreach [shape="ellipse", fillcolor="purple"
      label="end of WML file reached"
   ]
   func [shape="ellipse", fillcolor="purple"
      label="function nodemanip.closefile()\nwill be executed"
   ]
   if1 [ label="node list\nis empty"]
   if2 [ label="node list\nONLY contains\nroot node"]
   if3 [ color="red", fillcolor="#ffaaaa",
      label="Node list\ncontains root node\nAND other WML node(s)"
   ]
   checkroot [
      label="Check root node\ntake WmlNodeSentence objects\n and convert them in\ntemporary PoCommentedString objects"
   ]
   err [color="red",
      label="Critical error (wmlerr())"
   ]
   upd [
      label="update dictionary using\n those temporary objects"
   ]
   ok1 [ shape="circle", fillcolor="green", label="OK"]
   
   {rank=same if1 if2 if3}
   {rank=same checkroot err}
   
   manip -> endreach -> func
   func -> if1 [color="darkgreen"]
   func -> if2 [color="darkgreen"]
   func -> if3 [color="red"]
   
   if1 -> ok1
   if2 -> checkroot -> upd -> ok1
   if3 -> err 
} 

