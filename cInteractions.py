# cInteractions
# handles various commands that modify the world in some manner

import World, Globals, Rooms, cInfo
import uses

def get(client, args, clientDataID, CLIENT_DATA, currentRoom):
	# targetsList = []
	# if len(args) > 0:
	# 	poppedList = args.pop()
	# else:
	# 	poppedList = args

	objectFound = False
	resultsList = []
	if len(args) == 0:
		client.send("What did you want to pick up?\n")
		return

	if len(CLIENT_DATA[clientDataID].avatar.kind.inventory) >= CLIENT_DATA[clientDataID].avatar.kind.inventorySize:
		client.send("I have no more space in my inventory. I should drop something first.\n")
		return

	for obj in CLIENT_DATA[clientDataID].avatar.currentRoom.objects:
		# print obj.name
		# print 'argstr = ' + (" ".join(args))
		# print args

		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)


		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
				# print obj.name
				# print 'argstr = ' + (" ".join(args))
				# print args
					# for x in range(len(args[1:])):
					if len(args) == 1:
						if ob.name == args[-1]:
							resultsList.append(ob)

					if len(args) > 1:
						if ob.name == args[-2]:
							resultsList.append(ob)


							# if obj.kind is not None and obj.kind.itemGrabHandler is not None:
							# 	obj.kind.itemGrabHandler.get(client, CLIENT_DATA[clientDataID].avatar)
							# else:
							# 	client.send("The '%s' appears to be stuck in the '%s'.\n" %(obj.name, obj.owner.name))
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	for obj in CLIENT_DATA[clientDataID].avatar.currentRoom.equipment:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)


	#print "resultsList:"+str(resultsList)
	if len(resultsList) == 1:
		#print 'len resultsList = 1'
		#print resultsList[0]
		#print resultsList[0].kind
		#print resultsList[0].kind.itemGrabHandler
		if resultsList[0].kind is not None and resultsList[0].kind.itemGrabHandler is not None and hasattr(resultsList[0],'kind') and hasattr(resultsList[0].kind,'itemGrabHandler'):
			resultsList[0].kind.itemGrabHandler.get(client, CLIENT_DATA[clientDataID].avatar)
			objectFound = True
		else:
			client.send("*sigh* Why would I want to take the '%s'?\n" %resultsList[0].name)
			objectFound = True

	if len(resultsList) > 1:
		#print resultsList
		index = 1
		# use the last argument as an int to find the proper item to get
		if len(args) > 1:
			index = args[-1]
			#print "index " + str(index)
		try:
			if int(index) > len(resultsList):
				#print "index:" + str(index) + " len:" + str(len(resultsList))
				client.send("I don't see a '%s'. It seems like I understand the names of things better when I 'examine' them!\n" %(" ".join(args)))
				return

			else:
				#print "final"

				if resultsList[int(index) - 1].kind is not None and resultsList[int(index) - 1].kind.itemGrabHandler is not None:
					resultsList[int(index) - 1].kind.itemGrabHandler.get(client, CLIENT_DATA[clientDataID].avatar)
					objectFound = True
				else:
					client.send("*sigh* Why would I want to take the '%s'?\n" %resultsList[int(index) - 1].name)
					objectFound = True

		except ValueError:
			client.send("Object index must be an integer!\n")

	if objectFound == False:
		client.send("I don't see a '%s'. It seems like I understand the names of things better when I 'examine' them!\n" %(" ".join(args)))
		# 	targetsList.append(obj)
		# elif obj.name == str( ' '.join(poppedList) ):
		# 	pass
			# create a sub-list of all objects with that name, and select the object at the index position identified by the last argument, and add it to the targetsList, minus the last argument
			


	# if len(targetsList) > 1:
	# 	counter = 1
	# 	client.send("Pick which item by adding it's number below to the end of the 'get' command.\n\n")
	# 	for obj in targetsList:
	# 		client.send("[%s]    %s" %(counter, obj.name))

	# elif len(targetsList) == 1:
	# 	CLIENT_DATA[clientDataID].avatar.kind.inventory.append(targetsList[0])		# should be done with the item's 'get'
	# 	CLIENT_DATA[clientDataID].avatar.currentRoom.objects.remove(targetsList[0])	# see above.

	# 	client.send("You picked up '%s'.\n" %targetsList[0].name)

	# else:
	# 	client.send("Target not found.\n")


def drop(client, args, clientDataID, CLIENT_DATA, currentRoom):
	# drop items from inventory
	inventory = CLIENT_DATA[clientDataID].avatar.kind.inventory



	resultsList = []
	found = False

	if args != []:
		for item in inventory:
			if item.name == args[0]:
				resultsList.append(item)

			if item.name == args[0] and item.kind.itemGrabHandler.notDroppable == True:
				client.send("I get the feeling I shouldn't drop %s.  I have decided to keep it.\n" %item.name)
				return

	if len(args) == 0:
		client.send("What did I want to drop?\n")
		return

	if resultsList == []:
		client.send("There is not a single '%s' on my person.\n" %args[0])
		return


	if len(args) == 1:
		if len(resultsList) > 1:
			client.send("I have more than one %s. Which one did I want to drop?\n" %str(args[0]))
			found = True
		else:
			if resultsList[0].name == args[0]:
				inventory.remove(resultsList[0])
				client.send("I dropped %s.  %s is gone.\n" %(resultsList[0].name, resultsList[0].name.capitalize()))
				found = True
			else:
				client.send("I don't see a %s in my bags.\n" %args[0])
				found = True


	if len(args) > 1:
		try:
			selector = int(args[1])
			print "sel" + str(selector)
		except ValueError:
			client.send("I don't know which %s '%s' is.\n"%(resultsList[0].name, args[1]))
			found = True
			return

		if len(resultsList) >= (selector):
			selected = resultsList[selector - 1]
			inventory.remove(selected)
			client.send("I dropped %s.  %s is gone.\n" %(selected.name, selected.name.capitalize()))
			found = True
			return

		client.send("I only have %i '%s'.\n" %(len(resultsList), args[0]))
		found = True



	if found == False:
		client.send("I have nothing to drop!\n")


def use(client, args, CLIENT_LIST, clientDataID, CLIENT_DATA, currentRoom):
	'''
	use an item in the player's inventory, causing some effect as defined in uses.py 
	'''
	playerAvatar = CLIENT_DATA[clientDataID].avatar

	possibles = []

	if len(args) == 0:
		client.send("What did I want to use?\n")
		return

	for item in playerAvatar.kind.inventory:
		if item.name == args[0]:
			possibles.append(item)

	for item in possibles:
		#print item.kind.onUse
		if item.kind.onUse != None:
			if item.kind.onUse.endswith(")"):
				params = item.kind.onUse.split("(")
				params = params[1]
				params = params[:-1]
				params = params.split(",")
				paramsList = []
				paramsList.append(client)
				paramsList.append(playerAvatar)
				paramsList.append(item.name)

				paramsList += params
				# print params
				# print paramsList
				item.kind.useParams = paramsList
			else:
				item.kind.useParams = None

			# This is where each of the things that can happen when an item is used are defined and plugged into the appropriate function in uses.py
			if item.kind.onUse.startswith("heal"):
				item.kind.useFunction = uses.heal
			elif item.kind.onUse.startswith("attackMob"):
				item.kind.useFunction = uses.attackMob


			else:
				item.kind.useFunction = None
		else:
			item.kind.useFunction = None
			item.kind.useParams = None

	if len(args) == 1:
		if len(possibles) == 0:
			client.send("I don't have a " + args[0] + "!\n")
		else:
			result = possibles[0].kind.useFunction(possibles[0].kind.useParams)
			if result == True:
				playerAvatar.kind.inventory.remove(possibles[0])


	if len(args) >= 2:
		if not args[1].isdigit():
			client.send(args[1] + " doesn't appear to distinguish an item from the others.\n")
			return
		if len(possibles) == 0:
			client.send("I don't have a " + args[0] + "to use!\n")
			return
		else:
			if len(possibles) < int(args[1]):
				client.send("You only have " + str(len(possibles)) + " " + args[0] + "!\n")
				return
			else:
				params = possibles[int(args[1])-1].kind.useParams
				remainingArgs = args[2:]
				for arg in remainingArgs:
					params.append(arg)
				result = possibles[int(args[1])-1].kind.useFunction(params)
				if result == True:
					playerAvatar.kind.inventory.remove(possibles[int(args[1])-1])


def equip(client, args, CLIENT_LIST, clientDataID, CLIENT_DATA):
	gear = None
	gearType = None

	if args == [] or args == [''] or args == [None]:
		client.send("What did I want to equip?\n")
		return

	#print CLIENT_DATA[clientDataID].avatar.kind.inventory
	for item in CLIENT_DATA[clientDataID].avatar.kind.inventory:
		if item.name == args[0]:
			if hasattr(item.kind, 'equipment'):
				gear = item
				if hasattr(item.kind.equipment, 'weapon'):
					if item.kind.equipment.weapon != None:
						gearType = 'weapon'
				if hasattr(item.kind.equipment, 'armor'):
					if item.kind.equipment.armor != None:
						gearType = 'armor'
		elif str(item.ID) == args[0]:
			if hasattr(item.kind, 'equipment'):
				gear = item
				if hasattr(item.kind.equipment, 'weapon'):
					if item.kind.equipment.weapon != None:
						gearType = 'weapon'
				if hasattr(item.kind.equipment, 'armor'):
					if item.kind.equipment.armor != None:
						gearType = 'armor'

	if gear == None:
		client.send("I don't seem to have %s.\n" %(args[0]))
		return

	else:
		slot = gear.kind.equipment.slot

		if slot == 'both hands' and ('main hand' in CLIENT_DATA[clientDataID].avatar.kind.equipment or 'off hand' in CLIENT_DATA[clientDataID].avatar.kind.equipment):
			client.send("I am already holding a weapon, and %s requires both hands.\n" %gear.name)
			return

		if slot == 'main hand' and 'both hands' in CLIENT_DATA[clientDataID].avatar.kind.equipment:
			client.sent("I am already holding a weapon, and I must hold %s in my main hand.\n" %gear.name)
			return

		if slot not in CLIENT_DATA[clientDataID].avatar.kind.equipment:
			CLIENT_DATA[clientDataID].avatar.kind.equipment[slot] = gear
			CLIENT_DATA[clientDataID].avatar.kind.hp += gear.kind.equipment.hp
			CLIENT_DATA[clientDataID].avatar.kind.maxHp += gear.kind.equipment.hp
			CLIENT_DATA[clientDataID].avatar.kind.pp += gear.kind.equipment.pp
			CLIENT_DATA[clientDataID].avatar.kind.maxPp += gear.kind.equipment.pp
			CLIENT_DATA[clientDataID].avatar.kind.offense += gear.kind.equipment.offense
			CLIENT_DATA[clientDataID].avatar.kind.defense += gear.kind.equipment.defense
			CLIENT_DATA[clientDataID].avatar.kind.speed += gear.kind.equipment.speed
			CLIENT_DATA[clientDataID].avatar.kind.guts += gear.kind.equipment.guts
			CLIENT_DATA[clientDataID].avatar.kind.luck += gear.kind.equipment.luck
			CLIENT_DATA[clientDataID].avatar.kind.vitality += gear.kind.equipment.vitality
			CLIENT_DATA[clientDataID].avatar.kind.IQ += gear.kind.equipment.IQ

		else:
			if gearType == 'weapon':
				if slot != 'both hands':
					client.send("I am already holding a weapon in my %s.\n" %slot)
					return
				else:
					client.send("I am already holding a weapon that requires both my hands!\n")
			elif gearType == 'armor':
				client.send("I am already wearing " + str(CLIENT_DATA[clientDataID].avatar.kind.equipment[slot].name) + " on my " + slot + ".\n")

	if gearType == 'weapon':
		client.send("I hold the %s in my %s.\n" %(gear.name,str(slot)))
	elif gearType == 'armor':
		client.send("I put the %s on my %s.\n" %(gear.name,str(slot)))


def remove(client, args, CLIENT_LIST, clientDataID, CLIENT_DATA):
	player = CLIENT_DATA[clientDataID].avatar

	if args == [] or args == [''] or args == [None]:
		client.send("What did I want to remove?\n")
		return

	elif len(args) == 1:
		resultsList = []
		for item in player.kind.equipment:
			if player.kind.equipment[item].name == str(args[0]):
				resultsList.append(player.kind.equipment[item])

		if resultsList == []:
			client.send("I do not have %s equipped.\n" %args[0])

		else:
			eq = resultsList[0].kind.equipment

			player.kind.hp -= eq.hp
			player.kind.maxHp -= eq.hp
			player.kind.pp -= eq.pp
			player.kind.maxPp -= eq.pp
			player.kind.offense -= eq.offense
			player.kind.defense -= eq.defense
			player.kind.speed -= eq.speed
			player.kind.guts -= eq.guts
			player.kind.luck -= eq.luck
			player.kind.vitality -= eq.vitality
			player.kind.IQ -= eq.IQ

			del player.kind.equipment[eq.slot]
			client.send("I removed the %s.\n" %args[0])

	else:
		resultsList = []
		for item in player.kind.equipment:
			if player.kind.equipment[item].name == str(args[0]) and player.kind.equipment[item].slot == str(args[1]):
				resultsList.append(player.kind.equipment[item])

		if resultsList == []:
			client.send("I do not have a '%s' equipped on my '%s'.\n" %(args[0], args[1]))

		else:
			eq = resultsList[0].kind.equipment

			player.kind.hp -= eq.hp
			player.kind.maxHp -= eq.hp
			player.kind.pp -= eq.pp
			player.kind.maxPp -= eq.pp
			player.kind.offense -= eq.offense
			player.kind.defense -= eq.defense
			player.kind.speed -= eq.speed
			player.kind.guts -= eq.guts
			player.kind.luck -= eq.luck
			player.kind.vitality -= eq.vitality
			player.kind.IQ -= eq.IQ

			del player.kind.equipment[eq.slot]
			client.send("I removed the %s from my %s.\n" %(args[0], args[1]))




def check(client, args, clientDataID, CLIENT_DATA, room):
	'''
	get all items from the container named in args
	'''
	if len(args)== 0:
		client.send("Nothing unusual here.\n")

	resultsList = []
	pickups = []
	notContainer = False
	for obj in room.objects:
		if hasattr(obj, 'kind') and isinstance(obj.kind, World.container):
			if obj.name == args[0]:
				resultsList.append(obj)
		else:
			if obj.name == args[0]:
				notContainer = True

	if len(resultsList) == 0 and notContainer == False:
		client.send("It is difficult to check the " + args[0] + " when I can't find it.\n")
	elif len(resultsList) == 0 and notContainer == True:
		client.send("I couldn't figure out how to get the " + args[0] + " open.\n")

	elif len(resultsList) == 1:
		if resultsList[0].kind.isLocked == False:
			for obj in resultsList[0].kind.inventory:
				pickups.append(obj)
			if len(pickups) == 0:
				client.send("The " + resultsList[0].name + " is empty.\n")
				return
			for thing in pickups:
				#print CLIENT_DATA[clientDataID]
				if len(CLIENT_DATA[clientDataID].avatar.kind.inventory) < CLIENT_DATA[clientDataID].avatar.kind.inventorySize:
					CLIENT_DATA[clientDataID].avatar.kind.inventory.append(thing)
					resultsList[0].kind.inventory.remove(thing)
					client.send("I got a " +thing.name + " from the " + resultsList[0].name + "!\n")
				else:
					client.send("I was unable to get the " + thing.name + " from the " + resultsList[0].name + " because I couldn't carry any more.\n")
		else:
			client.send("The " + args[0] + " is locked.\n")

	elif len(resultsList) > 1:
		#print "resList:" + str(resultsList)
		if len(args) < 2:
			client.send("You see more than one " + args[0] + " here.  Which one did you want to check?\n")
		elif len(args) == 2:
			index = int(args[1]) - 1
			if index > len(resultsList) - 1:
				client.send("You only see " +str(len(resultsList))+ " " +str(resultsList[0].name) +" here.\n")
				return
			#print index
			result = resultsList[index]
			#print result
			#print result.kind.isLocked
			if result.kind.isLocked == False:
				for obj in result.kind.inventory:
					#print obj
					pickups.append(obj)		
				#print pickups	
			else:
				client.send("The " + args[0] + " is locked.\n")
			for thing in pickups:
				if len(CLIENT_DATA[clientDataID].avatar.kind.inventory) <= CLIENT_DATA[clientDataID].avatar.kind.inventorySize:
					CLIENT_DATA[clientDataID].avatar.kind.inventory.append(thing)
					result.kind.inventory.remove(thing)
					client.send("I found a " + thing.name + " in the " + result.name + "!\n")
				else:
					client.send("I was unable to get the " + thing.name + " from the " + obj.name + " because I couldn't carry any more.\n")
			if pickups == []:
				client.send("The " + args[0] + " is empty.\n")
		elif len(args) > 2:
			client.send("I got confused about what I wanted to check.  Maybe I will remember if I repeat it to myself like this: 'check <object_name> <index>\n")

		else:
			print "end"


def startBattle(client, args, clientDataID, CLIENT_DATA, room):
	if len(args) == 0:
		client.send_cc("Who do I want to fight?\n")
		return False

	playerAvatar = CLIENT_DATA[clientDataID].avatar
	#print playerAvatar
	mobToBattle = None

	mobList = []
	for mob in room.mobs:
		if args[0] == mob.name:
			mobList.append(mob)

	if len(args) == 1:
		if len(mobList) != 0:
			mobToBattle = mobList[0]
		else:
			client.send_cc("I don't see a %s.\n" %args[0])
			return False

	elif len(args) == 2:
		if int(args[1]) > len(args):
			client.send_cc("I don't see %s %s(s) here!\n" %(args[1], args[0]))
			return False
		else:
			mobToBattle = mobList[int(args[1])-1]

	room.players.remove(playerAvatar)
	room.mobs.remove(mobToBattle)

	roomCount = 0
	battleRoomName = 'Battle@' + room.name
	for battleRoom in Globals.battleRooms:
		if battleRoom.name == battleRoomName:
			roomCount += 1
	if roomCount > 0:
		battleRoomName = 'Battle@' + room.name + "(" + str(roomCount+1) + ")"

	playerAvatarName = playerAvatar.name

	battleRoomDescription = '^RA battle between ' + playerAvatarName + ' and a ' + mobToBattle.name + '.^c'
	battleRoomLongDescription = playerAvatarName.capitalize() + ' is ferociously fighting a ' + mobToBattle.name + ' here.'

	battleRoom = World.Room(region='battles', name=battleRoomName, description=battleRoomDescription, longDescription=battleRoomLongDescription, players=[playerAvatar], objects=[], mobs=[mobToBattle])
	battleRoom.attachedTo = room

	Rooms.master['battles'+battleRoomName] = battleRoom
	playerAvatar.currentRoom = battleRoom
	CLIENT_DATA[clientDataID].battleRoom = battleRoom
	mobToBattle.currentRoom = battleRoom
	Globals.MoveTIMERS.remove(mobToBattle.aiMove.Timer)
	if mobToBattle.expirator != None:
		if mobToBattle.expirator.Timer in Globals.TIMERS:
			Globals.TIMERS.remove(mobToBattle.expirator.Timer)
	Globals.battleRooms.append(battleRoom)

	for player in room.players:
		if CLIENT_DATA[player.clientDataID].gameState != 'battle':
			CLIENT_DATA[player.clientDataID].client.send_cc("^r%s and %s began fighting.^~\n" %(playerAvatar.name.capitalize(), mobToBattle.name))

	battleObjectName = "^r" +playerAvatar.name + "_vs_" + mobToBattle.name + "^c"
	battleObject = World.Object(name=battleObjectName, description=battleRoomDescription, currentRoom=room, isVisible=True, longDescription=battleRoomLongDescription)
	room.objects.append(battleObject)

	print "+B " + str(playerAvatar) +  " " + str(playerAvatar.name) + " vs. " + str(mobToBattle.name) + " @ [" + room.region + ":" + room.name + "]" 

	cInfo.battleLook(client, [], Globals.CLIENT_LIST, CLIENT_DATA)
	return True


def stopBattle(battleRoom):
	'''
	ends a battle in progress, returning the mobs and the player to the room they came from
	'''
	for mob in battleRoom.mobs:
		battleRoom.mobs.remove(mob)
		battleRoom.attachedTo.mobs.append(mob)
		mob.currentRoom = battleRoom.attachedTo
		Globals.MoveTIMERS.append(mob.aiMove.Timer)
		if mob.expirator.Timer is not None:
			Globals.TIMERS.append(mob.expirator.Timer)
		for player in mob.currentRoom.players:
			player.client.send_cc("^R" + mob.name + " has arrived from battle.^~\n")

	for player in battleRoom.players:
		battleRoom.players.remove(player)
		battleRoom.attachedTo.players.append(player)
		player.currentRoom = battleRoom.attachedTo
		player.battleRoom = None
		for obj in battleRoom.attachedTo.objects:
			if obj.name.startswith('^r'+player.name):
				battleRoom.attachedTo.objects.remove(obj)
		Globals.CLIENT_DATA[str(player.client.addrport())].gameState = 'normal'
		cInfo.render_room(player.client, player, battleRoom.attachedTo, Globals.CLIENT_DATA)
		alert(player.client, Globals.CLIENT_DATA, ("^g^!%s has arrived from battle.^~\n" %player.name))




	Globals.battleRooms.remove(battleRoom)
	label = str(battleRoom.region)+str(battleRoom.name)
	if label in Globals.masterRooms:
		del Globals.masterRooms[label]

	print "-B " + str(player) + " " + player.name + " (flee)"


def alert(client, CLIENT_DATA, messageString):
	"""
	Lets other players know about movement into or out of a room
	"""
	
	clientDataID = str(client.addrport())
	player = CLIENT_DATA[clientDataID].avatar
	for guest in player.currentRoom.players:
		if player.currentRoom == guest.currentRoom and player != guest:
			guest.client.send_cc(messageString)