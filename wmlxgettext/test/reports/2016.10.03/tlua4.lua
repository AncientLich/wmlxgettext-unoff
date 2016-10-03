-- the 'RIGHT' textdomain is 'test4'
-- All sentences under other textdomain should not be collected

local _ = wesnoth.textdomain 'wrong-textdomain-1'

_ ("WRONG SENTENCE #1 (singular)", "(plural)", 2)

_ ("WRONGE SENTENCE #2")

local _ = wesnoth.textdomain "test4"

_ ('sentence1')

_ ("sentence2 (singular)", 'sentence2 (plural)', 2)

_ 'sentence3'

local _ = wesnoth.textdomain 'wrong-textdomain-2'

_ 'WRONG SENTENCE #3'

_ "WRONG SENTENCE #4"

_ [==[WRONG
SENTENCE
5]==]

local _ = wesnoth.textdomain "test4"

_ (
    [[multiline
sentence
(singular)]],
[==[multiline
sentence
(plural)]==],
2
)


local _ = wesnoth.textdomain "wrong-textdomain-3"

_ (
    [[WRONG multiline
sentence
(singular)]],
[==[WRONG multiline
sentence
(plural)]==],
2
)

