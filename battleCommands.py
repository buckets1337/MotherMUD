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
					player.client.send_cc("^y" +mob.name + " arrived from battle.^~\n")

		playerAvatar.battleDeath(attackingMob)

		Globals.battleRooms.remove(playerAvatar.battleRoom)

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

	client.send_cc("\n^Y*^Ubonk^~^Y*^~ You ^!bash " + target.name + "^~ for ^!" + str(damage) + " damage^~.\n\n")

	mobLifeStatus = checkIfMobAlive(target, playerAvatar)


	#calculate damage dealt to player
	playerLifeStatus = ''
	for mob in room.mobs:
		hurt = mob.aiBattle(playerAvatar, target, room, CLIENT_DATA)
		playerAvatar.kind.hp -= hurt
		playerLifeStatus = checkIfPlayerAlive(playerAvatar, mob)

	if playerLifeStatus != 'dead' and mobLifeStatus != 'victory':
		cInfo.display_player_status(client, room, CLIENT_DATA)
		cInfo.display_battle_commands(client, CLIENT_DATA)

def identify(client, args, CLIENT_LIST, CLIENT_DATA):
	clientDataID = str(client.addrport())
	CLIENT_DATA[clientDataID].avatar.kind.pp -= 1
	cInfo.battleLook(client, [], CLIENT_LIST, CLIENT_DATA)