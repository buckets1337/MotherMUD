# Objects.py
"""
This file defines the various different objects that can be found in the world
"""

#--------------------------
# This file defines the objects in the world.  Best practice for naming an object follows: <region><Room><Name>, where the region is lowercase and every other word in the smashed string is capitalized
#--------------------------


import World
import Globals



def setLocation(location):
	global room
	room = location




######################
# test region objects
######################

## Room: Lobby

testLobbyPottedPlant = World.Object(
	name = 'potted_plant',
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

#~~~~~~~~~~~~~~  <-This signifies these items are related to each other somehow.  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
testKeyGrabber = World.itemGrabHandler(notDroppable=True)		
testKeyItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testKeyGrabber)
testLobbyKey =  World.Object(
	name = 'rusty_key',
	description = 'An old rusty key.',
	isVisible = False,
	kind = testKeyItemComponent,
	longDescription = "This key appears to be old.  It has to go to something around here, since it was in the desk.",
)

testDeskContainer = World.container(inventory=[testLobbyKey], respawnContents=True)
testLobbyDeskDrawer = World.Object(
	name = 'desk_drawer',
	description = 'An unlocked desk drawer.',
	isVisible = False,
	longDescription = "This is an ordinary desk drawer.  It has a lock on it, but it does not appear to be engaged.",
	kind = testDeskContainer
)

# places the key in the desk drawer
testLobbyKey.spawnContainer = testLobbyDeskDrawer
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

testFilesGrabber = World.itemGrabHandler()		
testFilesItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testFilesGrabber)

testLobbyFiles =  World.Object(
	name = 'files',
	description = 'Random files.',
	isVisible = False,
	kind = testFilesItemComponent,
	longDescription = "A random assortment of files",
)

testFileCabinetContainer = World.container(isLocked = True, inventory=[testLobbyFiles], respawnContents=True)
testLobbyFileCabinet = World.Object(
	name = 'file_cabinet',
	description = 'A grey steel file cabinet.',
	isVisible = True,
	longDescription = "This is a file cabinet.   There are many like it, but this one is here.",
	kind = testFileCabinetContainer
)
# place the files in the file cabinet
testLobbyFiles.spawnContainer = testLobbyFileCabinet
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




## Room: restroom

testTrashcanContainer = World.container(inventory=[], respawnContents=False)
testTrashcan = World.Object(
	name = 'trash_can',
	description = 'A metal trash can, in poor condition.',
	isVisible = True,
	kind = testTrashcanContainer,
	longDescription = "This trash can is probably as old as you are.  It is suprisingly rust-free, however.  Unfortunately, this doesn't seem to be the type of trashcan that holds good things."
)




## Room: outside

testRockGrabber = World.itemGrabHandler()
testRockItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testRockGrabber)
testRock = World.Object(
	name = 'rock',
	description = 'An ordinary rock.',
	isVisible = True,
	kind = testRockItemComponent,
	longDescription = "This is a typical rock.  Roundish and hard.",
)

testGardenGnomeGrabber = World.itemGrabHandler()
testGardenGnomeItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testGardenGnomeGrabber)
testGardenGnome = World.Object(
	name = 'garden_gnome',
	description = "A beat-up garden gnome.",
	isVisible = True,
	kind = testGardenGnomeItemComponent,
	longDescription = "This garden gnome is all scratched and worn, as if it had been traveling."

)
testGardenGnomeSpawnOdds = [[True, 1],[False, 10]]		# a true/false odds listing, if True object spawns.  This one is high freq low odds for regular item creation
testGardenGnomeSpawner = World.objectSpawner(testGardenGnomeItemComponent, Globals.TIMERS, (6), testGardenGnome, testGardenGnomeSpawnOdds, cycles=3, repeat=True)		# spawners and their odds have to go after the item definition because they reference it
testGardenGnome.kind.objectSpawner = testGardenGnomeSpawner
# print "spwn " + str(testGardenGnome.kind.objectSpawner)
# print "obstrm " + str(testGardenGnome.kind.objectSpawner.startingLocation)


