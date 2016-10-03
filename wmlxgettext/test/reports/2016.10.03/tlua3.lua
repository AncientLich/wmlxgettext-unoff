local _ = wesnoth.textdomain 'test3'

-- #######################
-- Case 1: sentence that originally doesn't have a plural form, 
--         but later will have it.
-- #######################

-- #1a

_ "sentence1 (singular)"


-- #1b

_ ('sentence1 (singular)', [[sentence1 (plural)]], 2)


-- #######################
-- Case 2: sentence that originally HAVE a plural form, 
--         but later will not.
-- #######################

-- #2a

_ (
    [==[sentence2 (singular)]==],
    "sentence2 (plural)",
    2
)

-- #2b

_ 'sentence2 (singular)'


-- ########################
-- Case 3: Sentence that, for any reason, definde different plural values 
--         in different points. 
--         Desired result: we want that the FIRST plural occurrence 
--         will be used and other plural implementations will be discarded
-- ########################

-- #3a

_ ("sentence3 (singular)", "sentence3 (plural)", 2)

-- #3b

_ ('sentence3 (singular)', 'sentence3 (WRONG PLURAL VALUE 1)', 2)

-- #3c

_ ([[sentence3 (singular)]],
   [===[sentence3 (WRONG PLURAL VALUE 2)]===],
   2)
   
-- #3d (no plural specified)
   
_ ( 
    "sentence3 (singular)"
)
   

-- ########################
-- Case 4: Combining case 1 and case 3
-- ########################
   
-- #4a
   
_ "sentence4 (singular)"

-- #4b 

_ ('sentence4 (singular)', "sentence 4 (plural)", 2)

-- #4c

_ ("sentence4 (singular)", 'sentence 4 (WRONG PLURAL)', 2)