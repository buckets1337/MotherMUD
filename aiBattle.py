# aiBattle.py
# different modules to control mob behavior in battle
import random


def basicBash(playerAvatar, mob, room, CLIENT_DATA):
	'''
	just bashes the player until the mob or the player dies
	'''

	toHit = 80 + (mob.kind.speed - playerAvatar.kind.speed)
	hitRoll = random.randint(0,100)
	luckMod = int(mob.kind.luck/mob.kind.level)
	if luckMod < 0:
		luckMod = 0

	if hitRoll <= toHit:
		baseDamage = int((mob.kind.offense * ((random.randint(80,100) + luckMod)/100)) - (playerAvatar.kind.defense * (random.randint(100,(100+playerAvatar.kind.speed))/100)))
		damageMod = 0		# reserved for boosts from weapons later on
		damage = baseDamage + damageMod

		if damage <=0:		# if damage is 0 or less, you may still cause 1 damage sometimes
			hailMary = random.randint(0,4)
			if hailMary == 0:
				damage = 1
			else:
				damage = 0


		hurt = damage

	else:
		hurt = 'miss'


	return hurt