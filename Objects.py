# Objects.py
"""
This file defines the various different objects that can be found in the world
"""

#--------------------------
# This file defines the objects in the world.  Best practice for naming an object follows: <region><Room><Name>, where the region is lowercase and every other word in the smashed string is capitalized
#--------------------------


import World



def setLocation(location):
	global room
	room = location



# test region objects

testLobbyPottedPlant = World.Object(
	name = 'potted plant',
	description = 'A plant in a pot.',
	isVisible = True,
	longDescription = 'This appears to be a long-neglected fern of some sort, in a crumbling ceramic pot.'
)

testLobbyDesk = World.Object(
	name = 'desk',
	description = 'A cheap plywood desk.',
	isVisible = True,
	longDescription = "This desk looks like it was flimsy even when it was new.  It has a single desk drawer which does not appear to be locked."
)

testKeyGrabber = World.itemGrabHandler()		
testKeyItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testKeyGrabber)
testLobbyKey =  World.Object(
	name = 'rusty key',
	description = 'An old rusty key.',
	isVisible = False,
	kind = testKeyItemComponent,
	longDescription = "This key appears to be old.  It has to go to something around here, since it was in the desk.",
)

testDeskContainer = World.container(inventory=[testLobbyKey], respawnContents=True)
testLobbyDeskDrawer = World.Object(
	name = 'desk drawer',
	description = 'An unlocked desk drawer.',
	isVisible = False,
	longDescription = "This is an ordinary desk drawer.  It has a lock on it, but it does not appear to be engaged.",
	kind = testDeskContainer
)
testLobbyKey.spawnContainer = testLobbyDeskDrawer

testRockGrabber = World.itemGrabHandler()
testRockItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testRockGrabber)
testRock = World.Object(
	name = 'rock',
	description = 'An ordinary rock.',
	isVisible = True,
	kind = testRockItemComponent,
	longDescription = "This is a typical rock.  Roundish and hard.",
)

testTrashcanContainer = World.container(inventory=[], respawnContents=False)
testTrashcan = World.Object(
	name = 'trash can',
	description = 'A metal trash can, in poor condition.',
	isVisible = True,
	kind = testTrashcanContainer,
	longDescription = 'This trash can is probably as old as you are.  It is suprisingly rust-free, however.'
)

