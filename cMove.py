# cMove.py
"""
This file describes all of the movement-related commands.
"""

import Regions
import Rooms
import cInfo, cInteractions



def move(client, cmd, args, CLIENT_LIST, CLIENT_DATA, exits):
	"""
	moves from one room to the next.
	"""

	#client.send( "moving to " + str(cmd) )
	clientDataID = str(client.addrport())


	# newRoomName = str(cmd)
	player = CLIENT_DATA[clientDataID].avatar

	alert(client, CLIENT_DATA, ("\n^g%s left.^~\n" %player.name))

	player.currentRoom.players.remove(player)
	player.currentRoom = exits[cmd]
	player.currentRoom.players.append(player)

	for item in player.kind.inventory:
		item.currentRoom = player.currentRoom

	for mob in player.currentRoom.mobs:
		if mob.expirator != None:
			mob.expirator.resetTimer()

	cInfo.render_room(client, player, player.currentRoom, CLIENT_DATA)

	alert(client, CLIENT_DATA, ("\n^g^!%s has entered.^~\n" %player.name))


def alert(client, CLIENT_DATA, messageString):
	"""
	Lets other players know about movement into or out of a room
	"""
	
	clientDataID = str(client.addrport())
	player = CLIENT_DATA[clientDataID].avatar
	for guest in player.currentRoom.players:
		if player.currentRoom == guest.currentRoom and player != guest:
			guest.client.send_cc(messageString)

def fleeBattle(client, args, CLIENT_LIST, CLIENT_DATA):
	'''
	tries to escape from a battle room
	'''
	cInteractions.stopBattle(CLIENT_DATA[str(client.addrport())].avatar.currentRoom)