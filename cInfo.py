# cInfo.py

"""
This file describes all the commands used to gather more information about the environment
"""

import Rooms


def look(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Gives more information about the room.  Without arguments, it displays description of the room.  With an argument, it displays the description of whatever item is named by the arguments
	"""
	clientDataID = str(client.addrport())
	#print args

	if args == []:
		display_description(client, room=CLIENT_DATA[clientDataID].avatar.currentRoom)
		display_exits(client, room=CLIENT_DATA[clientDataID].avatar.currentRoom)


def examine(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	More detailed info than look.  Without arguments, it shows the long description of the current room.  With arguments, it shows the long description of the item that is named by the arguments
	"""
	clientDataID = str(client.addrport())

	if args == []:
		examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom )








def render_room(client, player, room):
    """
    Displays the details of whatever room the client is in to the client on room entry
    """
    region = room.region
    regionRoom = str(region)+room.name.capitalize()
    roomDescription = Rooms.master[regionRoom].description
    roomName = Rooms.master[regionRoom].name
    roomMobs = Rooms.master[regionRoom].mobs
    roomContainers = Rooms.master[regionRoom].containers
    roomPlayers = Rooms.master[regionRoom].players
    roomExits = Rooms.master[regionRoom].exits.keys()

    client.send_cc("\n^I" + region + " >> " + roomName + "^~\n\n")
    client.send(roomDescription + "\n\n")
    client.send_cc("^!Exits: " + str(roomExits) + "^~\n\n")

def examine_room(client, player, region, room):
	"""
	Displays more information than render_room
	"""
	regionRoom = str(region)+room.name.capitalize()
	roomDescription = Rooms.master[regionRoom].longDescription
	roomName = Rooms.master[regionRoom].name
	roomMobs = Rooms.master[regionRoom].mobs
	roomContainers = Rooms.master[regionRoom].containers
	roomPlayers = Rooms.master[regionRoom].players
	roomExits = Rooms.master[regionRoom].exits.keys()

	client.send_cc("^I\nRegion: " + region +"\n")
	client.send_cc("Room Name: " + roomName + "^~\n\n")
	client.send(roomDescription + "\n\n")
	client.send_cc("^!Exits: " + str(roomExits) + "^~\n\n")

def display_description(client, room = None, item = None, entity = None):
	#print display_description
	if room != None:
		region =  room.region
		regionRoom = str(region)+room.name.capitalize()
    	roomDescription = Rooms.master[regionRoom].description
    	client.send("\n" + str(roomDescription) + "\n\n")

	if item != None:
		pass

	if entity != None:
		pass

def display_exits(client, room):
	region =  room.region
	regionRoom = str(region)+room.name.capitalize()
	roomExits = Rooms.master[regionRoom].exits.keys()
	client.send_cc("^!Exits: " + str(roomExits) + "^~\n\n")
