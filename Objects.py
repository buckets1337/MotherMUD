# Objects.py
"""
This file defines the various different objects that can be found in the world
"""

#--------------------------
# This file defines the objects in the world.  Best practice for naming an object follows: <region><Room><Name>, where the region is lowercase and every other word in the smashed string is capitalized
#--------------------------


import World



room = None

def setLocation(location):
	global room
	room = location



testLobbyPottedPlant = World.Object(
	name = 'potted plant',
	description = 'A plant in a pot.',
	currentRoom = room, 
	isVisible = True,
	longDescription = 'This appears to be a long-neglected fern of some sort, in a crumbling ceramic pot.'
)

testLobbyDesk = World.Object(
	name = 'desk',
	description = 'A cheap plywood desk',
	currentRoom = room,
	isVisible = True,
	longDescription = "This desk looks like it was flimsy even when it was new.  It has a single desk drawer which does not appear to be locked."
)

testLobbyKey =  World.Object(
	name = 'rusty key',
	description = 'An old rusty key.',
	currentRoom = room,
	isVisible = False,
	longDescription = "This key appears to be old.  It has to go to something around here, since it was in the desk.",
)

deskContainer = World.container(inventory=[testLobbyKey], respawnContents=True)

testLobbyDeskDrawer = World.Object(
	name = 'desk drawer',
	description = 'An unlocked desk drawer.',
	currentRoom = room,
	isVisible = False,
	longDescription = "This is an ordinary desk drawer.  It has a lock on it, but it does not appear to be engaged.",
	kind = deskContainer
)

