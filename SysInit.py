# SysInit.py
# Initializes various system-based information

import os
import World, Globals
import RoomInit, MobInit



# checks for a previous set of server data, and if it is present, load it.
def clientDataLoad(client, CLIENT_LIST, CLIENT_DATA, TIMERS, kind):
	"""
	Loads the information in the client file to CLIENT_DATA
	"""

	clientDataID = str(client.addrport())
	name = CLIENT_DATA[clientDataID].name
	fileData = []
	path = 'data/client/' + name
	try:
		with open(path, 'r') as CD:
			fileData = CD.readlines()
	except:
		print "!! " + path + " not found, " + name + " failed to load."




	clientName = ''
	op = False
	prompt = ''
	clientID = None
	title = ''
	description = ''
	currentRoomString = ''
	hp = None
	maxHp = None
	pp = None
	maxPp = None
	level = None
	exp = None
	money = None
	offense = None
	defense = None
	speed = None
	guts = None
	luck = None
	vitality = None
	IQ = None
	inventorySize = None
	inventoryItems = []
	gameState = None
	currentRoomRoom = None
	battleRoom = None
	battleRoomAttachedTo = None
	battleCommands = None
	rewardExp = 0
	rewardMoney = 0

	#print fileData
	for data in fileData:
		if data.startswith('name='):
			clientName = data[5:-1]
		if data.startswith('op='):
			op = data[3:-1]
		if data.startswith("prompt="):
			prompt = data[7:-1]
		if data.startswith('gameState='):
			gameState = data[10:-1]
		if data.startswith("battleRoom="):
			battleRoom = data[11:-1]
		if data.startswith("battleRoom.attachedTo="):
			battleRoomAttachedTo = data[22:-1]
			battleRoomAttachedTo = battleRoomAttachedTo.split(":")
		if data.startswith("clientID="):
			clientID= data[9:-1]
		if data.startswith("title="):
			title = data[6:-1]
		if data.startswith("description="):
			description = data[12:-1]
		if data.startswith("currentRoom="):
			currentRoomString = data[12:-1]
			#print "crs=" + currentRoomString
				#print currentRoomString
		if currentRoomString == '':
			currentRoomString = Globals.startingRoom.region + ":" + Globals.startingRoom.name
		currentRoomCoord = currentRoomString.split(":")
		#print str(currentRoomCoord)
		for region in Globals.regionListDict:
			for room in Globals.regionListDict[region]:
				if room == currentRoomCoord[1]:
					currentRoomRoom = Globals.regionListDict[currentRoomCoord[0]][currentRoomCoord[1]]

		#print currentRoomRoom.name
		if data.startswith("hp="):
			hp = int(data[3:-1])
		if data.startswith("maxHp="):
			maxHp = int(data[6:-1])
		if data.startswith("pp="):
			pp = int(data[3:-1])
		if data.startswith("maxPp="):
			maxPp = int(data[6:-1])
		if data.startswith("level="):
			level = int(data[6:-1])
		if data.startswith("exp="):
			exp = int(data[4:-1])
		if data.startswith("money="):
			money = int(data[6:-1])
		if data.startswith("rewardExp="):
			rewardExp = int(data[10:-1])
		if data.startswith("rewardMoney="):
			rewardMoney = int(data[12:-1])
		if data.startswith("offense="):
			offense = int(data[8:-1])
		if data.startswith("defense="):
			defense = int(data[8:-1])
		if data.startswith("speed="):
			speed = int(data[6:-1])
		if data.startswith("guts="):
			guts = int(data[5:-1])
		if data.startswith("luck="):
			luck = int(data[5:-1])
		if data.startswith("vitality="):
			vitality = int(data[9:-1])
		if data.startswith("IQ="):
			IQ = int(data[3:-1])
		if data.startswith("battleCommands="):
			battleCommands = data[15:-1]
			battleCommands = battleCommands.split(', ')
		if data.startswith("inventorySize="):
			inventorySize = int(data[14:-1])

		if data.startswith("inventory="):
			inventory = data[10:-1]
			inventory = inventory.split(", ")

			for item in inventory:
				#print item
				found = False
				for obj in Globals.fromFileList:
					#print obj.name
				 	if item == obj.name and found == False:
						#inventoryItems.append(obj)
						
						newItem = cmdSpawnObject(obj.name, currentRoomRoom, alert=False, whereFrom='playerinv')
						inventoryItems.append(newItem)
						currentRoomRoom.objects.remove(newItem)
						found = True
						#print 'invI:' + str(inventoryItems)





	#print Globals.startingRoom.players
	#print Globals.startingRoom
	newAvatar = World.Player(description=description, currentRoom=currentRoomRoom, name=clientName, client=client, clientDataID=clientDataID, title=title, rewardExp=rewardExp, rewardMoney=rewardMoney)
	newMortal = World.mortal(hp, maxHp, pp, maxPp, level, exp, money, offense, defense, speed, guts, luck, vitality, IQ, [])
	newMortal.inventory = []
	# print newAvatar.currentRoom.players
	# print newAvatar.currentRoom.name
	# print Globals.startingRoom.players
	# print Globals.startingRoom.name
	#print newAvatar.currentRoom
	#print 'morinv:' + str(newMortal.inventory)




	CLIENT_DATA[clientDataID].name = clientName
	CLIENT_DATA[clientDataID].op = op
	CLIENT_DATA[clientDataID].prompt = prompt
	CLIENT_DATA[clientDataID].clientID = clientID
	CLIENT_DATA[clientDataID].avatar = newAvatar
	CLIENT_DATA[clientDataID].avatar.kind = newMortal
	CLIENT_DATA[clientDataID].gameState = gameState
	CLIENT_DATA[clientDataID].avatar.battleCommands = battleCommands
	#print "********" + str(inventoryItems)

	if battleRoom != 'None' and battleRoom != '' and battleRoom != None:
		newBattleRoom = RoomInit.loadBattleRoom('battles/'+str(battleRoom))
		newBattleRoom.attachedTo = Globals.regionListDict[battleRoomAttachedTo[0]][battleRoomAttachedTo[1]]
		Globals.battleRooms.append(newBattleRoom)
		CLIENT_DATA[clientDataID].battleRoom = newBattleRoom
		currentRoomRoom = newBattleRoom

	for room in Globals.battleRooms:
		if room.name == currentRoomCoord[1]:
			currentRoomRoom = room

	for item in inventoryItems:
		CLIENT_DATA[clientDataID].avatar.kind.inventory.append(item)
		# print item.name
		# removed = False
		# newItem = cmdSpawnObject(item.name, CLIENT_DATA[clientDataID].avatar.currentRoom, alert=False, whereFrom='inv')
		# CLIENT_DATA[clientDataID].avatar.kind.inventory.append(newItem)
		# print newItem.name
		# for item in CLIENT_DATA[clientDataID].avatar.currentRoom.objects:
		# 	print item.name
		# 	if item.name == newItem.name and removed == False:
		# 		CLIENT_DATA[clientDataID].avatar.currentRoom.objects.remove(item)
		# 		removed = True
	#CLIENT_DATA[clientDataID].avatar.kind.inventory = inventoryItems
	#CLIENT_DATA[clientDataID].avatar.currentRoom.players.append(newAvatar)
	CLIENT_DATA[clientDataID].avatar.kind.hp = hp
	CLIENT_DATA[clientDataID].avatar.kind.exp = exp
	CLIENT_DATA[clientDataID].avatar.kind.inventorySize = inventorySize
	CLIENT_DATA[clientDataID].avatar.currentRoom = currentRoomRoom
	#print 'avcr:' +str(CLIENT_DATA[clientDataID].avatar.currentRoom.name)
	# for obj in CLIENT_DATA[clientDataID].avatar.currentRoom.objects:
	# 	print obj.currentRoom.name
	#print 'gsrp:'+str(Globals.startingRoom.players)

	# for item in inventoryItems:
	# 	newItem = cmdSpawnObject(item, CLIENT_DATA[clientDataID].avatar.currentRoom, alert=False, whereFrom='inv')
	# 	CLIENT_DATA[clientDataID].avatar.currentRoom.objects.remove(newItem)

	#print '&&:' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.name) + " " + str(CLIENT_DATA[clientDataID].avatar.currentRoom) + ":"+ str(Globals.startingRoom)
	#print '&&' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.players)
	#print str(Globals.startingRoom.players)
	CLIENT_DATA[clientDataID].avatar.currentRoom.players.append(CLIENT_DATA[clientDataID].avatar)
	#print CLIENT_DATA[clientDataID].avatar.kind.inventory
	# print str(Globals.startingRoom.players)
	# print '&&' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.players)
	# print str(CLIENT_DATA[clientDataID].avatar.currentRoom) + ":" + str(Globals.startingRoom)
	# print 'acrpl:' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.players)
	# print 'avcr:' +str(CLIENT_DATA[clientDataID].avatar.currentRoom.name)
	# print Globals.startingRoom.name
	# print Globals.startingRoom.players
	# #Globals.startingRoom.players.remove(CLIENT_DATA[clientDataID].avatar)
	# print 'acrpl:' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.players)
	# print 'avcr:' +str(CLIENT_DATA[clientDataID].avatar.currentRoom.name)
	# print Globals.startingRoom.name
	# print Globals.startingRoom.players
	# print 'loaded:' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.players) + " in:" + str(CLIENT_DATA[clientDataID].avatar.currentRoom.name)
	# print 'av:'+str(CLIENT_DATA[clientDataID].avatar.currentRoom.name)+ ' avp:'+ str(CLIENT_DATA[clientDataID].avatar.currentRoom.players)+' sr:' + str(Globals.startingRoom.name) + ' srp:'+ str(Globals.startingRoom.players)
	# print dir(CLIENT_DATA[clientDataID].avatar.kind)

	# CLIENT_LIST.remove(client)
	# CLIENT_LIST.append(client)


def clientDataSave(client, CLIENT_LIST, CLIENT_DATA, TIMERS):

	clientDataID = str(client.addrport())
	#print CLIENT_DATA
	#print "cdi"+clientDataID
	player = CLIENT_DATA[clientDataID]
	CLIENT = clientDataID

	if not os.path.exists('data'):
		os.mkdir('data')
	if not os.path.exists('data/world'):
		os.mkdir('data/world')
	if not os.path.exists('data/world/battles'):
		os.mkdir('data/world/battles')


	try:

		name = player.name
		op = player.op
		prompt = player.prompt
		gameState = player.gameState
		if player.battleRoom is not None:
			battleRoom = str(player.battleRoom.name)
		else:
			battleRoom = ''
		if player.battleRoom is not None:
			attachedTo = player.battleRoom.attachedTo
		else:
			attachedTo = ''
		#client = str(player.client)		# should be recreated on reload, not saved
		clientID = str(player.clientID)
		avatar = player.avatar 			# should be recreated on reload, not saved

		avatarName = avatar.name
		title = avatar.title
		description = player.avatar.description
		currentRoom = str(player.avatar.currentRoom.region+":"+player.avatar.currentRoom.name)
		#avatarClient = avatar.client
		#clientDataID = avatar.clientDataID
		kind = avatar.kind

		hp = str(kind.hp)
		maxHp = str(kind.maxHp)
		pp = str(kind.pp)
		maxPp = str(kind.maxPp)
		level = str(kind.level)
		exp = str(kind.exp)
		money = str(kind.money)
		offense = str(kind.offense)
		defense = str(kind.defense)
		speed = str(kind.speed)
		guts = str(kind.guts)
		luck = str(kind.luck)
		vitality = str(kind.vitality)
		IQ = str(kind.IQ)
		battleCommands = avatar.battleCommands
		inventory = kind.inventory
		inventorySize = str(kind.inventorySize)
		equipment = kind.equipment
		rewardExp = str(avatar.rewardExp)
		rewardMoney = str(avatar.rewardMoney)



		path = 'data/client/' + name
		with open(path, 'w') as f:
			f.write(str(player.password) + "\n")
			f.write("name=" + name + "\n")
			f.write("op=" + str(op) + "\n")
			f.write("prompt=" + prompt + "\n")
			#f.write("client=" + client + "\n")
			f.write("gameState=" + gameState + "\n")
			f.write("battleRoom=" + battleRoom + "\n")
			if battleRoom != '':
				f.write("battleRoom.attachedTo=" + attachedTo.region + ":" + attachedTo.name + "\n")
			else:
				f.write("battleRoom.attachedTo=\n")
			f.write("clientID=" + clientID + "\n\n")
			#f.write("avatar=" + avatar + "\n")

			#f.write("avatarName=" + avatarName + "\n")		#name and avatarName are the same
			f.write("title=" + title + "\n")
			f.write("description=" + description + "\n")
			f.write("currentRoom=" + currentRoom + "\n\n")

			f.write("hp=" + hp + "\n")
			f.write("maxHp=" + maxHp + "\n")
			f.write("pp=" + pp + "\n")
			f.write("maxPp=" + maxPp + "\n")
			f.write("level=" + level + "\n")
			f.write("exp=" + exp + "\n")
			f.write("money=" + money + "\n")
			f.write("rewardExp=" + rewardExp + "\n")
			f.write("rewardMoney=" + rewardMoney + "\n")
			f.write("offense=" + offense + "\n")
			f.write("defense=" + defense + "\n")
			f.write("speed=" + speed + "\n")
			f.write("guts=" + guts + "\n")
			f.write("luck=" + luck + "\n")
			f.write("vitality=" + vitality + "\n")
			f.write("IQ=" + IQ + "\n")

			commandList = ''
			for command in battleCommands:
				commandList += (str(command) + ", ")
			if str(commandList).endswith(", "):
				commandList = commandList[:-2]

			f.write("battleCommands=" + str(commandList) + "\n")
			
			f.write("inventorySize=" + inventorySize + "\n")

			f.write("\ninventory=")

			fileString = ''
			for item in inventory:
				fileString = fileString + (item.name + ", ")
			if fileString.endswith(', '):
				fileString = fileString[:-2]
			f.write(fileString)
			f.write("\n")

				# name = item.name
				# currentRoom = str((item.currentRoom.region, item.currentRoom.name))
				# isVisible = str(item.isVisible)
				# if item.spawnContainer is not None:
				# 	spawnContainer = item.spawnContainer.name
				# else:
				# 	spawnContainer = str(None)
				# kind = item.kind

				# f.write(str(location) + " " + name +".name=" + name + "\n")
				# f.write(str(location) + " " + name + ".currentRoom=" + currentRoom + "\n")
				# f.write(str(location) + " " + name + ".isVisible=" + isVisible + "\n")
				# f.write(str(location) + " " + name + ".spawnContainer=" + spawnContainer + "\n")

				# if isinstance(kind, World.item):
				# 	isCarryable = str(kind.isCarryable)
				# 	respawns = str(kind.respawns)
				# 	if kind.itemGrabHandler is not None:
				# 		itemGrabHandler = kind.itemGrabHandler
				# 	if kind.objectSpawner is not None:
				# 		objectSpawner = kind.objectSpawner

				# 	f.write(str(location) + " " + name +".isCarryable=" + isCarryable + "\n")
				# 	f.write(str(location) + " " + name +".respawns=" + respawns + "\n")


				# 	if kind.itemGrabHandler is not None:
				# 		notDroppable = str(itemGrabHandler.notDroppable)

				# 		f.write(str(location) + " " + name +".notDroppable=" + notDroppable + "\n")


				# 	if kind.objectSpawner is not None:
				# 		time = str(objectSpawner.time)
				# 		oddsList = str(objectSpawner.oddsList)
				# 		cycles = str(objectSpawner.cycles)
				# 		repeat = str(objectSpawner.repeat)
				# 		startingLocation = str((objectSpawner.startingLocation[0].region, objectSpawner.startingLocation[0].name))

				# 		f.write(str(location) + " " + name +".time=" + time + "\n")
				# 		f.write(str(location) + " " + name +".oddsList=" + oddsList + "\n")
				# 		f.write(str(location) + " " + name +".cycles=" + cycles + "\n")
				# 		f.write(str(location) + " " + name +".repeat=" + repeat + "\n")
				# 		f.write(str(location) + " " + name +".startingLocation=" + startingLocation + "\n")

				# 	f.write("\n")


				# if isinstance(kind, World.container):		# containers should probably not be able to be picked up
				# 	isLocked = str(kind.isLocked)
				# 	isCarryable = str(kind.isCarryable)
				# 	respawns = str(kind.respawns)
				# 	respawnContents = str(kind.respawnContents)
				# 	itemGrabHandler = kind.itemGrabHandler
				# 	objectSpawner= kind.objectSpawner

				# 	f.write(str(location) + " " + name +".isLocked=" + isLocked + "\n")
				# 	f.write(str(location) + " " + name +".isCarryable=" + isCarryable + "\n")
				# 	f.write(str(location) + " " + name +".respawns=" + respawns + "\n")
				# 	f.write(str(location) + " " + name +".respawnContents" + respawnContents + "\n")


				# 	if kind.itemGrabHandler is not None:
				# 		notDroppable = str(itemGrabHandler.notDroppable)

				# 		f.write(str(location) + " " + name +".notDroppable=" + notDroppable + "\n")


				# 	if kind.objectSpawner is not None:
				# 		time = str(objectSpawner.time)
				# 		oddsList = str(objectSpawner.oddsList)
				# 		cycles = str(objectSpawner.cycles)
				# 		repeat = str(objectSpawner.repeat)
				# 		startingLocation = str((objectSpawner.startingLocation[0].region, objectSpawner.startingLocation[0].name))

				# 		f.write(str(location) + " " + name +".time=" + time + "\n")
				# 		f.write(str(location) + " " + name +".oddsList=" + oddsList + "\n")
				# 		f.write(str(location) + " " + name +".cycles=" + cycles + "\n")
				# 		f.write(str(location) + " " + name +".repeat=" + repeat + "\n")
				# 		f.write(str(location) + " " + name +".startingLocation=" + startingLocation + "\n")

				# 	f.write("\n")
				# location += 1

			f.write("\nequipment=\n")

			# if battleRoom != None and battleRoom != 'None' and battleRoom != '':
			# 	RoomInit.saveRoom(player.battleRoom)
			if battleRoom != '':
				RoomInit.saveRoom(player.battleRoom)

				if not os.path.exists('data/world/battles/mobs'):
					os.mkdir('data/world/battles/mobs')
				if not os.path.exists('data/world/battles/mobs/'+player.battleRoom.name+'/'):
					os.mkdir('data/world/battles/mobs/'+player.battleRoom.name+'/')
				for mob in player.battleRoom.mobs:
					MobInit.saveMobToFile(mob, 'data/world/battles/mobs/'+player.battleRoom.name+'/')

	except:
		print "!! Failed to save CLIENT " + Globals.CLIENT_DATA[clientDataID].name
		raise


def dataSave(CLIENT_LIST, CLIENT_DATA, TIMERS):
	"""
	Saves the CLIENT_DATA and TIMERS lists to data/server/
	"""
	#print CLIENT_DATA

	try:
		for client in CLIENT_LIST:
			#print client
			#print CLIENT_DATA

			clientDataID = str(client.addrport())

			clientDataSave(client, CLIENT_LIST, CLIENT_DATA, Globals.TIMERS)
			# player = CLIENT_DATA[CLIENT]


			# name = player.name
			# prompt = player.prompt
			# #client = str(player.client)		# should be recreated on reload, not saved
			# clientID = str(player.clientID)
			# avatar = player.avatar 			# should be recreated on reload, not saved

			# avatarName = avatar.name
			# title = avatar.title
			# description = player.avatar.description
			# currentRoom = str(player.avatar.currentRoom.region+":"+player.avatar.currentRoom.name)
			# #avatarClient = avatar.client
			# #clientDataID = avatar.clientDataID
			# kind = avatar.kind

			# hp = str(kind.hp)
			# exp = str(kind.exp)
			# inventory = kind.inventory
			# inventorySize = str(kind.inventorySize)
			# equipment = kind.equipment



			# path = 'data/client/' + name
			# with open(path, 'w') as f:
			# 	f.write(str(player.password) + "\n")
			# 	f.write("name=" + name + "\n")
			# 	f.write("prompt=" + prompt + "\n")
			# 	#f.write("client=" + client + "\n")
			# 	f.write("clientID=" + clientID + "\n\n")
			# 	#f.write("avatar=" + avatar + "\n")

			# 	#f.write("avatarName=" + avatarName + "\n")		#name and avatarName are the same
			# 	f.write("title=" + title + "\n")
			# 	f.write("description=" + description + "\n")
			# 	f.write("currentRoom=" + currentRoom + "\n\n")

			# 	f.write("hp=" + hp + "\n")
			# 	f.write("exp=" + exp + "\n")
			# 	f.write("inventorySize=" + inventorySize + "\n\n")

			# 	f.write("\nInventory: ")

			# 	location = 1
			# 	for item in inventory:
			# 		f.write(item.name + ", ")
			# 	f.write("\n")

					# name = item.name
					# currentRoom = str((item.currentRoom.region, item.currentRoom.name))
					# isVisible = str(item.isVisible)
					# if item.spawnContainer is not None:
					# 	spawnContainer = item.spawnContainer.name
					# else:
					# 	spawnContainer = str(None)
					# kind = item.kind

					# f.write(str(location) + " " + name +".name=" + name + "\n")
					# f.write(str(location) + " " + name + ".currentRoom=" + currentRoom + "\n")
					# f.write(str(location) + " " + name + ".isVisible=" + isVisible + "\n")
					# f.write(str(location) + " " + name + ".spawnContainer=" + spawnContainer + "\n")

					# if isinstance(kind, World.item):
					# 	isCarryable = str(kind.isCarryable)
					# 	respawns = str(kind.respawns)
					# 	if kind.itemGrabHandler is not None:
					# 		itemGrabHandler = kind.itemGrabHandler
					# 	if kind.objectSpawner is not None:
					# 		objectSpawner = kind.objectSpawner

					# 	f.write(str(location) + " " + name +".isCarryable=" + isCarryable + "\n")
					# 	f.write(str(location) + " " + name +".respawns=" + respawns + "\n")


					# 	if kind.itemGrabHandler is not None:
					# 		notDroppable = str(itemGrabHandler.notDroppable)

					# 		f.write(str(location) + " " + name +".notDroppable=" + notDroppable + "\n")


					# 	if kind.objectSpawner is not None:
					# 		time = str(objectSpawner.time)
					# 		oddsList = str(objectSpawner.oddsList)
					# 		cycles = str(objectSpawner.cycles)
					# 		repeat = str(objectSpawner.repeat)
					# 		startingLocation = str((objectSpawner.startingLocation[0].region, objectSpawner.startingLocation[0].name))

					# 		f.write(str(location) + " " + name +".time=" + time + "\n")
					# 		f.write(str(location) + " " + name +".oddsList=" + oddsList + "\n")
					# 		f.write(str(location) + " " + name +".cycles=" + cycles + "\n")
					# 		f.write(str(location) + " " + name +".repeat=" + repeat + "\n")
					# 		f.write(str(location) + " " + name +".startingLocation=" + startingLocation + "\n")

					# 	f.write("\n")


					# if isinstance(kind, World.container):		# containers should probably not be able to be picked up
					# 	isLocked = str(kind.isLocked)
					# 	isCarryable = str(kind.isCarryable)
					# 	respawns = str(kind.respawns)
					# 	respawnContents = str(kind.respawnContents)
					# 	itemGrabHandler = kind.itemGrabHandler
					# 	objectSpawner= kind.objectSpawner

					# 	f.write(str(location) + " " + name +".isLocked=" + isLocked + "\n")
					# 	f.write(str(location) + " " + name +".isCarryable=" + isCarryable + "\n")
					# 	f.write(str(location) + " " + name +".respawns=" + respawns + "\n")
					# 	f.write(str(location) + " " + name +".respawnContents" + respawnContents + "\n")


					# 	if kind.itemGrabHandler is not None:
					# 		notDroppable = str(itemGrabHandler.notDroppable)

					# 		f.write(str(location) + " " + name +".notDroppable=" + notDroppable + "\n")


					# 	if kind.objectSpawner is not None:
					# 		time = str(objectSpawner.time)
					# 		oddsList = str(objectSpawner.oddsList)
					# 		cycles = str(objectSpawner.cycles)
					# 		repeat = str(objectSpawner.repeat)
					# 		startingLocation = str((objectSpawner.startingLocation[0].region, objectSpawner.startingLocation[0].name))

					# 		f.write(str(location) + " " + name +".time=" + time + "\n")
					# 		f.write(str(location) + " " + name +".oddsList=" + oddsList + "\n")
					# 		f.write(str(location) + " " + name +".cycles=" + cycles + "\n")
					# 		f.write(str(location) + " " + name +".repeat=" + repeat + "\n")
					# 		f.write(str(location) + " " + name +".startingLocation=" + startingLocation + "\n")

					# 	f.write("\n")
					# location += 1

				# f.write("\nEquipment:\n")

	except:
		print "!! Failed to save CLIENT " + CLIENT_DATA[clientDataID].name
		raise


	# try:
	# 	CD = shelve.open('data/server/CLIENT_DATA', writeback=True)

	# 	for CLIENT in CLIENT_DATA:
	# 		#print 'client name:' + CLIENT_DATA[CLIENT].name
	# 		clientKey = CLIENT_DATA[CLIENT].name
	# 		CD[clientKey] = CLIENT

	# except OSError:
	# 	print "Failed to save CLIENT_DATA"
	# 	return

	print TIMERS
	try:
		timerID = 0
		with open('data/server/TIMERS', 'w') as TI:
			for TIMER in Globals.TIMERS:
				TI.write(str(timerID) + " time=" + str(TIMER.time) + "\n")
				TI.write(str(timerID) + " actionFunction=" + str(TIMER.actionFunction) + "\n")
				TI.write(str(timerID) + " actionArgs=" + str(TIMER.actionArgs) + "\n")
				if hasattr(TIMER, 'attachedTo'):
					if TIMER.attachedTo != None:
						if hasattr(TIMER.attachedTo, 'owner'):
							if TIMER.attachedTo.owner != None:
								if hasattr(TIMER.attachedTo.owner, 'owner'):
									TI.write(str(timerID) + " attachedTo=" + TIMER.attachedTo.owner.owner.name + "\n")
								elif hasattr(TIMER.attachedTo, 'owner'):
									TI.write(str(timerID) + " attachedTo=" + TIMER.attachedTo.owner.name + "\n")
				TI.write(str(timerID) + " respawns=" + str(TIMER.respawns) + "\n")
				TI.write(str(timerID) + " currentTime=" + str(TIMER.currentTime) + "\n")
				TI.write(" \n")
				timerID += 1

	except:
		raise


	# try:
	# 	TI = shelve.open('data/server/TIMERS', writeback=True)
	# 	timerID = 0
	# 	timerIDexists = 'timerID' in TI
	# 	if timerIDexists:
	# 		timerID = TI['timerID']
	# 	else:
	# 		timerID = 1

	# 	for TIMER in TIMERS:
	# 		print "timer:" + str(TIMER) + " timerID:" + str(timerID)
	# 		timerKey = timerID
	# 		TI[timerKey] = TIMER
	# 		timerID += 1

	# 	TI['timerID'] = timerID

	# except OSError:
	# 	print "Failed to save TIMERS"
	# 	return


	# try:
	# 	CL = shelve.open('data/server/CLIENT_LIST', writeback=True)

	# 	for CLIENT in CLIENT_LIST:
	# 		clientKey = str(CLIENT.addrport())
	# 		CL[clientKey] = CLIENT

	# except OSError:
	# 	print "Failed to save CLIENT_LIST"
	# 	return


def cmdSpawnObject(refobj, spawnLocation, alert=True, active=False, whereFrom='cmd', spawnContainer=None):
    # creates a new object based on the attributes of the object fed to the function

    obj = None
    # if whereFrom == 'cmd':
    #     active = True
    #print Objects.fromFileList[0].name
    #print str(refobj)
    for thing in Globals.fromFileList:
        if thing.name == str(refobj):
            obj = thing
            #print obj
    if obj == None:
        print ("%s not found." %refobj)
        return

    newObject = World.Object(obj.name, obj.description)

    newObject.currentRoom = spawnLocation
    newObject.isVisible = obj.isVisible
    if obj.spawnContainer:
        newObject.spawnContainer = obj.spawnContainer
    else:
        newObject.spawnContainer = spawnContainer
    newObject.longDescription = obj.longDescription
    newObject.kind = obj.kind
    if newObject.kind:
        newObject.kind.owner = newObject
    newObject.TIMERS = obj.TIMERS
    # if newObject.TIMERS:
    #     newObject.TIMERS.owner = newObject

    if newObject.kind is not None:
        if isinstance(newObject.kind, World.item):
            newObject.kind = World.item()
            newObject.kind.owner = newObject
            newObject.kind.isCarryable = obj.kind.isCarryable
            newObject.kind.respawns = obj.kind.respawns
            newObject.kind.itemGrabHandler = obj.kind.itemGrabHandler
            if newObject.kind.itemGrabHandler:
                newObject.kind.itemGrabHandler.owner = newObject.kind
            newObject.kind.objectSpawner = obj.kind.objectSpawner
            if newObject.kind.objectSpawner:
                newObject.kind.objectSpawner.owner = newObject.kind

        if isinstance(newObject.kind, World.container):
            newObject.kind = World.container()
            newObject.kind.owner = newObject
            newObject.kind.inventory = []
            newObject.kind.isLocked = obj.kind.isLocked
            newObject.kind.isCarryable = obj.kind.isCarryable
            newObject.kind.respawns = obj.kind.respawns
            newObject.kind.respawnContents = obj.kind.respawnContents
            newObject.kind.itemGrabHandler = obj.kind.itemGrabHandler
            if newObject.kind.itemGrabHandler:
                newObject.kind.itemGrabHandler.owner = newObject.kind
            newObject.kind.objectSpawner = obj.kind.objectSpawner
            if newObject.kind.objectSpawner:
                newObject.kind.objectSpawner.owner = newObject.kind

        if newObject.kind.itemGrabHandler:
            newObject.kind.itemGrabHandler.notDroppable = obj.kind.itemGrabHandler.notDroppable

        if newObject.kind.objectSpawner:
            newObject.kind.objectSpawner = World.objectSpawner(newObject.kind)
            newObject.kind.objectSpawner.TIMERS = obj.kind.objectSpawner.TIMERS
            newObject.kind.objectSpawner.time = obj.kind.objectSpawner.time
            newObject.kind.objectSpawner.obj = obj.kind.objectSpawner.obj
            newObject.kind.objectSpawner.oddsList = obj.kind.objectSpawner.oddsList
            newObject.kind.objectSpawner.container = obj.kind.objectSpawner.container
            newObject.kind.objectSpawner.cycles = obj.kind.objectSpawner.cycles
            newObject.kind.objectSpawner.repeat = obj.kind.objectSpawner.repeat
            newObject.kind.objectSpawner.timer = World.Timer(newObject.kind.objectSpawner.TIMERS, newObject.kind.objectSpawner.time, newObject.kind.objectSpawner.spawn, [], newObject.kind.objectSpawner, newObject.kind.respawns)
            newObject.kind.objectSpawner.startingLocation = spawnLocation,

    if newObject.kind:
        if newObject.kind.objectSpawner:
            # print "has object spawner"
            newObject.kind.objectSpawner.active = active      # set the spawned object to active
            #print "active:" + str(newObject.kind.objectSpawner.active)

    spawnLocation.objects.append(newObject)
    symbol = '+'
    if whereFrom == 'cmd':
        symbol = 's'
    elif whereFrom == 'objSpawner':
        symbol = '$'
    elif whereFrom == 'inv':
    	symbol = 'i'
    if newObject.kind:
        if newObject.kind.objectSpawner:
            print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "] (active=" + str(newObject.kind.objectSpawner.active) +")"
        else:
            print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "]"
    else:
        print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "]"


    for client in Globals.CLIENT_LIST:
        if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
            if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == newObject.currentRoom:      # if a client is in the room object just appeared in, let it know
                if alert==True:
                	client.send_cc("^BA %s appeared.^~\n" %newObject.name)

    return newObject


# makes sure required directories exist, and if not, it creates them
path = [str("data/server/"), "data/client/", "data/log/auth/"]
for pathname in path:
	try:
		os.makedirs(pathname)
	except OSError:
		if not os.path.isdir(pathname):
			raise