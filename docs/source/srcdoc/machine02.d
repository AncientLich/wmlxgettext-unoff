digraph machine02 {
   node [shape="record", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   
   machine [shape="box", fillcolor="orange",
      label="State Machine"
   ]
   start [
      label="{Initialize nodemanip\neven if the parsed file\nis a .lua file|function nodemanip.newfile()}"
   ]
   lua [shape="ellipse", fillcolor="purple",
      label="Lua file"
   ]
   lua_explain [
      label="{Lua states DOES NOT use nodemanip|nodemanip is used ONLY on\npending Lua string to obtain\nfileref and fileno}"
   ]
   wml [shape="ellipse", fillcolor="purple",
      label="WML file"
   ]
   wml_explain [ shape="box"
      label="WML states use nodemanip\nto perform any action"
   ]
  
   machine -> start
   start -> lua -> lua_explain
   start -> wml -> wml_explain
} 

