digraph wmlerr {
   node [shape="ellipse", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"]
   
   wmlerr1 [label="wmlerr/wmlwarn"]
   explain_dual [shape="box", fillcolor="purple",
          label="wmlerr/wmlwarn sends its own finfo, info"]
   dualcol [label="dualcol_message"]
   explain_dual2 [shape="box", fillcolor="purple",
          label="Dualcol will return an unique string \"fileinfo:x: message\"\n(\"fileinfo:x\" will be yellow, \"message\" will be white)"
   ]
   wmlerr2 [label="wmlerr/wmlwarn"]
   explain_print [shape="box", fillcolor="purple",
          label="wmlerr/wmlwarn sends the string already obtained"
   ]
   printx [label="print_wmlerr"]
   notex [shape="box", fillcolor="purple", 
          label="The second parameter (iserror)\nis True when called by wmlerr (\"error:\" -> red)\nis False when called by wmlwarn (\"warning\" -> blue)"    
   ]
   msg [shape="box", fillcolor="purple", 
          label="print_wmlerr actually prints the error/warning message to stderr"
   ]
   
   wmlerr1 -> explain_dual -> dualcol -> explain_dual2 -> wmlerr2
   wmlerr2 -> explain_print -> printx
   wmlerr2 -> notex -> printx
   printx -> msg
} 

