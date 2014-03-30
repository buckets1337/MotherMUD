# cInfo.py

"""
This file describes all the commands used to gather more information about the environment
"""

import Rooms, World


def who(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Displays all players currently online
	"""

	client.send_cc("\n^I[ Players Online ]^~\n\n")
	for player in CLIENT_LIST:
		clientDataID = str(player.addrport())
		name = CLIENT_DATA[clientDataID].name
		if name != CLIENT_DATA[client.addrport()].name:
			client.send_cc("%s, %s\n" %(name, CLIENT_DATA[player.addrport()].avatar.title))
		else:
			client.send_cc("^!%s, %s (you)^~\n" %(CLIENT_DATA[client.addrport()].name, CLIENT_DATA[client.addrport()].avatar.title))
	if len(CLIENT_LIST) > 1:
		client.send("\n%s players online.\n\n" %len(CLIENT_LIST))
	elif len(CLIENT_LIST) == 1:
		client.send("\n%s player online.\n\n" %len(CLIENT_LIST))

def look(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Gives more information about the room.  Without arguments, it displays description of the room.  With an argument, it displays the description of whatever item is named by the arguments
	"""
	clientDataID = str(client.addrport())
	looked = False
	objectList = []
	inventory = False
	#print args

	if args == []:
		client.send_cc("\n^I[ %s ]^~\n" %CLIENT_DATA[clientDataID].avatar.currentRoom.name)
		display_description(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_objects(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_other_players(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_exits(client, CLIENT_DATA[clientDataID].avatar.currentRoom)
		looked = True

	elif args[0] == 'inventory' or args[0] == 'i':
		#print args[0]
		args = args[1:]
		inventory = True

	elif args[0] == 'harder':
		examine(client, ['lh'], CLIENT_LIST, CLIENT_DATA)
		return

	# handle looking at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory

	resultsList = []

	for obj in objectList:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)
			#print resultsList

		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
					if len(args) > 0:
						if args[-1] == ob.name: 
							resultsList.append(ob)
					elif len(args) > 1:
						if args[-2] == ob.name:
							resultsList.append(ob)
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	if len(resultsList) > 1:
		#print "args " + str(args)
		#print "arglen " + str(len(args))

		if len(args) >= 2:

			# numlist = [(x in range(0,99))]
			# if args[2] in numlist:
			try:
				if len(resultsList) >= int(args[1]):
					client.send_cc("^c%s^~\n" %resultsList[int(args[1]) - 1].description)
					looked = True

					if isinstance(resultsList[int(args[1]) - 1].kind, World.container):
						for ob in resultsList[int(args[1]) - 1].kind.inventory:
							# if ob.name == " ".join(args):
							client.send_cc("^c[In %s]: %s^~\n" %(resultsList[int(args[1]) - 1].name, ob.description))
			except ValueError:
				client.send("Object index must be an integer! I mean, it only makes sense.  Duh.\n")

		else:
			#print resultsList
			for obj in objectList:
				if obj.name == "_".join(args):
					client.send_cc("^c%s^~\n" %obj.description)
					looked = True
					

					if isinstance(obj.kind, World.container):
						for ob in resultsList[obj].kind.inventory:
							if ob.name == " ".join(args):
								client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))

	elif len(resultsList) == 1:
		#print resultsList
		for obj in resultsList:
			# if obj.name == "_".join(args):
			client.send_cc("^c%s^~\n" %obj.description)
			looked = True
			

			if isinstance(obj.kind, World.container):
				for ob in obj.kind.inventory:
					if ob.name == "_".join(args):
						client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))


	# handle looking at a player

	# handle looking at a mob



	if looked == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I like to 'look harder' to help me with the names of things!\n" %(" ".join(args)))
		else:
			client.send("You didn't say what you want to look at.\n")



def examine(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	More detailed info than look.  Without arguments, it shows the long description of the current room.  With arguments, it shows the long description of the item that is named by the arguments
	"""
	clientDataID = str(client.addrport())
	objectList = []
	examined = False
	inventory = False

	if args == []:
		# examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		client.send("What did I want to examine again?\n")
		examined = True


	elif args[0] == 'inventory' or args[0] == 'i':
		#print args[0]
		args = args[1:]
		inventory = True

	elif args[0] == 'lh':
		examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		args.pop(0)
		examined = True

	# handle examining at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory


	resultsList = []

	for obj in objectList:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)
			#print resultsList
		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
					if len(args) > 0:
						if args[-1] == ob.name: 
							resultsList.append(ob)
					elif len(args) > 1:
						if args[-2] == ob.name:
							resultsList.append(ob)
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	if len(resultsList) > 1:
		# print "args " + str(args)
		# print "arglen " + str(len(args))

		if len(args) >= 2:

			# numlist = []
			# for x in range(99):
			# 	numlist.append(x)
			# if args[1] in numlist:
			try:
				if len(resultsList) >= int(args[-1]):
					client.send_cc("^c%s^~\n" %resultsList[int(args[-1]) - 1].longDescription)
					examined = True

					if isinstance(resultsList[int(args[-1]) - 1].kind, World.container):
						#print"has inv"
						#print "isLocked: " + str(resultsList[int(args[-1]) - 1].kind.isLocked)
						if resultsList[int(args[-1]) - 1].kind.isLocked == False:
							for ob in resultsList[int(args[-1]) - 1].kind.inventory:
								# if ob.name == "_".join(args):
								client.send_cc("^c[In %s]: %s^~\n" %(resultsList[int(args[1]) - 1].name, ob.name))
							if resultsList[int(args[-1]) - 1].kind.inventory == []:
								client.send_cc("^c[In %s]:^~\n" %resultsList[int(args[1]) - 1].name)
						else:
							client.send_cc("^cThe %s is locked.^~\n" %resultsList[int(args[1]) - 1].name)
			except ValueError:
				client.send("Object index must be an integer! My mother always said!\n")

			# for obj in resultsList:
			# 	if args[-1] == obj.name or args[-2] == obj.name:
			# 		examine(client, [obj.name], CLIENT_LIST, CLIENT_DATA)
					


		else:
			#print resultsList
			for obj in resultsList:
				# if obj.name == "_".join(args):
				client.send_cc("^c%s^~\n" %obj.longDescription)
				examined = True

				if isinstance(obj.kind, World.container):
					if obj.kind.isLocked == False:
						for ob in obj.kind.inventory:
							client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.name))
						if obj.kind.inventory == []:
							client.send_cc("^c[In %s]:^~\n" %obj.name)
					else:
						client.send_cc("^cThe %s is locked.^~\n" %obj.name)	



	elif len(resultsList) == 1:
		#print resultsList
		for obj in resultsList:
			client.send_cc("^c%s^~\n" %obj.longDescription)
			examined = True

			if isinstance(obj.kind, World.container):
				if obj.kind.isLocked == False:
					for ob in obj.kind.inventory:
						client.send_cc("^c[In %s]: A %s^~\n" %(obj.name, ob.name))
					if obj.kind.inventory == []:
						client.send_cc("^c[In %s]:^~\n" %obj.name)
				else:
					client.send_cc("^cThe %s is locked.^~\n" %obj.name)					





	# for obj in objectList:
	# 	if obj.name == "_".join(args):
	# 		client.send_cc("^c%s^~\n" %obj.longDescription)
	# 		examined = True

	# 		if isinstance(obj.kind, World.container):	# is a container, display the inventory
	# 			client.send_cc("^c^UContents^u: ")
	# 			for ob in obj.kind.inventory:
	# 				if len(obj.kind.inventory) == 1:
	# 					client.send_cc( "%s " %ob.name)
	# 				else:
	# 					client.send_cc( "%s, " %ob.name)
	# 			client.send_cc("^~\n")

	# 	elif isinstance(obj.kind, World.container):		# check container inventory for argument
	# 		for ob in obj.kind.inventory:
	# 			if ob.name == " ".join(args):
	# 				client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.longDescription))
	# 				examined = True

	# handle examining a player

	# handle examining a mob



	if examined == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I seem to recall the names of things better when I 'look harder'!\n" %(" ".join(args)))
		else:
			client.send("I am not sure what I wanted to examine.\n")



def inventory(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Display the contents of the player avatar's inventory
	"""
	clientDataID = str(client.addrport())

	longestItemName = 0
	longestItemDescription = 0

	for obj in CLIENT_DATA[clientDataID].avatar.kind.inventory:
		if len(obj.name) > longestItemName:
			longestItemName = len(obj.name)
		if len(obj.name) > longestItemDescription:
			longestItemDescription = len(obj.name)

	client.send_cc("\n^I[" + ((longestItemName + 9)* " ") + "    Inventory" + ((longestItemDescription + 16)* " ") +"]^~\n")
	client.send_cc("\nSpace: " + str(len(CLIENT_DATA[clientDataID].avatar.kind.inventory)) + "/" + str(CLIENT_DATA[clientDataID].avatar.kind.inventorySize)+ " used. \n\n")

	client.send_cc("^U^!Item Name" + (longestItemName* " ") + "    Item Description"+ (longestItemDescription * " ") + "^~\n")

	for obj in CLIENT_DATA[clientDataID].avatar.kind.inventory:
		client.send_cc(str(obj.name) + (((9 + longestItemName) - len(obj.name)) * " ") + "    " + str(obj.description) + "\n")
	client.send("\n")




def render_room(client, player, room, CLIENT_DATA):
	"""
	Displays the details of whatever room the client is in to the client on room entry
	"""
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	# roomDescription = Rooms.master[regionRoom].description
	roomName = Rooms.master[regionRoom].name
	# roomMobs = Rooms.master[regionRoom].mobs
	roomObjects = Rooms.master[regionRoom].objects
	# roomPlayers = Rooms.master[regionRoom].players
	# roomExits = Rooms.master[regionRoom].exits.keys()

	client.send_cc("\n^I[ " + roomName + " ]^~\n")
	display_description(client, room, CLIENT_DATA)
	display_objects(client, room, CLIENT_DATA)
	display_other_players(client, room, CLIENT_DATA)
	display_exits(client, room)

def examine_room(client, player, region, room, CLIENT_DATA):
	"""
	Displays more information than render_room
	"""
	regionRoom = str(region)+room.name.capitalize()
	roomDescription = Rooms.master[regionRoom].longDescription
	roomName = Rooms.master[regionRoom].name
	# roomMobs = Rooms.master[regionRoom].mobs
	# roomContainers = Rooms.master[regionRoom].containers
	# roomPlayers = Rooms.master[regionRoom].players
	# roomExits = Rooms.master[regionRoom].exits.keys()

	client.send_cc("\n^I[ Region: " + region +" ]\n")
	client.send_cc("[ Room Name: " + roomName + " ]\n^~\n")
	client.send(roomDescription + "\n\n")
	#display_description(client, room, CLIENT_DATA)
	display_object_names(client, room, CLIENT_DATA)
	display_other_players(client, room, CLIENT_DATA, examine=True)
	display_exits(client, room)




def display_description(client, room, CLIENT_DATA):
	#print display_description
	region =  room.region
	regionRoom = str(region)+room.name.capitalize()
	roomDescription = Rooms.master[regionRoom].description
	client.send("\n" + str(roomDescription) + "\n\n")


def display_exits(client, room):
	region =  room.region
	regionRoom = str(region)+room.name.capitalize()
	roomExits = Rooms.master[regionRoom].exits.keys()
	client.send_cc("\n^UExits^u: " + str(roomExits) + "\n\n")


def display_other_players(client, room, CLIENT_DATA, examine=False):
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	roomPlayers = Rooms.master[regionRoom].players
	for player in roomPlayers:
		if player != CLIENT_DATA[str(client.addrport())].avatar and player.currentRoom == CLIENT_DATA[str(client.addrport())].avatar.currentRoom:
			if examine == True:
				client.send_cc("^gA player named ^~")
			client.send_cc("^g%s is here.^~\n" %player.name)


def display_objects(client, room, CLIENT_DATA):
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	roomObjects = Rooms.master[regionRoom].objects
	for obj in roomObjects:
		if obj.isVisible == True:
			client.send_cc("^c%s^~\n" %obj.description)


def display_object_names(client, room, CLIENT_DATA):
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	roomObjects = Rooms.master[regionRoom].objects
	for obj in roomObjects:
		if obj.isVisible == True:
			if obj.kind == None:
				client.send_cc("^cAn object named '%s'^~\n" %obj.name)
			elif isinstance(obj.kind, World.item):
				client.send_cc("^cAn item named '%s'^~\n" %obj.name)		
			elif isinstance(obj.kind, World.container):
				client.send_cc("^cA container named '%s'^~\n" %obj.name)