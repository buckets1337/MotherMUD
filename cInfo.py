# cInfo.py

"""
This file describes all the commands used to gather more information about the environment
"""

import Rooms, World


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
		client.send_cc("\n^I%s^~\n" %CLIENT_DATA[clientDataID].avatar.currentRoom.name)
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

	# handle examining at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory

	# handle looking at an object
	for obj in objectList:
		if obj.name == " ".join(args):
			client.send_cc("^c%s^~\n" %obj.description)
			looked = True

		if isinstance(obj.kind, World.container):
			for ob in obj.kind.inventory:
				if ob.name == " ".join(args):
					client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))
					looked = True

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
	examined = False
	inventory = False

	if args == []:
		# examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		client.send("What did you want to examine?\n")
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

	for obj in objectList:
		if obj.name == " ".join(args):
			client.send_cc("^c%s^~\n" %obj.longDescription)
			examined = True

			if isinstance(obj.kind, World.container):	# is a container, display the inventory
				client.send_cc("^c^UContents^u: ")
				for ob in obj.kind.inventory:
					if len(obj.kind.inventory) == 1:
						client.send_cc( "%s " %ob.name)
					else:
						client.send_cc( "%s, " %ob.name)
				client.send_cc("^~\n")

		elif isinstance(obj.kind, World.container):		# check container inventory for argument
			for ob in obj.kind.inventory:
				if ob.name == " ".join(args):
					client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.longDescription))
					examined = True

	# handle examining a player

	# handle examining a mob



	if examined == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I seem to recall the names of things better when I 'look harder' at a room!\n" %(" ".join(args)))
		else:
			client.send("You didn't say what you wanted to examine.\n")



def inventory(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Display the contents of the player avatar's inventory
	"""
	clientDataID = str(client.addrport())

	longestItemName = 0

	for obj in CLIENT_DATA[clientDataID].avatar.kind.inventory:
		if len(obj.name) > longestItemName:
			longestItemName = len(obj.name)

	client.send_cc("^U^!Item Name" + (longestItemName* " ") + "    Item Description^~\n")

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

	client.send_cc("\n^I" + roomName + "^~\n")
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

	client.send_cc("^I\nRegion: " + region +"\n")
	client.send_cc("Room Name: " + roomName + "\n^~\n")
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