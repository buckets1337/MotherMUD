# RoomInit.py
# handles loading in all the rooms in all the regions in the world.

import Globals, Engine, Rooms, World, aiMove, MobInit
import os


masterRooms = Globals.masterRooms
regionListDict = Globals.regionListDict
fileData = []

def saveAllRooms():
	'''
	saves each room in the server's memory to a room definition text file
	'''
	for region in Globals.regionListDict:
		# pathRoot= 'data/world/'
		# if not os.path.exists(pathRoot):
		# 	os.makedirs(pathRoom)
		path= 'data/world/'+ region + '/'
		if not os.path.exists(path):
			os.makedirs(path)
		#print 'region:' + str(region)
		for room in Globals.regionListDict[region]:
			#print 'room:' + str(Globals.regionListDict[region][room])
			saveRoom(Globals.regionListDict[region][room])


def saveRoom(room):
	'''
	saves the room and it's contents to a room definition file
	'''
	#print room
	region = room.region
	path = 'data/world/'+region+'/'+room.name


	with open(path, 'w') as f:
		f.write('name=%s\n' %room.name)
		f.write('region=%s' %room.region)
		f.write('\n\n')
		f.write("description='%s'" %room.description)
		f.write('\n\n')
		f.write("longDescription='%s'" %room.longDescription)
		f.write('\n\n')
		f.write('exits=',)
		fileString = ''
		for exit in room.exits:
			exitRegion = room.exits[exit].region
			exitRoom = room.exits[exit].name
			fileString = fileString + (exitRegion+':'+exitRoom+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')
		f.write('actives=',)
		fileString = ''
		for obj in room.objects:
			if hasattr(obj.kind,'objectSpawner'):
				if hasattr(obj.kind.objectSpawner, 'active'):
					if obj.kind.objectSpawner.active:
						fileString = fileString + (obj.name+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')				
		f.write('objects=',)
		fileString = ''
		for obj in room.objects:
			#print obj
			info = dir(obj)
			#print info
			fileString = fileString + (obj.name+', ')
			if hasattr(obj.kind,'inventory'):
				#print 'inv:' + str(obj.kind.inventory)
				for ob in obj.kind.inventory:
					fileString = fileString + (ob.name+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')
		f.write('spawnPoints=',)
		for obj in room.objects:
			fileString = ''
			if hasattr(obj, 'kind') and hasattr(obj.kind, 'objectSpawner') and obj.kind is not None and obj.kind.objectSpawner is not None:
				if obj.kind.objectSpawner.startingLocation[0].name != room.name:
					fileString = fileString + (obj.name +':'+obj.currentRoom.region+'-'+obj.kind.objectSpawner.startingLocation[0].name + ', ')
				if fileString.endswith(', '):
					fileString = fileString[:-2]
				f.write(fileString)
		f.write('\n\n')
		f.write('spawnContainers=',)
		for obj in room.objects:
			fileString = ''

			if obj.spawnContainer != None:
				fileString = fileString + (obj.name +':'+obj.currentRoom.region+'-'+obj.kind.objectSpawner.startingLocation[0].name + '-'+ str(obj.spawnContainer.name)+', ')
			if fileString.endswith(', '):
				fileString = fileString[:-2]
			f.write(fileString)
		f.write('\n\n')
		f.write('stuffList=',)
		fileString = ''
		for obj in room.objects:
			if hasattr(obj, 'kind'):
				#print "^^^stuffkind"
				if hasattr(obj.kind, 'inventory'):
					#print "^^^stuffinv"
					if obj.kind.inventory != []:
						#print "^^^stuffobjinv" + str(obj.kind.inventory)
						for ob in obj.kind.inventory:
							fileString = fileString + (ob.name+':'+obj.name+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')
		f.write('mobs=',)
		mobString=''
		for mob in room.mobs:
			mobString += (mob.name + ', ')
		if mobString.endswith(', '):
			mobString = mobString[:-2]+'\n'
		f.write(mobString)
		f.write('\n')
		f.write('equipment=',)
		eqString=''
		for eq in room.equipment:
			eqString += (eq.name + ', ')
		if eqString.endswith(', '):
			eqString = eqString[:-2]+'\n'
		f.write(eqString)
		f.write('\n')






def loadBattleRoom(file):
	'''
	loads the contents of one room definition file into the world, and initializes the room with all required items and exits
	'''

	if str(file).endswith('~'):
		return

	fileList = []

	print file

	path = 'blueprints/world/' + file
	if os.path.exists('data/world/' + file):
		path = 'data/world/' + file
	with open(path, 'r') as f:
		fileData = f.readlines()

	print fileData

	if 'battles' not in Globals.regionListDict:
		Globals.regionListDict['battles'] = {}

	# name = None
	# region = None
	# description = None
	# longDescription = None
	# exits = {}
	# objects = []
	fileDetails = file.split("/")
	newRoom = World.Room()

	newRoom.players = []
	newRoom.mobs = []

	item = ''
	destRegion = ''
	destRoom = ''
	destContainer = ''
	hasSpawnContainers = False
	activesList = []
	mobs = []

	for Data in fileData:


		if Data.startswith('name='):
			newRoom.name = Data[5:-1]
			#print "name-" + newRoom.name

		if Data.startswith('region='):
			newRoom.region = Data[7:-1]

		if Data.startswith('description='):
			newRoom.description = Data[13:-2]

		if Data.startswith('longDescription='):
			newRoom.longDescription = Data[17:-2]

		if Data.startswith('exits='):
			#print Data
			exitsDict = {}
			exitsList = (Data[6:-1]).split(', ')
			#print exitsList
			if newRoom.region in Globals.regionListDict:
				regionRooms = Globals.regionListDict[newRoom.region]
			for exit in exitsList:
				if exit != '':
					exitDetails = (exit).split(':')
					#print exitDetails
					exitsDict[exitDetails[1]] = Globals.regionListDict[exitDetails[0]][exitDetails[1]]
			newRoom.exits = exitsDict

		if Data.startswith('actives='):
			activesList = Data[8:-1]
			activesList = activesList.split(", ")
			print 'actives:' + str(activesList)

		if Data.startswith('objects='):
			#print Data
			objectList = Data[8:-1]
			objectList = objectList.split(", ")
			print 'objectList:' + str(objectList)
			spawnList = []
			#print "ffl:"+str(Globals.fromFileList)
			for obj in objectList:
				#print obj
				for ob in Globals.fromFileList:
					if ob.name == obj:
						print '!!!name:' + str(ob.name)
						if hasattr(ob, 'kind'):
							#print '!!!kind'
							if hasattr(ob.kind, 'objectSpawner'):
								#print '!!!objSpwn'
								act = False
								#print '###actives:' + str(activesList)
								for spawner in activesList:
									# print 'spn:' + spawner
									# print 'ob:' + ob.name
									if str(ob.name) == str(spawner):
										act = True
										activesList.remove(spawner)
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=act, whereFrom='file')
								if act == False and hasattr(newObject, 'kind') and hasattr(newObject.kind,'objectSpawner') and hasattr(newObject.kind.objectSpawner,'timer'):
									Globals.TIMERS.remove(newObject.kind.objectSpawner.timer)
								spawnList.append(newObject)
							else:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
								spawnList.append(newObject)
						else:
							if hasattr(ob, 'mobSpawner'):
								print str(ob.mobSpawner.mode)
							newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
							spawnList.append(newObject)

			newRoom.objects = spawnList
			Rooms.setCurrentRoom(newRoom.objects, newRoom)
			#print newRoom.name
			for obj in newRoom.objects:
				print str((obj.name, obj.currentRoom.name))

		if Data.startswith('spawnPoints='):
			pointsList = Data[12:-1]
			pointsList = pointsList.split(", ")
			for point in pointsList:
				pointDetails = point.split(":")
				for obj in newRoom.objects:
					if obj.name == pointDetails[0]:
						coord = pointDetails[1].split('-')
						obj.kind.objectSpawner.startingLocation = regionListDict[coord[0]][coord[1]],

		if Data.startswith('spawnContainers='):
			hasSpawnContainers = True
			containersList = Data[16:-1]
			if containersList != '':
				containersList = containersList.split(", ")
				#print '***' + str(containersList)
				for container in containersList:
					containerDetails = container.split(":")
					#print '***' + str(containerDetails)
					containerSpecs = containerDetails[1].split("-")

					item = containerDetails[0]
					destRegion = containerSpecs[0]
					destRoom = containerSpecs[1]
					destContainer = containerSpecs[2]

					for obj in newRoom.objects:
						if obj.name == item:
							obj.spawnContainer = [item, destRegion, destRoom, destContainer]

		if Data.startswith('stuffList='):
			stuffList = Data[10:-1]
			stuffList = stuffList.split(', ')

			for entry in stuffList:
				if entry != '':
					stuffDesc = entry.split(':')
					item = stuffDesc[0]
					container = stuffDesc[1]
					#print "container:" + container
					resultsList = []
					ID = False
					objObject = None
					for obj in newRoom.objects:
						if obj.name == item:
							objObject = obj
						# if hasattr(obj, 'kind'):
						# 	#print "$$$$$$stuff2kind"
						# 	if hasattr(obj.kind, 'inventory'):
						# 		#print "$$$$$stuff2inv"
						if obj.name == container:
							#print "$$$$$stuff2cont " + ob.name
							# print newRoom.objects
							# if obj in newRoom.objects:
							# 	newRoom.objects.remove(obj)	
							# ob.kind.inventory.append(obj)
							resultsList.append(obj)
							#print ob.kind.inventory
						elif obj.name == container[:-1]:
							resultsList.append(obj)
							ID = True

					if resultsList != []:
						# for obj in resultsList:
						# 	print obj.name
						# print 'res:' + str(resultsList)
						# print 'con:' + str(container)
						# print 'conID:' + str(container[-1:])
						if ID == True:
							selected = resultsList[int(container[-1:]) - 1]
							#print 'id'
						else:
							selected = resultsList[0]
						#print selected
						if objObject in newRoom.objects:
							newRoom.objects.remove(objObject)
						selected.kind.inventory.append(objObject)
						#print 'inv:' +str(selected.kind.inventory)

		if Data.startswith('mobs='):

			mobString = Data[5:-1]
			if mobString != '':
				print "mobs found in file definition"

				fileList = os.listdir('data/world/battles/mobs/'+newRoom.name)



				# mobList = mobString.split(", ")
				# for mob in mobList:
				# 	for proto in Globals.mobsFromFile:
				# 		if proto.name == mob:
				# 			protoMob = proto
				# 	protoInv = []
				# 	for item in protoMob.kind.inventory:
				# 		protoInv.append(item)
				# 	protoEq = {}
				# 	for item in protoMob.kind.equipment:
				# 		protoEq.append(item)

				# 	mortalComponent = World.mortal(protoMob.kind.hp, protoMob.kind.exp, protoInv, protoMob.kind.inventorySize, protoEq)

				# 	newMob = World.Mob(protoMob.description, newRoom, protoMob.name, newRoom.region, protoMob.longDescription, protoMob.speech, mortalComponent, protoMob.species, protoMob.expirator)

				# 	moveAIComponent = aiMove.movementAI(newMob, int(protoMob.aiMove.time))
				# 	if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.basicRandom:
				# 		moveAIComponent.Timer.actionFunction = moveAIComponent.basicRandom
				# 	if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.introvertRandom:
				# 		moveAIComponent.Timer.actionFunction = moveAIComponent.introvertRandom
				# 	if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.extrovertRandom:
				# 		moveAIComponent.Timer.actionFunction = moveAIComponent.extrovertRandom
				# 	if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.doNotMove:
				# 		moveAIComponent.Timer.actionFunction = moveAIComponent.doNotMove
				# 	newMob.aiMove = moveAIComponent

				# 	Globals.MoveTIMERS.remove(newMob.aiMove.Timer)
				# 	Globals.TIMERS.remove(newMob.expirator.Timer)

				# 	mobs.append(newMob)





	labelString = newRoom.region + newRoom.name.capitalize()
	#print 'ls:' + labelString
	Globals.masterRooms[labelString] = newRoom
	Globals.regionListDict[newRoom.region][newRoom.name] = newRoom
	for mobFile in fileList:
		MobInit.loadSavedMobFromFile(str(mobFile), 'data/world/battles/mobs/'+newRoom.name+'/', isBattle=True)

	# for mob in mobs:
	# 	print mob.name
	# 	Globals.regionListDict[newRoom.region][newRoom.name].mobs.append(mob)



	# if hasSpawnContainers:
	# 	found = False
	# 	for region in Globals.regionListDict:
	# 		for room in Globals.regionListDict[region]:
	# 			roomObj = Globals.regionListDict[region][room]
	# 			#print '****regionRooms:' + str(Globals.regionListDict[region][room])
	# 	#print Globals.regionListDict
	# 			# print 'roomName:' + roomObj.name
	# 			# print 'destRoom:' + destRoom
	# 			if roomObj == Globals.regionListDict[destRegion][destRoom]:
	# 				for obj in roomObj.objects:
	# 					if obj.name == destContainer:
	# 						for thing in roomObj.objects:
	# 							if thing.name == item and found == False:
	# 								roomObj.objects.remove(thing)
	# 								obj.inventory.append(thing)
	# 								found = True



	print "name=" + newRoom.name
	print "region=" + newRoom.region
	print "description=" + newRoom.description
	print "longDescription" + newRoom.longDescription
	print "exits=" + str(newRoom.exits)
	print "objects=" + str(newRoom.objects)
	print 'mobs=' + str(newRoom.mobs)
	print "\n"


	#print newRoom
	return newRoom


def loadRoom(file):
	'''
	loads the contents of one room definition file into the world, and initializes the room with all required items and exits
	'''

	if str(file).endswith('~'):
		return

	print file

	path = 'blueprints/world/' + file
	if os.path.exists('data/world/' + file):
		path = 'data/world/' + file
	with open(path, 'r') as f:
		fileData = f.readlines()

	print fileData



	# name = None
	# region = None
	# description = None
	# longDescription = None
	# exits = {}
	# objects = []
	fileDetails = file.split("/")
	newRoom = regionListDict[fileDetails[0]][fileDetails[1]]

	newRoom.players = []
	newRoom.mobs = []

	item = ''
	destRegion = ''
	destRoom = ''
	destContainer = ''
	hasSpawnContainers = False
	activesList = []
	mobs = []
	equipment = []

	for Data in fileData:


		if Data.startswith('name='):
			newRoom.name = Data[5:-1]
			#print "name-" + newRoom.name

		if Data.startswith('region='):
			newRoom.region = Data[7:-1]

		if Data.startswith('description='):
			newRoom.description = Data[13:-2]

		if Data.startswith('longDescription='):
			newRoom.longDescription = Data[17:-2]

		if Data.startswith('exits='):
			#print Data
			exitsDict = {}
			exitsList = (Data[6:-1]).split(', ')
			#print exitsList
			regionRooms = Globals.regionListDict[newRoom.region]
			for exit in exitsList:
				if exit != '':
					exitDetails = (exit).split(':')
					#print exitDetails
					exitsDict[exitDetails[1]] = Globals.regionListDict[exitDetails[0]][exitDetails[1]]
			newRoom.exits = exitsDict

		if Data.startswith('actives='):
			activesList = Data[8:-1]
			activesList = activesList.split(", ")
			print 'actives:' + str(activesList)

		if Data.startswith('objects='):
			#print Data
			objectList = Data[8:-1]
			objectList = objectList.split(", ")
			print 'objectList:' + str(objectList)
			spawnList = []
			#print "ffl:"+str(Globals.fromFileList)
			for obj in objectList:
				#print obj
				for ob in Globals.fromFileList:
					if ob.name == obj:
						print '!!!name:' + str(ob.name)
						if hasattr(ob, 'kind'):
							#print '!!!kind'
							if hasattr(ob.kind, 'objectSpawner'):
								#print '!!!objSpwn'
								act = False
								#print '###actives:' + str(activesList)
								for spawner in activesList:
									# print 'spn:' + spawner
									# print 'ob:' + ob.name
									if str(ob.name) == str(spawner):
										act = True
										activesList.remove(spawner)
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=act, whereFrom='file')
								if act == False and hasattr(newObject, 'kind') and hasattr(newObject.kind,'objectSpawner') and hasattr(newObject.kind.objectSpawner,'timer'):
									Globals.TIMERS.remove(newObject.kind.objectSpawner.timer)
								spawnList.append(newObject)
							else:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
								spawnList.append(newObject)
						else:
							if hasattr(ob, 'mobSpawner'):
								print str(ob.mobSpawner.mode)
							newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
							spawnList.append(newObject)

			newRoom.objects = spawnList
			Rooms.setCurrentRoom(newRoom.objects, newRoom)
			#print newRoom.name
			for obj in newRoom.objects:
				print str((obj.name, obj.currentRoom.name))

		if Data.startswith('spawnPoints='):
			pointsList = Data[12:-1]
			pointsList = pointsList.split(", ")
			for point in pointsList:
				pointDetails = point.split(":")
				for obj in newRoom.objects:
					if obj.name == pointDetails[0]:
						coord = pointDetails[1].split('-')
						obj.kind.objectSpawner.startingLocation = regionListDict[coord[0]][coord[1]],

		if Data.startswith('spawnContainers='):
			hasSpawnContainers = True
			containersList = Data[16:-1]
			if containersList != '':
				containersList = containersList.split(", ")
				#print '***' + str(containersList)
				for container in containersList:
					containerDetails = container.split(":")
					#print '***' + str(containerDetails)
					containerSpecs = containerDetails[1].split("-")

					item = containerDetails[0]
					destRegion = containerSpecs[0]
					destRoom = containerSpecs[1]
					destContainer = containerSpecs[2]

					for obj in newRoom.objects:
						if obj.name == item:
							obj.spawnContainer = [item, destRegion, destRoom, destContainer]

		if Data.startswith('stuffList='):
			stuffList = Data[10:-1]
			stuffList = stuffList.split(', ')

			for entry in stuffList:
				if entry != '':
					stuffDesc = entry.split(':')
					item = stuffDesc[0]
					container = stuffDesc[1]
					#print "container:" + container
					resultsList = []
					ID = False
					objObject = None
					for obj in newRoom.objects:
						if obj.name == item:
							objObject = obj
						# if hasattr(obj, 'kind'):
						# 	#print "$$$$$$stuff2kind"
						# 	if hasattr(obj.kind, 'inventory'):
						# 		#print "$$$$$stuff2inv"
						if obj.name == container:
							#print "$$$$$stuff2cont " + ob.name
							# print newRoom.objects
							# if obj in newRoom.objects:
							# 	newRoom.objects.remove(obj)	
							# ob.kind.inventory.append(obj)
							resultsList.append(obj)
							#print ob.kind.inventory
						elif obj.name == container[:-1]:
							resultsList.append(obj)
							ID = True

					if resultsList != []:
						# for obj in resultsList:
						# 	print obj.name
						# print 'res:' + str(resultsList)
						# print 'con:' + str(container)
						# print 'conID:' + str(container[-1:])
						if ID == True:
							selected = resultsList[int(container[-1:]) - 1]
							#print 'id'
						else:
							selected = resultsList[0]
						#print selected
						if objObject in newRoom.objects:
							newRoom.objects.remove(objObject)
						selected.kind.inventory.append(objObject)
						#print 'inv:' +str(selected.kind.inventory)

		if Data.startswith('mobs='):

			mobString = Data[5:-1]
			if mobString != '':
				print "mobs found in file definition."
				mobList = mobString.split(", ")
				for mob in mobList:
					for proto in Globals.mobsFromFile:
						if proto.name == mob:
							protoMob = proto
					protoInv = []
					for item in protoMob.kind.inventory:
						protoInv.append(item)
					protoEq = {}
					for item in protoMob.kind.equipment:
						protoEq.append(item)

					mortalComponent = World.mortal(hp=int(protoMob.kind.hp), maxHp=int(protoMob.kind.maxHp), pp=int(protoMob.kind.pp), maxPp=int(protoMob.kind.maxPp), level=int(protoMob.kind.level), exp=int(protoMob.kind.exp), money=int(protoMob.kind.money), offense=int(protoMob.kind.offense), defense=int(protoMob.kind.defense), speed=int(protoMob.kind.speed), guts=int(protoMob.kind.guts), luck=int(protoMob.kind.luck), vitality=int(protoMob.kind.vitality), IQ=int(protoMob.kind.IQ), inventory=protoInv, inventorySize=int(protoMob.kind.inventorySize), equipment=protoEq)
					newMob = World.Mob(description=protoMob.description, currentRoom=newRoom, name=protoMob.name, region=newRoom.region, longDescription=protoMob.longDescription, speech=protoMob.speech, kind=mortalComponent, species=protoMob.species, expirator=protoMob.expirator)

					moveAIComponent = aiMove.movementAI(newMob, int(protoMob.aiMove.time))
					if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.basicRandom:
						moveAIComponent.Timer.actionFunction = moveAIComponent.basicRandom
					if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.introvertRandom:
						moveAIComponent.Timer.actionFunction = moveAIComponent.introvertRandom
					if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.extrovertRandom:
						moveAIComponent.Timer.actionFunction = moveAIComponent.extrovertRandom
					if protoMob.aiMove.Timer.actionFunction == protoMob.aiMove.doNotMove:
						moveAIComponent.Timer.actionFunction = moveAIComponent.doNotMove
					newMob.aiMove = moveAIComponent
					newMob.aiBattle = protoMob.aiBattle

					mobs.append(newMob)


		if Data.startswith('equipment='):
			equipmentString = Data[10:-1]
			print equipmentString
			if equipmentString != '':
				print 'equipment found in room definition file.'
				equipmentList = equipmentString.split(", ")
				print equipmentList

				for eq in equipmentList:
					for proto in Globals.equipmentFromFile:
						if proto.name == eq:
							protoEq = proto

					if hasattr(protoEq.kind.equipment, 'weapon'):
						if protoEq.kind.equipment.weapon != None:
							newWeapon = World.weapon()
						else:
							newWeapon = None
					else:
						newWeapon = None
					if hasattr(protoEq.kind.equipment, 'armor'):
						if protoEq.kind.equipment.armor != None:
							newArmor = World.armor()
						else:
							newArmor = None
					else:
						newArmor = None

					newEquipment = World.equipment(None)
					newItem = World.item()
					newObject = World.Object(None, None)


					newEquipment.owner = newItem
					if protoEq.kind.equipment.weapon != None:
						newEquipment.weapon = newWeapon
					else:
						newEquipment.weapon = None
					if protoEq.kind.equipment.armor != None:
						newEquipment.armor = newArmor
					else:
						newEquipment.armor = None
					newEquipment.slot = protoEq.kind.equipment.slot
					newEquipment.durability = protoEq.kind.equipment.durability
					newEquipment.maxDurability = protoEq.kind.equipment.maxDurability
					newEquipment.worth = protoEq.kind.equipment.worth
					newEquipment.hp = protoEq.kind.equipment.hp
					newEquipment.pp = protoEq.kind.equipment.pp
					newEquipment.offense = protoEq.kind.equipment.offense
					newEquipment.defense = protoEq.kind.equipment.defense
					newEquipment.speed = protoEq.kind.equipment.speed
					newEquipment.guts = protoEq.kind.equipment.guts
					newEquipment.luck = protoEq.kind.equipment.luck
					newEquipment.vitality = protoEq.kind.equipment.vitality
					newEquipment.IQ = protoEq.kind.equipment.IQ
					newEquipment.statusEffect = protoEq.kind.equipment.statusEffect
					bcList = []
					for command in protoEq.kind.equipment.battleCommands:
						bcList.append(command)
					newEquipment.battleCommands = bcList
					newEquipment.onUse = protoEq.kind.equipment.onUse


					newItem.isCarryable = protoEq.kind.isCarryable
					newItem.respawns = protoEq.kind.respawns
					newItem.itemGrabHandler = protoEq.kind.itemGrabHandler
					newItem.objectSpawner = protoEq.kind.objectSpawner
					newItem.equipment = newEquipment
					newItem.onUse = protoEq.kind.onUse


					newObject.name = protoEq.name
					newObject.description = protoEq.description
					newObject.isVisible = protoEq.isVisible
					newObject.spawnContainer = protoEq.spawnContainer
					newObject.longDescription = protoEq.longDescription
					newObject.kind = newItem
					newObject.TIMERS = Globals.TIMERS


					equipment.append(newObject)





	labelString = newRoom.region + newRoom.name.capitalize()
	#print 'ls:' + labelString
	Globals.masterRooms[labelString] = newRoom
	Globals.regionListDict[newRoom.region][newRoom.name] = newRoom

	for mob in mobs:
		print mob.name
		Globals.regionListDict[newRoom.region][newRoom.name].mobs.append(mob)
		mob.currentRoom = Globals.regionListDict[newRoom.region][newRoom.name]

	print "equipment:" + str(equipment)
	Globals.regionListDict[newRoom.region][newRoom.name].equipment = []
	for eq in equipment:
		print eq.name
		Globals.regionListDict[newRoom.region][newRoom.name].equipment.append(eq)
		print Globals.regionListDict[newRoom.region][newRoom.name].equipment
		eq.currentRoom = newRoom
		eq.kind.owner = eq
		eq.kind.equipment.owner = eq.kind
		if eq.kind.itemGrabHandler:
			eq.kind.itemGrabHandler.owner = eq.kind
		if eq.kind.objectSpawner:
			eq.kind.objectSpawner.owner = eq.kind





	# if hasSpawnContainers:
	# 	found = False
	# 	for region in Globals.regionListDict:
	# 		for room in Globals.regionListDict[region]:
	# 			roomObj = Globals.regionListDict[region][room]
	# 			#print '****regionRooms:' + str(Globals.regionListDict[region][room])
	# 	#print Globals.regionListDict
	# 			# print 'roomName:' + roomObj.name
	# 			# print 'destRoom:' + destRoom
	# 			if roomObj == Globals.regionListDict[destRegion][destRoom]:
	# 				for obj in roomObj.objects:
	# 					if obj.name == destContainer:
	# 						for thing in roomObj.objects:
	# 							if thing.name == item and found == False:
	# 								roomObj.objects.remove(thing)
	# 								obj.inventory.append(thing)
	# 								found = True



	print "name=" + newRoom.name
	print "region=" + newRoom.region
	print "description=" + newRoom.description
	print "longDescription" + newRoom.longDescription
	print "exits=" + str(newRoom.exits)
	print "objects=" + str(newRoom.objects)
	print 'mobs=' + str(newRoom.mobs)
	print 'equipment=' + str(newRoom.equipment)
	print "\n"


	#print newRoom
	return newRoom


def setSpawnContainers(newRoom):
	for obj in newRoom.objects:
		#print obj.name
		try:
			if obj.spawnContainer is not None:
				print 'init:' + str(obj.spawnContainer)
				for thing in obj.spawnContainer:
					print thing
				if isinstance(obj.spawnContainer, World.Object):
					pass
				else:
					print 'sc:' + str(obj.spawnContainer)
					destination = Globals.regionListDict[obj.spawnContainer[1]][obj.spawnContainer[2]]
					print "destination:" + str(destination) + obj.spawnContainer[1] + ":" + obj.spawnContainer[2]
					#print destination.objects
					for item in destination.objects:
						print obj.spawnContainer
						#print obj.spawnContainer[3]
						#print item.name
						#print "destCont:" + str(obj.spawnContainer)
						#print item.name
						if not isinstance(obj.spawnContainer, World.Object):
							print obj.spawnContainer
							if item.name == obj.spawnContainer[3]:
								obj.spawnContainer = item
								# for ob in Globals.fromFileList:
								# 	if ob.name == obj.name
								print "spawnCont:" + str(obj.spawnContainer) + str(obj.spawnContainer.name)
		except:
			#print "obj.spawnContainer:" + str(obj.spawnContainer) + str(obj.spawnContainer.name)
			raise

	for obj in newRoom.equipment:
		#print obj.name
		try:
			if obj.spawnContainer is not None:
				print 'init:' + str(obj.spawnContainer)
				for thing in obj.spawnContainer:
					print thing
				if isinstance(obj.spawnContainer, World.Object):
					pass
				else:
					print 'sc:' + str(obj.spawnContainer)
					destination = Globals.regionListDict[obj.spawnContainer[1]][obj.spawnContainer[2]]
					print "destination:" + str(destination) + obj.spawnContainer[1] + ":" + obj.spawnContainer[2]
					#print destination.objects
					for item in destination.objects:
						print obj.spawnContainer
						#print obj.spawnContainer[3]
						#print item.name
						#print "destCont:" + str(obj.spawnContainer)
						#print item.name
						if not isinstance(obj.spawnContainer, World.Object):
							print obj.spawnContainer
							if item.name == obj.spawnContainer[3]:
								obj.spawnContainer = item
								# for ob in Globals.fromFileList:
								# 	if ob.name == obj.name
								print "spawnCont:" + str(obj.spawnContainer) + str(obj.spawnContainer.name)
		except:
			#print "obj.spawnContainer:" + str(obj.spawnContainer) + str(obj.spawnContainer.name)
			raise




def setup():
	fileList=[]
	for region in Globals.RegionsList:
		directoryFiles = os.listdir('blueprints/world/'+str(region)+'/')
		for roomFile in directoryFiles:
			path = str(region)+'/'+ roomFile
			fileList.append(path)
	newRooms = []
	for room in fileList:
		if room is not None:
			newRooms.append(loadRoom(room))
		#print newRooms
	for room in newRooms:
		if room is not None:
			setSpawnContainers(room)

	# for room in Globals.masterRooms:
	# 	print room
	# 	for obj in Globals.masterRooms[room].objects:
	# 		print obj
	# 		if obj.kind:
	# 			if obj.kind.objectSpawner:
	# 				stuffed = obj.kind.objectSpawner.stuff(obj.kind.objectSpawner)
	# 				if stuffed:
	# 					print obj.name + " stuffed"