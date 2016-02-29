digraph wmlstr {
   node [shape="record", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   idle [shape="ellipse", label="WML IDLE STATE", fillcolor="green"]
   
   single [     
     label="{WmlStr01|{(single line string)|(first line of multiline string)}}"
   ]
   
   mult [label="{WmlStr10|(multiline string: from line 2 to last line)}", 
         color="red", fillcolor="#ffaaaa"]
   nextstate [label="Next State", shape="box", fillcolor="orange"]
  
   single -> nextstate
   single -> idle [color="blue"]
   single -> mult [style="dotted", color="blue"]
   mult -> mult
   mult -> idle
} 

