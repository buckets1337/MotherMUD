# Rooms.py
"""
contains all the rooms in the game, separated by region; this file also describes the contents of each room
"""

#------------------------------------------------------------------------------------------------------------------------------------------------
# This defines almost all of the game's content.  Therefore, it is important to understand how it is working. An explanation of each part
# lies in the comments below.
#
# Some general structural information follows. 
#
# Every room in the world must be contained in the 'master' dictionary.  This is accomplished
# by adding each room to the master dictionary after the room's attributes have been defined, where the key is a string combining the
# region and roomname, with the first letter of the room name capitalized.  The value is a reference to the room within the region's dictionary.
# For example, if the room "batcave" was located in the region Gotham, the entry for the master dictionary would look like
# " master['gothamBatcave'] = gotham['batcave'] ".
#
# Every region also has a dictionary of rooms, where the key is the name of the room, and the value is a blank instance of World.room.  Once a 
# region's dictionary has been filled with all the rooms in the region, each room must then have it's attributes set, and then must be added to
# the master dictionary.  This is accomplished with dot attribute notation on the items in the region's dictionary.  For example:
# gotham['batcave'].region = 'gotham'
# gotham['batcave'].name = 'batcave'
# gotham['batcave'].description = 'Batman's base.'
# gotham['batcave'].longDescription = 'A high tech cave, filled with all the newest gadgets.'
# gotham['batcave'].exits = {
#     'mansion':gotham['mansion']
#     'hangar':gotham['hangar']
# }
# ...and so on.  It is important to remember to assign each room to the master dictionary, AFTER the attributes have been set.
#-------------------------------------------------------------------------------------------------------------------------------------------------

import World
import Objects

def setCurrentRoom(objectList, currentRoom):		# sets the currentRoom attribute for items in 'objectList'
	for obj in objectList:
		if isinstance(obj.kind, World.container):
			if obj.kind.inventory != []:
				for ob in obj.kind.inventory:
					ob.currentRoom = currentRoom
		obj.currentRoom = currentRoom

###################################################################################################################################################
# This section contains the master dictionary, holding a reference to every room in the game

master = {}

# An example of a region dictionary, holding a reference to a blank instance of World.Room for each room in the region
test = {
	'lobby':World.Room(),
	'restroom':World.Room(), 
	'outside':World.Room(),
	'bullpen':World.Room()
	}



####################################################################################################################################################
# This section defines the contents and attributes of each room, and then assigns them to the master list

# The lobby
room = test['lobby']		# lets objects in the room know which room they are in
test['lobby'].region = 'test'
test['lobby'].name = 'lobby'
test['lobby'].description = 'A dark and musty lobby.'
test['lobby'].longDescription = 'This lobby is dingy and poorly lit.  It looks like it has not been cleaned in years, and you doubt it is a very popular place to hang out.  You probably should move on.'
test['lobby'].exits = {
	'restroom':test['restroom'], 
	'outside':test['outside']
	}
test['lobby'].objects = [				# note: objects inside a container do not have to be defined here, as they are defined in Objects.py
	Objects.testLobbyPottedPlant,		# This list is just for 'top level' objects in the room, visible or not
	Objects.testLobbyDesk,
	Objects.testLobbyDeskDrawer,
	]
setCurrentRoom(test['lobby'].objects, room)
master['testLobby'] = test['lobby']


# The restroom
room = test['restroom']
test['restroom'].region = 'test'
test['restroom'].name = 'restroom'
test['restroom'].description = 'A dingy restroom.'
test['restroom'].longDescription = 'You are pretty sure you have never seen a more disgusting restroom.  It is not possible for anyone to use anything in here, due to the filth.'
test['restroom'].exits = {
	'lobby':test['lobby']
	}
test['restroom'].objects = [
	Objects.testTrashcan
]
setCurrentRoom(test['restroom'].objects, room)
master['testRestroom'] = test['restroom']


# The outside
room = test['outside']
test['outside'].region = 'test'
test['outside'].name = 'outside'
test['outside'].description = 'The scary, wide world.'
test['outside'].longDescription = 'No, really.  This is everything else.  It is far too much to describe right now.  If you want to know what this looks like, quit this MUD and step outside.'
test['outside'].exits = {
	'lobby':test['lobby']
	}
test['outside'].objects = [
	Objects.testRock,
	Objects.testGardenGnome
	]
setCurrentRoom(test['outside'].objects, room)
master['testOutside'] = test['outside']


#-----------------------------------------------------------------------------------------------------------------------------------------------------

# The bullpen.  This is a place to put things that you don't want the clients being able to get to, but need to exist for spawner calls, etc.
# Each region should have a bullpen.
room = test['bullpen']
test['bullpen'].region = 'test'
test['bullpen'].name = 'bullpen'
test['bullpen'].description = 'An endless white room.'
test['bullpen'].longDescription = "This room is white.  So white that you can't tell where the walls meet the floor and ceiling, or even where the ceiling is at all."
test['bullpen'].exits = {
	'lobby':test['lobby']
	}
test['bullpen'].objects = [
	]
setCurrentRoom(test['bullpen'].objects, room)
master['testBullpen'] = test['bullpen']


#####################################################################################################################################################

# This variable defines the room that new players will spawn in when first entering the world
startingRoom = test['lobby']