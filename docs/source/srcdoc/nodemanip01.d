digraph nodemanip01 {
   node [shape="box", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"
   ]
   
   manip [shape="record", fillcolor="orange",
      label="{Nodemanip module|stores WML nodes in a list\n(on the global _nodes variable)}"
   ]
   newnode [shape="ellipse", fillcolor="purple",
      label="A new WML node must be created"
   ]
   nodelistquestion [shape="diamond",
      label="Is node list empty?"
   ]
   nodelistempty [
      label="Create a ROOT node\n(tagname=\"\")"   
   ]
   createnode [
      label="Create the WML [tag] node"
   ]
   
   manip -> newnode -> nodelistquestion
    
   nodelistquestion -> nodelistempty  [label="yes"]
   nodelistempty -> createnode
   nodelistquestion -> createnode [label="no"]
} 

