#onExits.py
#functions to run on exiting a room

import random
from cMove import teleport
import Globals

def teleportRandom(client, cmd, args, CLIENT_LIST, CLIENT_DATA, exits, argsList):
	'''
	teleports to a random room in the roomList

	argsList should be a list with only one entry, specifying the region in which to look for the random room
	'''
	#print 'teleported'
	#print exits
	clientDataID = client.addrport()
	player = CLIENT_DATA[clientDataID].avatar

	teleportArgs = []
	for arg in argsList:
		teleportArgs.append(arg)
	#print teleportArgs

	selectionList = []
	for room in Globals.regionListDict[argsList[0]]:
		if Globals.regionListDict[argsList[0]][room] != player.currentRoom and Globals.regionListDict[argsList[0]][room].name != 'bullpen':
			selectionList.append(room)


	selection = random.randint(0, len(selectionList)-1)
	roomName = selectionList[selection]

	teleportArgs.append(roomName)

	#print argsList

	client.send_cc("^!^YEverything freezes and a void evelops you.\n*POP*^~\n")

	teleport(client, cmd, teleportArgs, CLIENT_LIST, CLIENT_DATA, exits)



	return False

def gotoRoom(client, cmd, args, CLIENT_LIST, CLIENT_DATA, exits, argsList):
	'''
	moves a player to a room specified by the argsList.
	argsList is a list with argsList[0] being a string naming a region,
	and argsList[1] being a string naming a room
	'''
	#print argsList
	client.send_cc("^!^YYou feel reality pinch inward, and your view suddenly shifts.^~\n")
	teleport(client, cmd, argsList, CLIENT_LIST, CLIENT_DATA, exits)


	return False
