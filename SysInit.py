# SysInit.py
# Initializes various system-based information

import os, shelve
import World, Globals



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
	exp = None
	inventorySize = None
	inventoryItems = []

	print fileData
	for data in fileData:
		if data.startswith('name='):
			clientName = data[5:-1]
		if data.startswith('op='):
			op = data[3:-1]
		if data.startswith("prompt="):
			prompt = data[7:-1]
		if data.startswith("clientID="):
			clientID= data[9:-1]
		if data.startswith("title="):
			title = data[6:-1]
		if data.startswith("description="):
			description = data[12:-1]
		if data.startswith("currentRoom="):
			currentRoomString = data[12:-1]
			print "crs=" + currentRoomString
		if data.startswith("hp="):
			hp = int(data[3:-1])
		if data.startswith("exp="):
			exp = int(data[4:-1])
		if data.startswith("inventorySize="):
			inventorySize = int(data[14:-1])
		if data.startswith("inventory="):
			inventory = data[10:-1]
			inventory = inventory.split(", ")

			for item in inventory:
				print item
				for obj in Globals.fromFileList:
					print obj.name
					if item == obj.name:
						newItem = cmdSpawnObject(item, CLIENT_DATA[clientDataID].avatar.currentRoom)
						inventoryItems.append(newItem)
						CLIENT_DATA[clientDataID].avatar.currentRoom.objects.remove(newItem)


	print currentRoomString
	currentRoomCoord = currentRoomString.split(":")
	print str(currentRoomCoord)
	currentRoomRoom = Globals.regionListDict[currentRoomCoord[0]][currentRoomCoord[1]]

	newAvatar = World.Player(description, currentRoomRoom, clientName, client, clientDataID, title)

	CLIENT_DATA[clientDataID].name = clientName
	CLIENT_DATA[clientDataID].op = op
	CLIENT_DATA[clientDataID].prompt = prompt
	CLIENT_DATA[clientDataID].clientID = clientID
	CLIENT_DATA[clientDataID].avatar = newAvatar
	CLIENT_DATA[clientDataID].avatar.kind = kind
	print "********" + str(inventoryItems)
	CLIENT_DATA[clientDataID].avatar.kind.inventory = inventoryItems
	#CLIENT_DATA[clientDataID].avatar.currentRoom.players.append(newAvatar)
	CLIENT_DATA[clientDataID].avatar.kind.hp = hp
	CLIENT_DATA[clientDataID].avatar.kind.exp = exp
	CLIENT_DATA[clientDataID].avatar.kind.inventorySize = inventorySize
	CLIENT_DATA[clientDataID].avatar.currentRoom = currentRoomRoom

	# CLIENT_LIST.remove(client)
	# CLIENT_LIST.append(client)


def clientDataSave(client, CLIENT_LIST, CLIENT_DATA, TIMERS):

	clientDataID = str(client.addrport())
	print CLIENT_DATA
	print "cdi"+clientDataID
	player = CLIENT_DATA[clientDataID]
	CLIENT = clientDataID


	try:

		name = player.name
		op = player.op
		prompt = player.prompt
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
		exp = str(kind.exp)
		inventory = kind.inventory
		inventorySize = str(kind.inventorySize)
		equipment = kind.equipment



		path = 'data/client/' + name
		with open(path, 'w') as f:
			f.write(str(player.password) + "\n")
			f.write("name=" + name + "\n")
			f.write("op=" + str(op) + "\n")
			f.write("prompt=" + prompt + "\n")
			#f.write("client=" + client + "\n")
			f.write("clientID=" + clientID + "\n\n")
			#f.write("avatar=" + avatar + "\n")

			#f.write("avatarName=" + avatarName + "\n")		#name and avatarName are the same
			f.write("title=" + title + "\n")
			f.write("description=" + description + "\n")
			f.write("currentRoom=" + currentRoom + "\n\n")

			f.write("hp=" + hp + "\n")
			f.write("exp=" + exp + "\n")
			f.write("inventorySize=" + inventorySize + "\n\n")

			f.write("\ninventory=")

			location = 1
			for item in inventory:
				f.write(item.name + ", ")
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
			print client
			print CLIENT_DATA

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
				TI.write(str(timerID) + " attachedTo=" + TIMER.attachedTo.owner.owner.name + "\n")
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



def cmdSpawnObject(refobj, spawnLocation, active=False, whereFrom='cmd', spawnContainer=None):
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
                # if not stuffed:
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