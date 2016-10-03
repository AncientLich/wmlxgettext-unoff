_ = wesnoth.textdomain 'test1'

_ "sentence 1, single line"

_ 'sentence 2, single line'

_ [==[ sentence 3, single line ]==]


_ [===[ ML
sentence 3
multi line ]==] ok]===]


_ ("sentence 1, standard")

_ ('sentence 2, standard')

_ ( [==[sentence
    3
    standard]==] 
)
    
_ (
    "sentence 1b, standard"
)



_ ("plural1 (singular)", 'plural1 (plural)', 2)

_ ('plural2 (singular)', [=[plural2 (plural)]=], 2)

_ (
    [==[plural3 (singular)
multiline
xyz]==],
    [===[plural3 (plural)
multiline
xyz]===] )

