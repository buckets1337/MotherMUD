# mobInit.py
# initializes the mobs in the world, and handles saving and loading the mobs in the world to and from file


import os

import Globals
import Engine, World
import aiMove, aiBattle


mobsFromFile = Globals.mobsFromFile
fileList = []

for region in Globals.RegionsList:
	directoryFiles = os.listdir('blueprints/mob/'+str(region)+'/')
	for obj in directoryFiles:
		path = str(region)+'/'+ obj
		fileList.append(path)


def loadMobs():
	'''
	handles loading all the mob prototypes into the world from files.
	'''
	for file in fileList:
		loadMobFromFile(file)

	for region in Globals.regionListDict:
		for room in Globals.regionListDict[region]:
			for obj in Globals.regionListDict[region][room].objects:
				if obj.mobSpawner is not None:
					for Amob in Globals.mobsFromFile:
						if Amob.name == obj.mobSpawner.mob:
							obj.mobSpawner.mob = Amob


def loadSavedMobs():
	for region in Globals.regionListDict:
		for room in Globals.regionListDict[region]:
			path = 'data/world/'+region+'/mobs/'+room+'/'
			if os.path.exists(path):
				# print path + " exists."
				# print Globals.regionListDict[region][room].mobs
				for mob in Globals.regionListDict[region][room].mobs:
					Globals.MoveTIMERS.remove(mob.aiMove.Timer)
				Globals.regionListDict[region][room].mobs = []
				# print Globals.regionListDict[region][room].mobs
				# print Globals.masterRooms
				#Globals.masterRooms[(region+room.capitalize())].mobs = []
				# Globals.masterRooms = {}
				mobFiles = os.listdir(path)
				for mob in mobFiles:
					# filePath = region + '/' + str(mob)
					if mob != '':
						if mob.endswith('~'):
							pass
						else:
							newMob = loadSavedMobFromFile(mob, path)

							# protoMob = newMob
							# inventoryList = []
							# for item in protoMob.kind.inventory:
							# 	found = False
							# 	for obj in Globals.fromFileList:
							# 		if item.name == obj.name and found == False:
							# 			# inventoryList.append(obj)	# not the right way to handle this, should be forming new objects 
							# 			invObj = Engine.cmdSpawnObject(obj.name, Globals.regionListDict[region][room], alert=False, whereFrom='mobinv')
							# 			inventoryList.append(invObj)
							# 			Globals.regionListDict[region][room].objects.remove(invObj)
							# 			found = True
							# newMortal = World.mortal(protoMob.kind.hp, protoMob.kind.exp, inventoryList, protoMob.kind.inventorySize, protoMob.kind.equipment)

							# newMob = World.Mob(protoMob.description, Globals.regionListDict[region][room], protoMob.name, Globals.regionListDict[region][room].region, protoMob.longDescription, protoMob.speech, newMortal, protoMob.species, None)
							# newMoveAI = aiMove.movementAI(newMob, protoMob.aiMove.Timer.time)
							# if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.basicRandom:
							# 	newMoveAI.Timer.actionFunction = newMoveAI.basicRandom
							# elif protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.introvertRandom:
							# 	newMoveAI.Timer.actionFunction = newMoveAI.introvertRandom
							# elif protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.extrovertRandom:
							# 	newMoveAI.Timer.actionFunction = newMoveAI.extrovertRandom
							# elif protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.donotMove:
							# 	newMoveAI.Timer.actionFunction = newMoveAI.doNotMove

							# newMob.aiMove = newMoveAI
							# Globals.MoveTIMERS.remove(newMob.aiMove.Timer)

							# if hasattr(protoMob, 'expirator') and protoMob.expirator != None:
							# 	newExpirator = World.expirator(newMob, protoMob.expirator.startingTime)
							# 	newMob.expirator = newExpirator

							# Globals.regionListDict[region][room].mobs.append(newMob)
							# print Globals.regionListDict[region][room].mobs

							#Globals.mobsFromFile.remove(protoMob)

							#Globals.MoveTIMERS.remove(protoMob.aiMove.Timer)


def loadMobFromFile(file):
	'''
	handles loading a single mob from a given mob definition file into the world
	'''
	print file

	if str(file).endswith('~'):
		print '\n'
		return

	path = 'blueprints/mob/' + file
	with open(path, 'r') as f:
		fileData = f.readlines()



	newMob = World.Mob('none', 'none', 'none')
	newMob.mobID = ''

	print fileData

	splitFile = file.split("/")
	mobID = None
	name = 'none'
	species = None
	currentRoom = None
	region = None
	description = ''
	longDescription = ''
	hp = 0
	exp = 0
	inventory = []
	inventorySize = 0
	equipment = {}
	kind = None
	expirator = None
	inventoryItems = []
	currentRoomString = ''
	moveAI = None
	battleAI = None

	newMob.kind = World.mortal(hp=0,maxHp=0,pp=0,maxPp=0,level=0,exp=0,money=0,offense=0,defense=0,speed=0,guts=0,luck=0,vitality=0,IQ=0,inventory=[],inventorySize=0,equipment={})
	newMob.region = splitFile[0]

	for Data in fileData:

		if Data.startswith('mobID='):
			IDstring = Data[6:-1]
			if IDstring != '':
				newMob.mobID = int(IDstring)
		if Data.startswith('name='):
			newMob.name = Data[5:-1]
		if Data.startswith('species='):
			newMob.species = Data[8:-1]

		if Data.startswith('currentRoom='):
			currentRoomString = Data[12:-1]

		if Data.startswith('description='):
			newMob.description = Data[12:-1]

		if Data.startswith('longDescription='):
			newMob.longDescription = Data[16:-1]

		if Data.startswith('speech='):
			newMob.speech = Data[7:-1]

		if Data.startswith('expirator='):
			expirator = Data[10:-1]
			if expirator != '':
				expirator = int(expirator)
		if Data.startswith('moveAI='):
			text = Data[7:-1]
			moveAI = text.split(":")
		if Data.startswith('battleAI='):
			text = Data[9:-1]
			if text == 'basicBash':
				battleAI = aiBattle.basicBash
			else:
				battleAI = ''

		if Data.startswith('kind.hp='):
			newMob.kind.hp = int(Data[8:-1])
		if Data.startswith('kind.maxHp='):
			newMob.kind.maxHp = int(Data[11:-1])
		if Data.startswith('kind.pp='):
			newMob.kind.pp = int(Data[8:-1])
		if Data.startswith('kind.maxPp='):
			newMob.kind.maxPp = int(Data[11:-1])
		if Data.startswith('kind.level='):
			newMob.kind.level = int(Data[11:-1])
		if Data.startswith('kind.exp='):
			newMob.kind.exp = int(Data[9:-1])
		if Data.startswith('kind.money='):
			newMob.kind.money = int(Data[11:-1])
		if Data.startswith('kind.offense='):
			newMob.kind.offense = int(Data[13:-1])
		if Data.startswith('kind.defense='):
			newMob.kind.defense = int(Data[13:-1])
		if Data.startswith('kind.speed='):
			newMob.kind.speed = int(Data[11:-1])
		if Data.startswith('kind.guts='):
			newMob.kind.guts = int(Data[10:-1])
		if Data.startswith('kind.luck='):
			newMob.kind.luck = int(Data[10:-1])
		if Data.startswith('kind.vitality='):
			newMob.kind.vitality = int(Data[14:-1])
		if Data.startswith('kind.IQ='):
			newMob.kind.IQ = int(Data[8:-1])
		if Data.startswith('kind.inventory='):
			invString = Data[15:-1]
			if invString != '':
				#print "invString:" + invString
				invList = invString.split(', ')
				#print 'invList:' + str(invList)
				for item in invList:
					for ob in Globals.fromFileList:
						if item == ob.name:
							inventoryItems.append(item)
			else:
				inventoryItems = []
		if Data.startswith('kind.inventorySize='):
			newMob.kind.inventorySize = int(Data[19:-1])


	if currentRoomString != '':
		currentRoomCoords = currentRoomString.split(":")
		newMob.currentRoom = Globals.regionListDict[currentRoomCoords[0]][currentRoomCoords[1]]
	else:
		# newMob.currentRoom = Globals.regionListDict[newMob.region]['bullpen']
		newMob.currentRoom = None

	if expirator != None and expirator != '':
		expiratorComponent = World.expirator(newMob, expirator)
		newMob.expirator = expiratorComponent

	if moveAI != None and moveAI != []:
		newMoveAI = aiMove.movementAI(newMob, int(moveAI[1]))
		if moveAI[0] == 'basicRandom':
			newMoveAI.Timer.actionFunction = newMoveAI.basicRandom
		elif moveAI[0] == 'introvertRandom':
			newMoveAI.Timer.actionFunction = newMoveAI.introvertRandom
		elif moveAI[0] == 'extrovertRandom':
			newMoveAI.Timer.actionFunction = newMoveAI.extrovertRandom
		elif moveAI[0] == 'doNotMove':
			newMoveAI.Timer.actionFunction = newMoveAI.doNotMove

		newMob.aiMove = newMoveAI
		Globals.MoveTIMERS.remove(newMob.aiMove.Timer)

	if battleAI != None:
		newMob.aiBattle = battleAI

	#print 'invItems:' + str(inventoryItems)
	for item in inventoryItems:
		#print 'invitem:' + str(item)
		removed = False
		newItem = Engine.cmdSpawnObject(item, newMob.currentRoom, alert=False, whereFrom='mobinv')
		newMob.kind.inventory.append(newItem)
		# for obj in newMob.currentRoom.objects:
		# 	if obj.name == item:
		# 		newMob.currentRoom.objects.remove(obj)
		if newMob.currentRoom is not None:
			newMob.currentRoom.objects.remove(newItem)

	if newMob.currentRoom is not None:
		newMob.currentRoom.mobs.append(newMob)

	if expirator != None and expirator != '':
		Globals.TIMERS.remove(newMob.expirator.Timer)
		#newMob.expirator.Timer = None

	Globals.mobsFromFile.append(newMob)


	#print 'region:' + str(newMob.region)


def loadSavedMobFromFile(file, path, isBattle=False):
	'''
	handles loading a single mob from a given mob definition file into the world
	'''
	print file

	if str(file).endswith('~'):
		print '\n'
		return

	# path = 'blueprints/mob/' + file
	filePath = path + file
	with open(filePath, 'r') as f:
		fileData = f.readlines()



	newMob = World.Mob('none', 'none', 'none')
	newMob.mobID=''

	print fileData

	splitFile = file.split("/")
	mobID = None
	name = 'none'
	species = None
	currentRoom = None
	region = None
	description = ''
	longDescription = ''
	hp = 0
	exp = 0
	inventory = []
	inventorySize = 0
	equipment = {}
	kind = None
	expirator = None
	inventoryItems = []
	currentRoomString = ''
	moveAI = None
	battleAI = None

	newMob.kind = World.mortal(hp=0,maxHp=0,pp=0,maxPp=0,level=0,exp=0,money=0,offense=0,defense=0,speed=0,guts=0,luck=0,vitality=0,IQ=0,inventory=[],inventorySize=0,equipment={})
	newMob.region = splitFile[0]

	for Data in fileData:

		if Data.startswith('mobID='):
			IDstring = Data[6:-1]
			if IDstring != '':
				newMob.mobID = str(IDstring)
		if Data.startswith('name='):
			newMob.name = Data[5:-1]
		if Data.startswith('species='):
			newMob.species = Data[8:-1]
		if Data.startswith('currentRoom='):
			currentRoomString = Data[12:-1]
		if Data.startswith('description='):
			newMob.description = Data[12:-1]
		if Data.startswith('longDescription='):
			newMob.longDescription = Data[16:-1]
		if Data.startswith('speech='):
			newMob.speech = Data[7:-1]
		if Data.startswith('expirator='):
			expirator = Data[10:-1]
			if expirator != '':
				expirator = int(expirator)
		if Data.startswith('moveAI='):
			text = Data[7:-1]
			moveAI = text.split(":")
		if Data.startswith('battleAI='):
			text = Data[9:-1]
			if text == 'basicBash':
				battleAI = aiBattle.basicBash
			else:
				battleAI = ''

		if Data.startswith('kind.hp='):
			newMob.kind.hp = int(Data[8:-1])
		if Data.startswith('kind.maxHp='):
			newMob.kind.maxHp = int(Data[11:-1])
		if Data.startswith('kind.pp='):
			newMob.kind.pp = int(Data[8:-1])
		if Data.startswith('kind.maxPp='):
			newMob.kind.maxPp = int(Data[11:-1])
		if Data.startswith('kind.level='):
			newMob.kind.level = int(Data[11:-1])
		if Data.startswith('kind.exp='):
			newMob.kind.exp = int(Data[9:-1])
		if Data.startswith('kind.money='):
			newMob.kind.money = int(Data[11:-1])
		if Data.startswith('kind.offense='):
			newMob.kind.offense = int(Data[13:-1])
		if Data.startswith('kind.defense='):
			newMob.kind.defense = int(Data[13:-1])
		if Data.startswith('kind.speed='):
			newMob.kind.speed = int(Data[11:-1])
		if Data.startswith('kind.guts='):
			newMob.kind.guts = int(Data[10:-1])
		if Data.startswith('kind.luck='):
			newMob.kind.luck = int(Data[10:-1])
		if Data.startswith('kind.vitality='):
			newMob.kind.vitality = int(Data[14:-1])
		if Data.startswith('kind.IQ='):
			newMob.kind.IQ = int(Data[8:-1])
		if Data.startswith('kind.inventory='):
			invString = Data[15:-1]
			if invString != '':
				#print "invString:" + invString
				invList = invString.split(', ')
				#print 'invList:' + str(invList)
				for item in invList:
					for ob in Globals.fromFileList:
						if item == ob.name:
							inventoryItems.append(item)
		if Data.startswith('kind.inventorySize='):
			newMob.kind.inventorySize = int(Data[19:-1])


	if currentRoomString != '':
		if isBattle == False:
			currentRoomCoords = currentRoomString.split(":")
			newMob.currentRoom = Globals.regionListDict[currentRoomCoords[0]][currentRoomCoords[1]]
		else:
			currentRoomCoords = currentRoomString.split(":")
			newMob.currentRoom = Globals.regionListDict['battles'][currentRoomCoords[1]]
	else:
		newMob.currentRoom = Globals.regionListDict[newMob.region]['bullpen']

	if expirator != None and expirator != '':
		expiratorComponent = World.expirator(newMob, expirator)
		newMob.expirator = expiratorComponent
		#newMob.expirator.Timer.attachedTo = newMob.expirator

	if moveAI != None and moveAI != []:
		newMoveAI = aiMove.movementAI(newMob, int(moveAI[1]))
		if moveAI[0] == 'basicRandom':
			newMoveAI.Timer.actionFunction = newMoveAI.basicRandom
		elif moveAI[0] == 'introvertRandom':
			newMoveAI.Timer.actionFunction = newMoveAI.introvertRandom
		elif moveAI[0] == 'extrovertRandom':
			newMoveAI.Timer.actionFunction = newMoveAI.extrovertRandom
		elif moveAI[0] == 'doNotMove':
			newMoveAI.Timer.actionFunction = newMoveAI.doNotMove

		newMob.aiMove = newMoveAI
		#Globals.MoveTIMERS.remove(newMob.aiMove.Timer)
	if battleAI != None:
		newMob.aiBattle = battleAI

	for item in inventoryItems:
		#print item
		removed = False
		newItem = Engine.cmdSpawnObject(item, newMob.currentRoom, alert=False, whereFrom='mobinv')
		newMob.kind.inventory.append(newItem)
		for obj in newMob.currentRoom.objects:
			if obj.name == item:
				newMob.currentRoom.objects.remove(obj)

	if isBattle == True:
		if newMob.expirator.Timer in Globals.TIMERS:
			Globals.TIMERS.remove(newMob.expirator.Timer)
		if newMob.aiMove.Timer in Globals.MoveTIMERS:
			Globals.MoveTIMERS.remove(newMob.aiMove.Timer)

	newMob.currentRoom.mobs.append(newMob)

	# if expirator != None and expirator != '':
	# 	Globals.TIMERS.remove(newMob.expirator.Timer)
	# 	newMob.expirator.Timer = None

	#Globals.mobsFromFile.append(newMob)

	return newMob


	#print 'region:' + str(newMob.region)







def saveMobs():
	'''
	handles saving all mobs in the world into unique mob definition files when the server is shutdown
	'''
	for region in Globals.regionListDict:
		for room in Globals.regionListDict[region]:
			path='data/world/'+region+ '/mobs/' + room + '/'
			shortPath='data/world/'+region+'/mobs/'
			if not os.path.exists(shortPath):
				os.makedirs(shortPath)
			if not os.path.exists(path):
				os.makedirs(path)
				
			dirList = os.listdir(path)
			for mobFile in dirList:
				#print mobFile
				os.remove(path+mobFile)

			for mob in Globals.regionListDict[region][room].mobs:
				saveMobToFile(mob, path)


def saveMobToFile(mob, path):
	'''
	handles saving a single mob to a unique mob definition file when the server is shutdown
	'''
	filePath = path + str(mob)
	with open(filePath, 'w') as f:
		f.write('mobID=%s\n' %str(mob))
		f.write('name=%s\n' %mob.name)
		f.write('species=%s\n' %mob.species)
		f.write('currentRoom=%s\n' %(str(mob.currentRoom.region)+ ":" +str(mob.currentRoom.name)))
		f.write('\n')
		f.write('description=%s\n' %mob.description)
		f.write('\n')
		f.write('longDescription=%s\n' %mob.longDescription)
		f.write('\n')
		f.write('speech=%s\n' %mob.speech)
		f.write('\n')
		if mob.expirator != None:
			f.write('expirator=%s\n' %mob.expirator.startingTime)

		if mob.aiMove != None:
			if mob.aiMove.Timer.actionFunction == mob.aiMove.basicRandom:
				actionFunction = 'basicRandom'
			elif mob.aiMove.Timer.actionFunction == mob.aiMove.introvertRandom:
				actionFunction = 'introvertRandom'
			elif mob.aiMove.Timer.actionFunction == mob.aiMove.extrovertRandom:
				actionFunction = 'extrovertRandom'
			elif mob.aiMove.Timer.actionFunction == mob.aiMove.doNotMove:
				actionFunction = 'doNotMove'
			f.write('moveAI=%s:%s\n' %(actionFunction, mob.aiMove.Timer.time))

		if mob.aiBattle != None:
			if mob.aiBattle == aiBattle.basicBash:
				battleFunction = 'basicBash'
			f.write('battleAI=%s\n' %battleFunction)

		f.write('\n')
		f.write('kind.hp=%s\n' %str(mob.kind.hp))
		f.write('kind.maxHp=%s\n' %str(mob.kind.maxHp))
		f.write('kind.pp=%s\n' %str(mob.kind.pp))
		f.write('kind.maxPp=%s\n' %str(mob.kind.maxPp))
		f.write('kind.level=%s\n' %str(mob.kind.level))
		f.write('kind.exp=%s\n' %str(mob.kind.exp))
		f.write('kind.money=%s\n' %str(mob.kind.money))
		f.write('kind.offense=%s\n' %str(mob.kind.offense))
		f.write('kind.defense=%s\n' %str(mob.kind.defense))
		f.write('kind.speed=%s\n' %str(mob.kind.speed))
		f.write('kind.guts=%s\n' %str(mob.kind.guts))
		f.write('kind.luck=%s\n' %str(mob.kind.luck))
		f.write('kind.vitality=%s\n' %str(mob.kind.vitality))
		f.write('kind.IQ=%s\n' %str(mob.kind.IQ))
		f.write('kind.inventory=',)
		invString = ''
		for item in mob.kind.inventory:
			invString += (item.name + ', ')
		if invString.endswith(', '):
			invString = invString[:-2]
		f.write(invString)
		f.write('\n')
		f.write('kind.inventorySize=%s\n' %str(mob.kind.inventorySize))
		f.write('kind.equipment=%s\n' %str(mob.kind.equipment))


