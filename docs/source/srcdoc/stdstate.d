digraph stdstate {
   node [shape="ellipse", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   state [label="State", shape="octagon"]
   match [label="regex matches", shape="box", fillcolor="purple"]
   run [label="Execute run()"]
   notmatch [label="regex DOES NOT match", shape="box", fillcolor="purple"]
   fail [label="ChangeState: 'iffail'"]
   exe [label="Returns a tuple:\n(non_consumed_line, new_state)", 
        shape="box", fillcolor="cyan"]
   
   state -> match -> run -> exe
   state -> notmatch -> fail
} 
