# battleCommands.py
# all player battle commands

import cInfo, Globals
import random

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

def mobsAttack(room, client, playerAvatar, target, mobLifeStatus):
	if mobLifeStatus == 'victory':
		return
	playerLifeStatus = ''
	for mob in room.mobs:
		hurt = mob.aiBattle(playerAvatar, target, room, Globals.CLIENT_DATA)
		if hurt != 'miss':
			client.send_cc("\n^Y*^Ublam^~^Y*^~ ^!" + mob.name.capitalize() + " hits^~ you for ^!" + str(hurt) + " damage^~.\n")
			playerAvatar.kind.hp -= hurt
		else:
			client.send_cc("\n^!" + mob.name.capitalize() + " missed^~ you!\n")
		playerLifeStatus = checkIfPlayerAlive(playerAvatar, mob)
	#client.send_cc("\n")
	if playerLifeStatus == 'dead':
		cInfo.render_room(playerAvatar.client, playerAvatar, playerAvatar.currentRoom, Globals.CLIENT_DATA)
		

	if playerLifeStatus != 'dead' and mobLifeStatus != 'victory':
		client.send_cc("______________________________________\n\n\n")
		cInfo.display_mobs(client, room, Globals.CLIENT_DATA, isBattle=True)
		client.send("\n\n")
		cInfo.display_player_status(client, room, Globals.CLIENT_DATA)
		cInfo.display_battle_commands(client, Globals.CLIENT_DATA)

def tickTurn(playerAvatar):
	'''
	advances combat 1 turn, causing the mobs to attack if they are still alive
	'''
	mobStatus = ''
	for mob in Globals.CLIENT_DATA[str(playerAvatar.client.addrport())].battleRoom.mobs:
		mobLifeStatus = checkIfMobAlive(mob, playerAvatar)
		if mobLifeStatus == 'victory':
			mobStatus = 'victory'
	mobsAttack(Globals.CLIENT_DATA[str(playerAvatar.client.addrport())].battleRoom, playerAvatar.client, playerAvatar, playerAvatar, mobStatus)

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
	speedMod = (playerAvatar.kind.speed - target.kind.speed)
	if speedMod <0:
		speedMod = int(speedMod/2)
	else:
		speedMod = int(speedMod*2)
	toHit = 80 + speedMod
	hitRoll = random.randint(0,100)
	luckMod = int(playerAvatar.kind.luck/playerAvatar.kind.level)
	if luckMod < 0:
		luckMod = 0

	if hitRoll <= toHit:
		baseDamage = int((playerAvatar.kind.offense * ((random.randint(80,120) + luckMod)/100)) - (target.kind.defense * (random.randint(50,100)/100)))
		damageMod = 0		# reserved for boosts from weapons later on
		damage = baseDamage + damageMod

		if damage <=0:		# if damage is 0 or less, you may still cause 1 damage sometimes
			hailMary = random.randint(0,4)
			if hailMary == 0:
				damage = 1
			else:
				damage = 0

		target.kind.hp -= damage

		sound = 'bonk'

		client.send_cc("\n^Y*^U" + sound + "^~^Y*^~ You ^!bash " + target.name + "^~ for ^!" + str(damage) + " damage^~.\n")


	else:
		client.send_cc("\nYou ^!missed %s^~!\n" %target.name)

	tickTurn(playerAvatar)


def identify(client, args, CLIENT_LIST, CLIENT_DATA):
	clientDataID = str(client.addrport())
	CLIENT_DATA[clientDataID].avatar.kind.pp -= 1
	cInfo.battleLook(client, [], CLIENT_LIST, CLIENT_DATA)






