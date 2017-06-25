digraph nodemanip03 {
   rankdir=LF
   node [shape="box", style="filled", fillcolor="grey",
         fontname="DejaVu Sans Mono"
   ]
   
   attaccare_pennetta [
       label="Attaccare la \"ciabattina USB\" con attaccata la pennetta USB al PC"
   ]
   attesa1 [
       label="Attendere qualche secondo e verificare se cliccando sull'icona della connessione (in alto)\nappare o meno la scritta \"TIM Maxxi Alice/Internet 1\"."
   ]
   q1 [shape="diamond", fillcolor="orange",
       label="La scritta\n\"Tim Maxxi...\"\nè apparsa?"
   ]
   tenta_connessione [
       label="Puoi provare a connetterti."
   ]
   scritta_non_appare [
       label="Se dopo un po' la scritta non appare allora devi eseguire il programma \"usb_connect\"\nche vedi sul Desktop.\n\"usb_connect\" ti aprirà una schermata nera che conterrà delle istruzioni." 
   ]
   usb1 [shape="ellipse", fillcolor="purple",
       label="Se \"usb_connect\" ti dice di staccare e riattaccare la pennetta"
   ]
   usb2 [shape="ellipse", fillcolor="purple",
       label="Se \"usb_connect\" ti chiede di digitare la tua password"
   ]
   usb3 [shape="ellipse", fillcolor="purple",
       label="Se \"usb_connect\" ti dice che non occorre fare nulla ed attendere"
   ]
   stacca1 [color="red", fillcolor="#ffaaaa",
       label="Stacca la pennetta USB. Attendi qualche secondo. Riattaccala e ricomincia\ntutto il processo dall'inizio"
   ]
   stacca2 [color="red", fillcolor="#ffaaaa",
       label="Stacca la pennetta USB. Attendi qualche secondo. Riattaccala e ricomincia\ntutto il processo dall'inizio"
   ]
   pwd [
       label="Digita la tua password (daniela.88). La schermata nera si chiuderà"
   ]
   attesa2 [
       label="Attendere qualche secondo. Prima o poi sull'icona della connessione (in alto)\napparirà senz'altro la scritta \"TIM Maxxi Alice/Internet 1\"."
   ]
   tentativo_ok [shape="ellipse", fillcolor="purple",
       label="Se si è connesso correttamente"
   ]
   tentativo_fallito [shape="ellipse", fillcolor="purple",
       label="Se non riesce a connettersi, ed invece si disconnette immediatamente"
   ]
   ok [fillcolor="green", 
       label="Sei riuscito a connetterti"
   ]
   avviso [
       label="Ma ricorda che la connessione è instabile"
   ]
   if1 [shape="ellipse", fillcolor="purple"
       label="Se risulta connesso, ma sembra \"non andare\""
   ]
   if2 [shape="ellipse", fillcolor="purple"
       label="Se si è disconnesso"
   ]
   disc1 [
       label="Disconnetti internet. Attendi un paio di secondi. Poi prova a riconnetterti"
   ]
   disc2 [
       label="Prova a riconnetterti"
   ]
   beta [shape="diamond", fillcolor="orange"
       label="La scritta\n\"Tim Maxxi...\"\nc'è ancora?"
   ]
   ifb1 [
       label="Prova a connetterti"
   ]
   ifb2 [
       label="Prova ad usare \"usb_connect\""
   ]
   
   
   {rank=same usb1 usb2 usb3}
   {rank=same stacca1 attesa2}
   {rank=same tentativo_ok tentativo_fallito}
   {rank=same if1 if2}
   {rank=same disc1 disc2}
   {rank=same ifb1 ifb2}
   
   attaccare_pennetta -> attesa1 -> q1
   q1 -> scritta_non_appare [color="red", label="NO"]
   scritta_non_appare -> usb1
   scritta_non_appare -> usb2
   scritta_non_appare -> usb3
   usb2 -> pwd -> attesa2
   usb3 -> attesa2 -> tenta_connessione
   usb1 -> stacca1
   q1 -> tenta_connessione [color="darkgreen", label="SI'"]
   tenta_connessione -> tentativo_ok
   tenta_connessione -> tentativo_fallito
   tentativo_fallito -> stacca2
   tentativo_ok -> ok -> avviso
   avviso -> if1 -> disc1 -> beta
   avviso -> if2 -> disc2 -> beta
   beta -> ifb1
   beta -> ifb2
   
   ifb1 -> tenta_connessione [color="blue", style="dotted"]
   ifb2 -> scritta_non_appare [color="blue", style="dotted"]
   
   
} 

