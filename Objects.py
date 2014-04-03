# Objects.py
"""
This file defines the various different objects that can be found in the world
"""

#--------------------------
# This file defines the objects in the world.  Best practice for naming an object follows: <region><Room><Name>, where the region is lowercase and every other word in the smashed string is capitalized
#--------------------------

import os

import World
import Globals


indexList = []
fromFileList = Globals.fromFileList

fileList = []

for region in Globals.RegionsList:
	directoryFiles = os.listdir('obj/'+str(region)+'/')
	for obj in directoryFiles:
		path = str(region)+'/'+obj
		fileList.append(path)


def setLocation(location):
	global room
	room = location


def buildObjectFromFile(file):
	'''
	creates an object by constructing it out of details in a file
	'''
	print file

	if str(file).endswith('~'):
		print "\n"
		return

	path = 'obj/' + file
	with open(path, 'r') as f:
		fileData = f.readlines()

	newObject = World.Object('none', 'none')

	print fileData


	kind = None
	isCarryable = None
	isVisible = None
	isLocked = False
	respawns = None
	objectSpawner = None
	itemGrabHandler = None
	repeat = None
	time = None
	spawnOdds = None
	container = None
	cycles = None
	repeat = None
	active = None
	notDroppable = None
	objectSpawnerComponent = None
	itemGrabHandlerComponent = None
	itemComponent = None

	for Data in fileData:



		if Data.startswith('name='):
			newObject.name = Data[6:-2]
		if Data.startswith('description='):
			newObject.description = Data[13:-2]
		if Data.startswith('longDescription='):
			newObject.longDescription = Data[17:-2]
		if Data.startswith('isVisible='):
			text = Data[10:-1]
			if text == 'True':
				newObject.isVisible = True
			elif text == 'False':
				newObject.isVisible = False


		if Data.startswith('kind='):
			text = Data[5:-1]
			#print "kind:" + text
			if text == 'item':
				kind = 'item'
			elif text == 'container':
				kind = 'container'
		if Data.startswith('kind.isCarryable='):
			text = Data[17:-1]
			#print "isCarryable:" +text
			if text == 'True':
				isCarryable = True
			elif text == 'False':
				isCarryable = False
		if Data.startswith('kind.respawns='):
			text = Data[14:-1]
			if text == 'True':
				respawns = True
			elif text == 'False':
				respawns = False
		if Data.startswith('kind.isLocked='):
			text = Data[14:-1]
			if text == 'True':
				isLocked = True
			if text == 'False':
				isLocked = False
		if Data.startswith('kind.respawnContents='):
			text = Data[21:-1]
			if text == 'True':
				respawnContents = True
			elif text == 'False':
				respawnContents = False


		if Data.startswith('kind.objectSpawner='):
			text = Data[19:-1]
			if text == 'True':
				objectSpawner = True
			elif text == 'False':
				objectSpawner = False
		if Data.startswith('kind.objectSpawner.time='):
			time = int(Data[24:-1])
		if Data.startswith('kind.objectSpawner.spawnOdds='):
			text = Data[29:-1]
			oddsList = text.split(',')
			#print "oddsList:" + str(oddsList)
			nestedOddsList = []
			for odds in oddsList:
				nestedOddsList.append(odds.split(':'))
			for oddsEntry in nestedOddsList:
				oddsEntry[1] = int(oddsEntry[1])
				if oddsEntry[0] == 'True':
					oddsEntry[0] = True
				elif oddsEntry[0] == 'False':
					oddsEntry[0] = False
			#print nestedOddsList
			spawnOdds = nestedOddsList
		if Data.startswith('kind.objectSpawner.container='):
			text = Data[29:-1]
			if text == 'None':
				container = None
			else:
				container = text		# this should be a reference to another object
		if Data.startswith('kind.objectSpawner.cycles='):
			cycles = int(Data[26:-1])
		if Data.startswith('kind.objectSpawner.repeat='):
			text = Data[26:-1]
			if text == 'True':
				repeat = True
			elif text == 'False':
				repeat = False
		if Data.startswith('kind.objectSpawner.active='):
			
			text = Data[26:-1]
			#print "***active:" + text

			if text == 'True':
				active = True
			elif text == 'False':
				active = False


		if Data.startswith('kind.itemGrabHandler='):
			text = Data[21:-1]
			#print "itemGrabHandler:" +text
			if text == 'True':
				itemGrabHandler = True
			elif text == 'False':
				itemGrabHandler = False
		if Data.startswith('kind.itemGrabHandler.notDroppable='):
			text = Data[34:-1]
			#print "*** notDroppabletext:" + text
			if text == 'True':
				notDroppable = True
			elif text == 'False':
				notDroppable = False

	#print kind
	if kind == 'item':
		# print itemGrabHandler
		# print objectSpawnerComponent
		# print isCarryable
		itemComponent = World.item()
		itemComponent.owner = newObject
	if kind == 'container':
		itemComponent = World.container(inventory=[])
		itemComponent.owner = newObject

	if objectSpawner:
		objectSpawnerComponent = World.objectSpawner(itemComponent, Globals.TIMERS, time, newObject, spawnOdds, container, cycles, repeat, active)
	else:
		objectSpawnerComponent = None

	if itemGrabHandler:
		itemGrabHandlerComponent = World.itemGrabHandler(notDroppable)
	else:
		itemGrabHandlerComponent = None


	#print kind
	if kind == 'item':
		# print itemGrabHandler
		# print objectSpawnerComponent
		#print isCarryable
		itemComponent.isCarryable = isCarryable
		itemComponent.respawns = respawns
		itemComponent.itemGrabHandler = itemGrabHandlerComponent
		itemComponent.objectSpawner = objectSpawnerComponent
		#itemComponent = World.item(isCarryable, respawns, itemGrabHandlerComponent, objectSpawnerComponent)
	if kind == 'container':
		itemComponent.isLocked = isLocked
		itemComponent.isCarryable = isCarryable
		itemComponent.respawns = respawns
		itemComponent.respawnContents = respawnContents
		itemComponent.itemGrabHandler = itemGrabHandlerComponent
		itemComponent.objectSpawner = objectSpawnerComponent
		itemComponent.inventory = []
		#itemComponent = World.container(isLocked, isCarryable, respawns, respawnContents, itemGrabHandlerComponent, objectSpawnerComponent)

	#print newObject.name

	if kind is not None:
		newObject.kind = itemComponent
	fromFileList.append(newObject)

	# printing suite
	print "name:" + str(newObject.name)
	print "description:" + str(newObject.description)
	print "currentRoom:" + str(newObject.currentRoom)
	print "isVisible:" + str(newObject.isVisible)
	print "spawnContainer:" + str(newObject.spawnContainer)
	print "longDescription:" + str(newObject.longDescription)
	print "kind:" + str(newObject.kind)
	print "TIMERS:" + str(newObject.TIMERS)
	if newObject.kind is not None:
		if isinstance(newObject.kind, World.item):
			print "kind.isCarryable:" + str(newObject.kind.isCarryable)
			print "kind.respawns:" + str(newObject.kind.respawns)
			print "kind.itemGrabHandler:" + str(newObject.kind.itemGrabHandler)
			print "kind.objectSpawner:" + str(newObject.kind.objectSpawner)
		if isinstance(newObject.kind, World.container):
			print "kind.inventory:" + str(newObject.kind.inventory)
			print "kind.isLocked:" + str(newObject.kind.isLocked)
			print "kind.isCarryable:" + str(newObject.kind.isCarryable)
			print "kind.respawns:" + str(newObject.kind.respawns)
			print "kind.respawnContents:" + str(newObject.kind.respawnContents)
			print "kind.itemGrabHandler:" + str(newObject.kind.itemGrabHandler)
			print "kind.objectSpawner:" + str(newObject.kind.objectSpawner)
		if newObject.kind.itemGrabHandler is not None:
			print "kind.itemGrabHandler.notDroppable:" + str(newObject.kind.itemGrabHandler.notDroppable)
		if newObject.kind.objectSpawner is not None:
			print "kind.objectSpawner.owner:" + str(newObject.kind.objectSpawner.owner)
			print "kind.objectSpawner.TIMERS:" + str(newObject.kind.objectSpawner.TIMERS)
			print "kind.objectSpawner.time:" + str(newObject.kind.objectSpawner.time)
			print "kind.objectSpawner.obj:" + str(newObject.kind.objectSpawner.obj)
			print "kind.objectSpawner.oddsList:" + str(newObject.kind.objectSpawner.oddsList)
			print "kind.objectSpawner.container:" + str(newObject.kind.objectSpawner.container)
			print "kind.objectSpanwer.cycles:" + str(newObject.kind.objectSpawner.cycles)
			print "kind.objectSpawner.repeat:" + str(newObject.kind.objectSpawner.repeat)
			print "kind.objectSpawner.active:" + str(newObject.kind.objectSpawner.active)
			print "kind.objectSpawner.timer:" + str(newObject.kind.objectSpawner.timer)
			print "kind.objectSpawner.startingLocation:" + str(newObject.kind.objectSpawner.startingLocation)
	print "\n"


for obj in fileList:
	buildObjectFromFile(obj)


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
indexList.append(testLobbyPottedPlant)

testLobbyDesk = World.Object(
	name = 'desk',
	description = 'A cheap plywood desk.',
	isVisible = True,
	longDescription = "This desk looks like it was flimsy even when it was new.  It has a single desk drawer which does not appear to be locked."
)
indexList.append(testLobbyDesk)

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
indexList.append(testLobbyKey)

testDeskContainer = World.container(inventory=[testLobbyKey], respawnContents=True)
testLobbyDeskDrawer = World.Object(
	name = 'desk_drawer',
	description = 'An unlocked desk drawer.',
	isVisible = False,
	longDescription = "This is an ordinary desk drawer.  It has a lock on it, but it does not appear to be engaged.",
	kind = testDeskContainer
)
indexList.append(testLobbyDeskDrawer)

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
indexList.append(testLobbyFiles)

testFileCabinetContainer = World.container(isLocked = True, inventory=[testLobbyFiles], respawnContents=True)
testLobbyFileCabinet = World.Object(
	name = 'file_cabinet',
	description = 'A grey steel file cabinet.',
	isVisible = True,
	longDescription = "This is a file cabinet.   There are many like it, but this one is here.",
	kind = testFileCabinetContainer
)
indexList.append(testLobbyFileCabinet)
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
indexList.append(testTrashcan)

#@ things that spawn in the restroom
testTrashGrabber = World.itemGrabHandler()
testTrashItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testTrashGrabber)
testTrash = World.Object(
	name = 'trash_pile',
	description = "A pile of trash",
	isVisible = True,
	kind = testTrashItemComponent,
	longDescription = "Your typical trash heap.  Trash seems to pile up if no one takes it out.",
	spawnContainer = testTrashcan.kind

)
indexList.append(testTrash)
testTrashSpawnOdds = [[True, 1],[False, 20]]		# a true/false odds listing, if True object spawns.  This one is high freq low odds for regular item creation
testTrashSpawner = World.objectSpawner(testTrashItemComponent, Globals.TIMERS, (6), testTrash, testTrashSpawnOdds, cycles=1, repeat=True, active=True)		# spawners and their odds have to go after the item definition because they reference it
testTrash.kind.objectSpawner = testTrashSpawner



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
indexList.append(testRock)

testGardenGnomeGrabber = World.itemGrabHandler()
testGardenGnomeItemComponent = World.item(isCarryable=True, respawns=True, itemGrabHandler=testGardenGnomeGrabber)
testGardenGnome = World.Object(
	name = 'garden_gnome',
	description = "A beat-up garden gnome.",
	isVisible = True,
	kind = testGardenGnomeItemComponent,
	longDescription = "This garden gnome is all scratched and worn, as if it had been traveling."

)
indexList.append(testGardenGnome)
testGardenGnomeSpawnOdds = [[True, 1],[False, 10]]		# a true/false odds listing, if True object spawns.  This one is high freq low odds for regular item creation
testGardenGnomeSpawner = World.objectSpawner(testGardenGnomeItemComponent, Globals.TIMERS, (6), testGardenGnome, testGardenGnomeSpawnOdds, cycles=3, repeat=True, active=True)		# spawners and their odds have to go after the item definition because they reference it
testGardenGnome.kind.objectSpawner = testGardenGnomeSpawner
# print "spwn " + str(testGardenGnome.kind.objectSpawner)
# print "obstrm " + str(testGardenGnome.kind.objectSpawner.startingLocation)


