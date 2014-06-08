# battleCommands.py
# all player battle commands

import cInfo, Globals

def checkIfPlayerAlive(playerAvatar, attackingMob):
	'''
	check the player's hp.  If it is below zero, then run death routines
	'''
	if playerAvatar.kind.hp <= 0:
		for mob in Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.mobs:
			Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.mobs.remove(mob)
			Globals.regionListDict[Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.region][Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.name].mobs.append(mob)

			mob.currentRoom = Globals.regionListDict[Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.region][Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.name]

			Globals.MoveTIMERS.append(mob.aiMove.Timer)
			if mob.expirator.Timer is not None:
				Globals.TIMERS.append(mob.expirator.Timer)

			for player in Globals.regionListDict[Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.region][Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.name].players:
				if player != playerAvatar:
					player.client.send_cc("^y" +mob.name + ", finished with battle, seems to suddenly notice you.^~\n")

		print Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.name
		print Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.objects
		for obj in Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.objects:
			if obj.name.startswith("^r" + playerAvatar.name):
				Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo.objects.remove(obj)

		playerAvatar.battleDeath(attackingMob)

		Globals.battleRooms.remove(Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom)

		label = str(Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.region)+str(Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.name)
		if label in Globals.masterRooms:
			del Globals.masterRooms[label]

		
		Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.attachedTo = None
		Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom = None
		Globals.CLIENT_DATA[playerAvatar.clientDataID].gameState = 'normal'

		#cInfo.render_room(playerAvatar.client, playerAvatar, playerAvatar.currentRoom, Globals.CLIENT_DATA)

		#Globals.regionListDict[playerAvatar.currentRoom.region][playerAvatar.currentRoom.name].objects.remove()

		return 'dead'

def checkIfMobAlive(mob, attackingPlayer):
	if mob.kind.hp <= 0:
		mob.battleDeath(attackingPlayer)

		if Globals.CLIENT_DATA[attackingPlayer.clientDataID].battleRoom.mobs == []:
			attackingPlayer.battleWin()
			return 'victory'

		return 'dead'


#--------------------------------------------------------------------------

def bash(client, args, CLIENT_LIST, CLIENT_DATA):
	'''
	whack the baddie with your weapon, or fists
	'''
	clientDataID = str(client.addrport())
	playerAvatar = CLIENT_DATA[clientDataID].avatar
	room = CLIENT_DATA[clientDataID].battleRoom
	if args == []:
		target = room.mobs[0]
	else:
		for mob in room.mobs:
			if mob.name == args[0]:
				target = mob

	#calculate damage dealt to mob
	damage = 1

	target.kind.hp -= damage

	client.send_cc("\n^Y*^Ubonk^~^Y*^~ You ^!bash " + target.name + "^~ for ^!" + str(damage) + " damage^~.\n")

	mobLifeStatus = checkIfMobAlive(target, playerAvatar)


	#calculate damage dealt to player
	playerLifeStatus = ''
	for mob in room.mobs:
		hurt = mob.aiBattle(playerAvatar, target, room, CLIENT_DATA)
		client.send_cc("\n^Y*^Ublam^~^Y*^~ ^!" + mob.name.capitalize() + " hits^~ you for ^!" + str(hurt) + " damage^~.\n")
		playerAvatar.kind.hp -= hurt
		playerLifeStatus = checkIfPlayerAlive(playerAvatar, mob)
	#client.send_cc("\n")
	if playerLifeStatus == 'dead':
		cInfo.render_room(playerAvatar.client, playerAvatar, playerAvatar.currentRoom, Globals.CLIENT_DATA)
		

	if playerLifeStatus != 'dead' and mobLifeStatus != 'victory':
		client.send_cc("______________________________________\n\n\n")
		cInfo.display_mobs(client, room, CLIENT_DATA, isBattle=True)
		client.send("\n\n")
		cInfo.display_player_status(client, room, CLIENT_DATA)
		cInfo.display_battle_commands(client, CLIENT_DATA)

def identify(client, args, CLIENT_LIST, CLIENT_DATA):
	clientDataID = str(client.addrport())
	CLIENT_DATA[clientDataID].avatar.kind.pp -= 1
	cInfo.battleLook(client, [], CLIENT_LIST, CLIENT_DATA)