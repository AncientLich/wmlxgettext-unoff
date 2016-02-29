digraph machine01 {
   node [shape="box", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   idle [shape="ellipse", label="IDLE STATE", fillcolor="green"]
   idle2 [label="IDLE STATE of the other language", fillcolor="cyan"]
   preproc [label="Preprocessing and Comment STATES"]
   winfo [label="WML TAG/INFO STATES", fillcolor="yellow"]
   cstr [label="Capture String STATE (single-line?)", 
         shape="box", color="red", fillcolor="#ffaaaa"]
   mult [label="Multi-Line String STATE", color="red",
         fillcolor="#ffaaaa"]
   change [label="Change language STATE"]
   end [shape="ellipse", label="FINAL STATE", fillcolor="green"]
  
   idle -> preproc [color="darkgreen"]
   preproc -> winfo -> cstr -> change -> end
   preproc -> idle [color="blue"]
   winfo -> idle [color="blue"]
   cstr -> idle [color="blue"]
   cstr -> mult [style="dotted", color="blue"]
   mult -> mult
   mult -> idle
   change -> idle2 [color="blue"]
   end -> idle [color="darkgreen"]
} 

