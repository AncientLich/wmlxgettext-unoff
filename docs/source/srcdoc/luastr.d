digraph luastr {
   node [shape="record", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   idle [shape="ellipse", label="LUA IDLE STATE", fillcolor="green"]
   
   str01 [
     label="{LuaStr01|type 1|{(single line)|(first line of multiline string)}}"
   ]
   str10 [ color="red", fillcolor="#ffaaaa",
     label="{LuaStr10|type 1|(multiline string: from line 2 to last line)}"
   ]
   
   str02 [
     label="{LuaStr02|type 2|{(single line)|(first line of multiline string)}}"
   ]
   str20 [ color="red", fillcolor="#ffaaaa",
     label="{LuaStr20|type 2|(multiline string: from line 2 to last line)}"
   ]
   
   str03 [
     label="{LuaStr03|type 3|(single line ONLY)}"
   ]
   str03o [
     label="{LuaStr03o|type 3|(multiline string: line 1)}"
   ]
   str30 [ color="red", fillcolor="#ffaaaa",
     label="{LuaStr30|type 3|(multiline string: from line 2 to last line)}"
   ]
      
   nextstate [label="Next State", shape="box", fillcolor="orange"]
   
   str01 -> str02 -> str03 -> str03o -> nextstate
   str01 -> idle [color="blue"]
   str01 -> str10 [style="dotted", color="blue"]
   str02 -> idle [color="blue"]
   str02 -> str20 [style="dotted", color="blue"]
   str03 -> idle [color="blue"]
   str03o -> str30 [color="blue"]
   str10 -> str10
   str20 -> str20
   str30 -> str30
   str10 -> idle
   str20 -> idle
   str30 -> idle
} 

