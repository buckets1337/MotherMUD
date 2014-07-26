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
equipmentFromFile = Globals.equipmentFromFile

fileList = []
eqFileList = []
savedEqFileList = []

for region in Globals.RegionsList:
	directoryFiles = os.listdir('blueprints/obj/'+str(region)+'/')
	eqDirectoryFiles = os.listdir('blueprints/equip/'+str(region)+'/')
	if os.path.exists('data/world/' + str(region) + '/equip/'):
		savedEqFiles = os.listdir('data/world/' + str(region) + '/equip/')
	else:
		savedEqFiles = []
	for obj in directoryFiles:
		path = str(region)+'/'+obj
		fileList.append(path)
	for obj in eqDirectoryFiles:
		path = str(region)+'/'+obj
		eqFileList.append(path)
	for obj in savedEqFiles:
		path = str(region) + '/equip/' + obj
		savedEqFileList.append(path)	


def setLocation(location):
	global room
	room = location


def loadSavedEq():
	'''
	loads equipment into rooms from equipment definition files after server restart
	'''
	for region in Globals.regionListDict:
		for room in Globals.regionListDict[region]:
			path='data/world/' + region + '/equip/' + room + '/'
			#shortPath='data/world' + region + '/equip/'

			if os.path.exists(path):
				Globals.regionListDict[region][room].equipment = {}
				dirList = os.listdir(path)
				for eqFile in dirList:
					if not eqFile.endswith('~'):
						newEq = buildEquipmentFromFile(eqFile, path)
						# Globals.regionListDict[region][room].items.append(newEq)


def saveEq():
	'''
	handles saving all equipment in the world (but not player equipment) into unique equipment definition files when the server is shutdown
	'''

	for region in Globals.regionListDict:
		for room in Globals.regionListDict[region]:
			path='data/world/'+region+'/equip/'+room+'/'
			shortPath='data/world/'+region+'/equip/'
			if not os.path.exists(shortPath):
				os.makedirs(shortPath)
			if not os.path.exists(path):
				os.makedirs(path)

			dirList = os.listdir(path)
			for eqFile in dirList:
				print eqFile
				os.remove(path+eqFile)

			for eq in Globals.regionListDict[region][room].equipment:
				saveEqToFile(eq, path)


def saveEqToFile(eq, path):
	'''
	handles saving a single bit of equipment to a unique equipment definition file when the server is shutdown
	'''
	eqType = ''
	if eq.kind.equipment.weapon != None:
		eqType = 'weapon'
	elif eq.kind.equipment.armor != None:
		eqType = 'armor'

	battleCommands = []
	if eq.kind.equipment.battleCommands != [''] and eq.kind.equipment.battleCommands != []:
		for command in eq.kind.equipment.battleCommands:
			battleCommands.append(command)
	if battleCommands == []:
		battleCommands = ''

	itemGrabHandler = 'False'
	if hasattr(eq.kind, 'itemGrabHandler'):
		if eq.kind.itemGrabHandler != None:
			itemGrabHandler = 'True'

	notDroppable = 'False'
	if hasattr(eq.kind, 'itemGrabHandler') and eq.kind.itemGrabHandler != None:
		if eq.kind.itemGrabHandler.notDroppable:
			notDroppable = 'True'

	objectSpawner = 'False'
	if hasattr(eq.kind, 'objectSpawner'):
		if eq.kind.objectSpawner != None:
			objectSpawner = 'True'

	filePath = path + str(eq)
	with open(filePath, 'w') as f:
		f.write('ID=%s\n' %str(eq))
		f.write('currentRoom=%s\n' %(str(eq.currentRoom.region)+ ":" +str(eq.currentRoom.name)))
		f.write('\n')
		f.write('name=%s\n' %eq.name)
		f.write('type=%s\n' %eqType)
		f.write('slot=%s\n' %eq.kind.equipment.slot)
		f.write('\n')
		f.write('durability=%s\n' %eq.kind.equipment.durability)
		f.write('maxDurability=%s\n' %eq.kind.equipment.maxDurability)
		f.write('worth=%s\n' %eq.kind.equipment.worth)
		f.write('\n')
		f.write('description=%s\n' %eq.description)
		f.write('\n')
		f.write('longDescription=%s\n' %eq.longDescription)
		f.write('\n')
		f.write('isVisible=%s\n' %eq.isVisible)
		f.write('\n')
		f.write('hp=%s\n' %eq.kind.equipment.hp)
		f.write('pp=%s\n' %eq.kind.equipment.pp)
		f.write('offense=%s\n' %eq.kind.equipment.offense)
		f.write('defense=%s\n' %eq.kind.equipment.defense)
		f.write('speed=%s\n' %eq.kind.equipment.speed)
		f.write('guts=%s\n' %eq.kind.equipment.guts)
		f.write('luck=%s\n' %eq.kind.equipment.luck)
		f.write('vitality=%s\n' %eq.kind.equipment.vitality)
		f.write('IQ=%s\n' %eq.kind.equipment.IQ)
		f.write('\n')
		f.write('battleCommands=%s\n' %battleCommands)
		f.write('\n')
		f.write('statusEffect=%s\n' %eq.kind.equipment.statusEffect)
		f.write('\n')
		f.write('onUse=%s\n' %eq.kind.equipment.onUse)
		f.write('\n\n')
		f.write('kind.isCarryable=%s\n' %eq.kind.isCarryable)
		f.write('kind.respawns=%s\n' %eq.kind.respawns)
		f.write('\n')
		f.write('kind.itemGrabHandler=%s\n' %itemGrabHandler)
		if itemGrabHandler == 'True':
			f.write('kind.itemGrabHandler.notDroppable=%s\n' %notDroppable)
		f.write('\n')
		f.write('kind.objectSpawner=%s\n' %objectSpawner)
		if objectSpawner == 'True':
			f.write('kind.objectSpawner.time=%s\n' %eq.kind.objectSpawner.time)
			f.write('kind.objectSpawner.spawnOdds=%s\n' %eq.kind.objectSpawner.spawnOdds)
			f.write('kind.objectSpawner.container=%s\n' %eq.kind.objectSpawner.container)
			f.write('kind.objectSpawner.cycles=%s\n' %eq.kind.objectSpawner.cycles)
			f.write('kind.objectSpawner.repeat=%s\n' %eq.kind.objectSpawner.repeat)
			f.write('kind.objectSpawner.active=%s\n' %eq.kind.objectSpawner.active)


def buildObjectFromFile(file):
	'''
	creates an object by constructing it out of details in a file
	'''
	print file

	if str(file).endswith('~'):
		print "\n"
		return

	path = 'blueprints/obj/' + file
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
	mobActive = None
	mobCycles = None
	mobMode = None
	mobSpawnOdds = None
	mobTime = None
	mobFile = None
	mobSpawner = None
	onUse = None

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
				container = text[1:-1]		# this should be a reference to another object
				container = container.split(', ')
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

		if Data.startswith('kind.onUse='):
			text = Data[11:-1]
			onUse = text

		if Data.startswith('mobSpawner='):
			text = Data[11:-1]
			if text == 'True':
				mobSpawner = True
			elif text == 'False':
				mobSpawner = False
		if Data.startswith('mobSpawner.mobFile='):
			text = Data[19:-1]
			mobFile = text
		if Data.startswith('mobSpawner.time='):
			text = Data[16:-1]
			mobTime = int(text)
		if Data.startswith('mobSpawner.oddsList='):
			text = Data[20:-1]
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
			mobSpawnOdds = nestedOddsList
		if Data.startswith('mobSpawner.mode='):
			text = Data[16:-1]
			print "mobModeff:" + text
			mobMode = text
		if Data.startswith('mobSpawner.cycles='):
			text = Data[18:-1]
			mobCycles = int(text)
		if Data.startswith('mobSpawner.active='):
			text = Data[18:-1]
			if text == 'True':
				mobActive = True
			elif text == 'False':
				mobActive = False
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

	if mobSpawner:
		mobFileMod = mobFile.split("/")
		# print mobFileMod
		# print Globals.mobsFromFile
		# for mob in Globals.mobsFromFile:
		# 	if mob.name == mobFileMod[1]:
		# 		mobref = mob
		#print mobMode
		mobSpawnerComponent = World.mobSpawner(newObject, Globals.TIMERS, mobTime, mobFileMod[1], mobSpawnOdds, mobCycles, mode=mobMode, active=mobActive)
	else:
		mobSpawnerComponent = None


	#print kind
	if kind == 'item':
		# print itemGrabHandler
		# print objectSpawnerComponent
		#print isCarryable
		itemComponent.isCarryable = isCarryable
		itemComponent.respawns = respawns
		itemComponent.itemGrabHandler = itemGrabHandlerComponent
		itemComponent.objectSpawner = objectSpawnerComponent
		itemComponent.onUse = onUse
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

	if mobSpawner:
		newObject.mobSpawner = mobSpawnerComponent
	else:
		newObject.mobSpawner = None

	#print newObject.kind
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
			print "kind.onUse:" + str(newObject.kind.onUse)
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
	print "mobSpawner:" + str(newObject.mobSpawner)
	if newObject.mobSpawner is not None:
		#print "mobSpawner.mobFile:" + str(newObject.mobSpawner.mobFile)
		print "mobSpawner.time:" + str(newObject.mobSpawner.time)
		print "mobSpawner.oddsList:" + str(newObject.mobSpawner.oddsList)
		print "mobSpawner.mode:" + str(newObject.mobSpawner.mode)
		print "mobSpawner.cycles:" + str(newObject.mobSpawner.cycles)
		print "mobSpawner.active:" + str(newObject.mobSpawner.active)
	print "\n"


def buildEquipmentFromFile(file, location):

	print file

	if str(file).endswith('~'):
		print "\n"
		return

	path = location + file
	with open(path, 'r') as f:
		fileData = f.readlines()


	newWeapon = None
	newArmor = None
	equipmentType = None
	slot = None
	durability = None
	maxDurability = None
	worth = None
	description = None
	longDescription = None
	hp = None
	pp = None
	offense = None
	defense = None
	speed = None
	guts = None
	luck = None
	vitality = None
	IQ = None
	battleCommands = None
	statusEffect = None
	onUse = None
	isVisible = None
	spawnContainer = None
	isCarryable = None
	respawns = None
	itemGrabHandler = None
	objectSpawner = None
	notDroppable = None
	container = None
	spawnOdds = None
	time = None
	active = None
	repeat = None
	cycles = None


	for Data in fileData:
		if Data.startswith('type='):
			equipmentType = Data[5:-1]
		if Data.startswith('ID='):
			ID = Data[3:-1]
		if Data.startswith('name='):
			name = Data[5:-1]
		if Data.startswith('slot='):
			slot = Data[5:-1]
		if Data.startswith('durability='):
			durability = Data[11:-1]
		if Data.startswith('maxDurability='):
			maxDurability = Data[14:-1]
		if Data.startswith('worth='):
			worth = Data[6:-1]
		if Data.startswith('description='):
			description = Data[12:-1]
		if Data.startswith('longDescription='):
			longDescription = Data[16:-1]
		if Data.startswith('hp='):
			hp = int(Data[3:-1])
		if Data.startswith('pp='):
			pp = int(Data[3:-1])
		if Data.startswith('offense='):
			offense = int(Data[8:-1])
		if Data.startswith('defense='):
			defense = int(Data[8:-1])
		if Data.startswith('speed='):
			speed = int(Data[6:-1])
		if Data.startswith('guts='):
			guts = int(Data[5:-1])
		if Data.startswith('luck='):
			luck = int(Data[5:-1])
		if Data.startswith('vitality='):
			vitality = int(Data[9:-1])
		if Data.startswith('IQ='):
			IQ = int(Data[3:-1])
		if Data.startswith('battleCommands='):
			battleCommands = Data[15:-1]
			battleCommands = battleCommands.split(",")
		if Data.startswith('statusEffect='):
			statusEffect = Data[13:-1]
		if Data.startswith('onUse='):
			onUse = Data[6:-1]
		if Data.startswith('isVisible='):
			isVisible = Data[10:-1]
			if isVisible == 'True':
				isVisible = True
			elif isVisible == 'False':
				isVisible = False
		if Data.startswith('kind.isCarryable='):
			isCarryable = Data[17:-1]
			if isCarryable == "True":
				isCarryable = True
			elif isCarryable == "False":
				isCarryable = False
		if Data.startswith('kind.respawns='):
			respawns = Data[14:-1]
			if respawns == "True":
				respawns = True
			elif respawns == "False":
				respawns = False
		if Data.startswith('kind.itemGrabHandler='):
			itemGrabHandler = Data[21:-1]
			if itemGrabHandler == "True":
				itemGrabHandler = True
			elif itemGrabHandler == "False":
				itemGrabHandler = False
		if Data.startswith('kind.itemGrabHandler.notDroppable='):
			notDroppable = Data[34:-1]
			if notDroppable == "True":
				notDroppable = True
			elif notDroppable == "False":
				notDroppable = False
		if Data.startswith('kind.objectSpawner='):
			objectSpawner = Data[19:-1]
			if objectSpawner == 'True':
				objectSpawner = True
			elif objectSpawner == 'False':
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
				container = text[1:-1]		# this should be a reference to another object
				container = container.split(', ')
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


	if equipmentType == 'weapon':
		newWeapon = World.weapon()
	elif equipmentType == 'armor':
		newArmor = World.armor()

	if itemGrabHandler == True:
		newItemGrabHandler = World.itemGrabHandler(notDroppable=notDroppable)
	else:
		newItemGrabHandler = None
	if objectSpawner == True:
		newObjectSpawner = World.objectSpawner(owner=None, TIMERS=Globals.TIMERS, time=time, obj=None, oddsList=oddsList, container=container, cycles=cycles, repeat=repeat, active=active)
	else:
		newObjectSpawner = None


	newEquipment = World.equipment(owner=None, weapon=newWeapon, armor=newArmor, slot=slot, durability=durability, maxDurability=maxDurability, worth=worth, hp=hp, pp=pp, offense=offense, defense=defense, speed=speed, guts=guts, luck=luck, vitality=vitality, IQ=IQ, battleCommands=battleCommands, statusEffect=statusEffect, onUse=onUse)
	newItem = World.item(isCarryable=isCarryable, respawns=respawns, itemGrabHandler=newItemGrabHandler, objectSpawner=newObjectSpawner, equipment=newEquipment, onUse=onUse)
	if newItem.itemGrabHandler:
		newItem.itemGrabHandler.owner = newItem
	if newItem.objectSpawner:
		newItem.objectSpawner.owner = newItem
	newEquipment.owner = newItem
	newObject = World.Object(name=name, description=description, isVisible=isVisible, spawnContainer=spawnContainer, longDescription=longDescription, kind=newItem)
	if newObject.kind.objectSpawner:
		newObject.kind.objectSpawner.obj = newObject
	newObject.ID = ID
	newItem.owner = newObject


	equipmentFromFile.append(newObject)

	print "\n"
	print "name:" + str(newObject.name)
	print "description:" + str(newObject.description)
	print "currentRoom:" + str(newObject.currentRoom)
	print "isVisible:" + str(newObject.isVisible)
	print "spawnContainer:" + str(newObject.spawnContainer)
	print "longDescription:" + str(newObject.longDescription)
	print "kind:" + str(newObject.kind)
	#print "TIMERS:" + str(newObject.TIMERS)
	if newObject.kind is not None:
		print "kind.owner:" + str(newObject.kind.owner)
		print "kind.equipment:" + str(newObject.kind.equipment)
		print "kind.equipment.owner" + str(newObject.kind.equipment.owner)
		if hasattr(newObject.kind.equipment, 'weapon'):
			if newObject.kind.equipment.weapon is not None:
				print "weapon:" + str(newObject.kind.equipment.weapon)
		if hasattr(newObject.kind.equipment, 'armor'):
			if newObject.kind.equipment.armor is not None:
				print "armor:" + str(newObject.kind.equipment.armor)
		print "slot:" + str(newObject.kind.equipment.slot)
		print "durability:" + str(newObject.kind.equipment.durability)
		print "maxDurability:" + str(newObject.kind.equipment.maxDurability)
		print "worth:" + str(newObject.kind.equipment.worth)
		if newObject.kind.equipment.hp != 0:
			print "hp:" + str(newObject.kind.equipment.hp)
		if newObject.kind.equipment.pp != 0:
			print "pp:" + str(newObject.kind.equipment.pp)
		if newObject.kind.equipment.offense != 0:
			print "offense:" + str(newObject.kind.equipment.offense)
		if newObject.kind.equipment.defense != 0:
			print "defense:" + str(newObject.kind.equipment.defense)
		if newObject.kind.equipment.speed != 0:
			print "speed:" + str(newObject.kind.equipment.speed)
		if newObject.kind.equipment.guts != 0:
			print "guts:" + str(newObject.kind.equipment.guts)
		if newObject.kind.equipment.luck != 0:
			print "luck:" + str(newObject.kind.equipment.luck)
		if newObject.kind.equipment.vitality != 0:
			print "vitality:" + str(newObject.kind.equipment.vitality)
		if newObject.kind.equipment.IQ != 0:
			print "IQ:" + str(newObject.kind.equipment.IQ)
		if newObject.kind.equipment.statusEffect is not None:
			if newObject.kind.equipment.statusEffect != '':
				print "statusEffect:" + str(newObject.kind.equipment.statusEffect)
		if newObject.kind.equipment.battleCommands is not None:
			if newObject.kind.equipment.battleCommands != ['']:
				print "battleCommands:" + str(newObject.kind.equipment.battleCommands)
		if newObject.kind.equipment.onUse is not None:
			if newObject.kind.equipment.onUse != '':
				print "onUse:" + str(newObject.kind.equipment.onUse)

		if newObject.kind.itemGrabHandler is not None:
			print "kind.itemGrabHandler:" + str(newObject.kind.itemGrabHandler)
			print "kind.itemGrabHandler.notDroppable:" + str(newObject.kind.itemGrabHandler.notDroppable)
		if newObject.kind.objectSpawner is not None:
			print "kind.objectSpawner:" + str(newObject.kind.objectSpawner)
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


	return newObject

for obj in fileList:
	buildObjectFromFile(obj)

print savedEqFileList
if savedEqFileList == []:
	for obj in eqFileList:
		buildEquipmentFromFile(obj, 'blueprints/equip/')
else:
	loadSavedEq()










