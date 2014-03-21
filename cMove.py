# cMove.py
"""
This file describes all of the movement-related commands.
"""

import Regions
import Rooms
import cInfo

def move(client, cmd, args, CLIENT_LIST, CLIENT_DATA, exits):
	"""
	moves from one room to the next.  Checks args for an exit, and if it exists, moves to that room.  Otherwise, tell the player the exit wasn't found
	"""
	#client.send( "moving to " + str(cmd) )
	clientDataID = str(client.addrport())


	# newRoomName = str(cmd)
	player = CLIENT_DATA[clientDataID].avatar

	player.currentRoom.players.remove(player)
	player.currentRoom = exits[cmd]
	player.currentRoom.players.append(player)

	cInfo.render_room(client, player, player.currentRoom)