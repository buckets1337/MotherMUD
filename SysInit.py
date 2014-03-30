# SysInit.py
# Initializes various system-based information

import os
import World


# checks for a previous set of server data, and if it is present, load it.
def dataLoad():
	"""
	Loads the CLIENT_DATA and TIMERS lists
	"""
	pass


def dataSave(CLIENT_LIST, CLIENT_DATA, TIMERS):
	"""
	Saves the CLIENT_DATA and TIMERS lists to data/server/
	# I'm pretty sure I want raw text files, not serialized files, but we'll see.
	"""
	#print CLIENT_DATA

	try:
		for CLIENT in CLIENT_DATA:

			player = CLIENT_DATA[CLIENT]


			name = player.name
			prompt = player.prompt
			#client = str(player.client)		# should be recreated on reload, not saved
			clientID = str(player.clientID)
			avatar = player.avatar 			# should be recreated on reload, not saved

			avatarName = avatar.name
			title = avatar.title
			description = player.avatar.description
			currentRoom = str((player.avatar.currentRoom.region, player.avatar.currentRoom.name))
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

				f.write("\nInventory:\n")

				location = 1
				for item in inventory:
					name = item.name
					currentRoom = str((item.currentRoom.region, item.currentRoom.name))
					isVisible = str(item.isVisible)
					if item.spawnContainer is not None:
						spawnContainer = item.spawnContainer.name
					else:
						spawnContainer = str(None)
					kind = item.kind

					f.write(str(location) + " " + name +".name=" + name + "\n")
					f.write(str(location) + " " + name + ".currentRoom=" + currentRoom + "\n")
					f.write(str(location) + " " + name + ".isVisible=" + isVisible + "\n")
					f.write(str(location) + " " + name + ".spawnContainer=" + spawnContainer + "\n")

					if isinstance(kind, World.item):
						isCarryable = str(kind.isCarryable)
						respawns = str(kind.respawns)
						if kind.itemGrabHandler is not None:
							itemGrabHandler = kind.itemGrabHandler
						if kind.objectSpawner is not None:
							objectSpawner = kind.objectSpawner

						f.write(str(location) + " " + name +".isCarryable=" + isCarryable + "\n")
						f.write(str(location) + " " + name +".respawns=" + respawns + "\n")


						if kind.itemGrabHandler is not None:
							notDroppable = str(itemGrabHandler.notDroppable)

							f.write(str(location) + " " + name +".notDroppable=" + notDroppable + "\n")


						if kind.objectSpawner is not None:
							time = str(objectSpawner.time)
							oddsList = str(objectSpawner.oddsList)
							cycles = str(objectSpawner.cycles)
							repeat = str(objectSpawner.repeat)
							startingLocation = str((objectSpawner.startingLocation[0].region, objectSpawner.startingLocation[0].name))

							f.write(str(location) + " " + name +".time=" + time + "\n")
							f.write(str(location) + " " + name +".oddsList=" + oddsList + "\n")
							f.write(str(location) + " " + name +".cycles=" + cycles + "\n")
							f.write(str(location) + " " + name +".repeat=" + repeat + "\n")
							f.write(str(location) + " " + name +".startingLocation=" + startingLocation + "\n")

						f.write("\n")


					if isinstance(kind, World.container):		# containers should probably not be able to be picked up
						isLocked = str(kind.isLocked)
						isCarryable = str(kind.isCarryable)
						respawns = str(kind.respawns)
						respawnContents = str(kind.respawnContents)
						itemGrabHandler = kind.itemGrabHandler
						objectSpawner= kind.objectSpawner

						f.write(str(location) + " " + name +".isLocked=" + isLocked + "\n")
						f.write(str(location) + " " + name +".isCarryable=" + isCarryable + "\n")
						f.write(str(location) + " " + name +".respawns=" + respawns + "\n")
						f.write(str(location) + " " + name +".respawnContents" + respawnContents + "\n")


						if kind.itemGrabHandler is not None:
							notDroppable = str(itemGrabHandler.notDroppable)

							f.write(str(location) + " " + name +".notDroppable=" + notDroppable + "\n")


						if kind.objectSpawner is not None:
							time = str(objectSpawner.time)
							oddsList = str(objectSpawner.oddsList)
							cycles = str(objectSpawner.cycles)
							repeat = str(objectSpawner.repeat)
							startingLocation = str((objectSpawner.startingLocation[0].region, objectSpawner.startingLocation[0].name))

							f.write(str(location) + " " + name +".time=" + time + "\n")
							f.write(str(location) + " " + name +".oddsList=" + oddsList + "\n")
							f.write(str(location) + " " + name +".cycles=" + cycles + "\n")
							f.write(str(location) + " " + name +".repeat=" + repeat + "\n")
							f.write(str(location) + " " + name +".startingLocation=" + startingLocation + "\n")

						f.write("\n")
					location += 1

				f.write("\nEquipment:\n")

	except:
		print "!! Failed to save CLIENT " + CLIENT_DATA[CLIENT].name
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

	# print TIMERS
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




# makes sure required directories exist, and if not, it creates them
path = [str("data/server/"), "data/client/", "data/log/auth"]
for pathname in path:
	try:
		os.makedirs(pathname)
	except OSError:
		if not os.path.isdir(pathname):
			raise