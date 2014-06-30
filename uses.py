# uses.py
# describes functions that handle what happens when an item is used
import random
import Globals
import battleCommands

def heal(params):
	'''
	adds to a player's health
	'''


	client = params[0]
	playerAvatar = params[1]
	itemName = params[2]
	minHeal = int(params[3])
	maxHeal = int(params[4])

	if playerAvatar.kind.hp == playerAvatar.kind.maxHp:
		client.send_cc("I feel fine.  That would be a waste.\n")
		return False

	heal = random.randint(minHeal, maxHeal + 1)
	playerAvatar.kind.hp += heal
	if playerAvatar.kind.hp >= playerAvatar.kind.maxHp:
		heal -= playerAvatar.kind.hp - playerAvatar.kind.maxHp
		playerAvatar.kind.hp = playerAvatar.kind.maxHp


	client.send_cc("I feel a little bit better! ^G(+" + str(heal) + "hp)^~\n")

	if hasattr(Globals.CLIENT_DATA[playerAvatar.clientDataID], 'battleRoom'):
		if Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom != None:
			battleCommands.tickTurn(playerAvatar)

	return True


def attackMob(params):
	'''
	causes damage to a mob.  Only for use in a battle
	'''

	client = params[0]
	playerAvatar = params[1]
	itemName = params[2]
	minDamage = int(params[3])
	maxDamage = int(params[4])
	numTargets = int(params[5])
	soundEffect = params[6]

	targetList = []

	#checks that the player is in battle, or fails
	if hasattr(Globals.CLIENT_DATA[playerAvatar.clientDataID], 'battleRoom'):
		if Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom is None:
			client.send_cc("I can only use a " + itemName + " in battle!\n")
			return False
		else:
			client.send_cc(soundEffect + "\n")

			if numTargets == -1:
				numTargets = len(Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.mobs)

			for i in range(numTargets):
				targetMob = Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.mobs[random.randint(0,len(Globals.CLIENT_DATA[playerAvatar.clientDataID].battleRoom.mobs)-1)]
				targetList.append(targetMob)
				i += 1

			for mob in targetList:
				damage = random.randint(minDamage, maxDamage)
				mob.kind.hp -= damage
				soundTag = soundEffect
				for character in soundEffect:
					if character == '^':
						index = soundTag.find(character)
						print index
						#soundEffect.remove(character)
						soundTag = soundTag[:index] + soundTag[index+2:]
					print soundTag
				soundTagEle = soundTag.split("*")
				print soundTagEle
				soundTag = "\n*" + soundTagEle[1] + "* "
				print soundTag
				client.send_cc((" "*len(soundTag)) + "^W" +mob.name.capitalize() + "^~ takes ^W" + str(damage) + " damage.^~\n")

			battleCommands.tickTurn(playerAvatar)
			return True
	else:
		client.send_cc("I can only use a " + itemName + " in battle!\n")
		return False


