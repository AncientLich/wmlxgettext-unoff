digraph wmlstr {
   rankdir=LF
   node [shape="ellipse", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   
   wmltag [shape="box", fillcolor="green",
           label="WmlTagState regexp"
   ]
   tagfound1 [
       label="[tag]\nstays alone"
   ]
   tagfound2 [
       label="[tag] in macro-call"
   ]
   question [ shape="diamond",
       label="Are there\nquotes (\")\nbefore the [tag]?"
   ]
   match [ 
       label="regex matches:\n[tagname] will be collected\nby WmlTagState"
   ]
   nomatch [ 
       label="regex does not match:\nWmlStr01 can be reached"
   ]
   
   wmlstr01 [
       label="WmlStr01 state can\ncollect the sentence\n included between quotes"
   ]
   
   wmlstr02 [
       label="WmlStr01 state will consume the parsed line\n until the closing quote reached.\n (The quoted string will be removed\nfrom the line to parse)"
   ]
   
   wmlstr03 [ fillcolor="cyan",
       label="WmlTagState, next time,\n(when all quotes will be removed after executing WmlStr01 state)\nwill be able to match the [tagname]"
   ]
   
   {rank=same tagfound1 tagfound2}
   {rank=same match nomatch}
   
   
   wmltag -> tagfound1 -> match
   wmltag -> tagfound2 -> question
   
   question -> nomatch [label="yes"]
   question -> match [label="no"]
   
   nomatch -> wmlstr01 -> wmlstr02 -> wmlstr03 -> match
} 

