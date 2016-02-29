digraph example {
         a [label="sphinx", href="http://sphinx-doc.org", target="_top",
            shape="diamond"];
         b [label="other", shape="circle"];
         SPACE [shape="record", label="{{SPACE|27}|00}"];
         a -> b -> SPACE;
         SPACE -> a;
}