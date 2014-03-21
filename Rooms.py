# Rooms.py
"""
contains all the rooms in the game, separated by region
"""

import World


master = {}

test = {
	'lobby':World.Room(),
	'restroom':World.Room(), 
	'outside':World.Room()
	}




test['lobby'].region = 'test'
test['lobby'].name = 'lobby'
test['lobby'].description = 'A dark and musty lobby.'
test['lobby'].longDescription = 'This lobby is dingy and poorly lit.  It looks like it has not been cleaned in years, and you doubt it is a very popular place to hang out.  You probably should move on.'
test['lobby'].exits = {
	'restroom':test['restroom'], 
	'outside':test['outside']
	}
master['testLobby'] = test['lobby']


test['restroom'].region = 'test'
test['restroom'].name = 'restroom'
test['restroom'].description = 'A dingy restroom.'
test['restroom'].longDescription = 'You are pretty sure you have never seen a more disgusting restroom.  It is not possible for anyone to use anything in here, due to the filth.'
test['restroom'].exits = {
	'lobby':test['lobby']
	}
master['testRestroom'] = test['restroom']


test['outside'].region = 'test'
test['outside'].name = 'outside'
test['outside'].description = 'The scary, wide world.'
test['outside'].longDescription = 'No, really.  This is everything else.  It is far too much to describe right now.  If you want to know what this looks like, quit this MUD and step outside.'
test['outside'].exits = {
	'lobby':test['lobby']
	}
master['testOutside'] = test['outside']



startingRoom = test['lobby']