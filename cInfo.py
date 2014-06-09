# cInfo.py

"""
This file describes all the commands used to gather more information about the environment
"""

import Rooms, World


def who(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Displays all players currently online
	"""

	client.send_cc("\n^I[ Players Online ]^~\n\n")
	for player in CLIENT_LIST:
		clientDataID = str(player.addrport())
		name = CLIENT_DATA[clientDataID].name
		if name != CLIENT_DATA[client.addrport()].name:
			client.send_cc("%s, %s\n" %(name, CLIENT_DATA[player.addrport()].avatar.title))
		else:
			client.send_cc("^!%s, %s (you)^~\n" %(CLIENT_DATA[client.addrport()].name, CLIENT_DATA[client.addrport()].avatar.title))
	if len(CLIENT_LIST) > 1:
		client.send("\n%s players online.\n\n" %len(CLIENT_LIST))
	elif len(CLIENT_LIST) == 1:
		client.send("\n%s player online.\n\n" %len(CLIENT_LIST))


def look(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Gives more information about the room.  Without arguments, it displays description of the room.  With an argument, it displays the description of whatever item is named by the arguments
	"""
	clientDataID = str(client.addrport())
	looked = False
	objectList = []
	inventory = False
	#print args

	if args == []:
		client.send_cc("\n^I[ %s ]^~\n" %CLIENT_DATA[clientDataID].avatar.currentRoom.name)
		display_description(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_objects(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_mobs(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_other_players(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_exits(client, CLIENT_DATA[clientDataID].avatar.currentRoom)
		looked = True

	elif args[0] == 'inventory' or args[0] == 'i':
		#print args[0]
		args = args[1:]
		inventory = True

	elif args[0] == 'harder':
		examine(client, ['lh'], CLIENT_LIST, CLIENT_DATA)
		return

	# handle looking at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory

	resultsList = []

	for obj in objectList:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)
			#print resultsList

		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
					if len(args) > 0:
						if args[-1] == ob.name: 
							resultsList.append(ob)
					elif len(args) > 1:
						if args[-2] == ob.name:
							resultsList.append(ob)
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	if len(resultsList) > 1:
		#print "args " + str(args)
		#print "arglen " + str(len(args))

		if len(args) >= 2:

			# numlist = [(x in range(0,99))]
			# if args[2] in numlist:
			try:
				if len(resultsList) >= int(args[1]):
					client.send_cc("^c%s^~\n" %resultsList[int(args[1]) - 1].description)
					looked = True

					if isinstance(resultsList[int(args[1]) - 1].kind, World.container):
						for ob in resultsList[int(args[1]) - 1].kind.inventory:
							# if ob.name == " ".join(args):
							client.send_cc("^c[In %s]: %s^~\n" %(resultsList[int(args[1]) - 1].name, ob.description))
			except ValueError:
				client.send("Object index must be an integer! I mean, it only makes sense.  Duh.\n")

		else:
			#print resultsList
			for obj in objectList:
				if obj.name == "_".join(args):
					client.send_cc("^c%s^~\n" %obj.description)
					looked = True
					

					if isinstance(obj.kind, World.container):
						for ob in resultsList[obj].kind.inventory:
							if ob.name == " ".join(args):
								client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))

	elif len(resultsList) == 1:
		#print resultsList
		for obj in resultsList:
			# if obj.name == "_".join(args):
			client.send_cc("^c%s^~\n" %obj.description)
			looked = True
			

			if isinstance(obj.kind, World.container):
				for ob in obj.kind.inventory:
					if ob.name == "_".join(args):
						client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))


	# handle looking at a player

	# handle looking at a mob



	if looked == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I like to 'look harder' to help me with the names of things!\n" %(" ".join(args)))
		else:
			client.send("You didn't say what you want to look at.\n")


def battleLook(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Gives more information about the room.  Without arguments, it displays description of the room.  With an argument, it displays the description of whatever item is named by the arguments
	"""
	clientDataID = str(client.addrport())
	looked = False
	objectList = []
	inventory = False
	#print args

	if args == []:
		client.send_cc("\n^I[ %s ]^~\n" %CLIENT_DATA[clientDataID].avatar.currentRoom.name)
		display_description(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_mobs(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA, isBattle=True)
		client.send("\n")
		display_other_players(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		client.send("\n")
		display_player_status(client, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA)
		display_battle_commands(client, CLIENT_DATA)
		looked = True

	elif args[0] == 'inventory' or args[0] == 'i':
		#print args[0]
		args = args[1:]
		inventory = True

	elif args[0] == 'harder':
		battleExamine(client, ['lh'], CLIENT_LIST, CLIENT_DATA)
		return

	# handle looking at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory

	resultsList = []

	for obj in objectList:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)
			#print resultsList

		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
					if len(args) > 0:
						if args[-1] == ob.name: 
							resultsList.append(ob)
					elif len(args) > 1:
						if args[-2] == ob.name:
							resultsList.append(ob)
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	if len(resultsList) > 1:
		#print "args " + str(args)
		#print "arglen " + str(len(args))

		if len(args) >= 2:

			# numlist = [(x in range(0,99))]
			# if args[2] in numlist:
			try:
				if len(resultsList) >= int(args[1]):
					client.send_cc("^c%s^~\n" %resultsList[int(args[1]) - 1].description)
					looked = True

					if isinstance(resultsList[int(args[1]) - 1].kind, World.container):
						for ob in resultsList[int(args[1]) - 1].kind.inventory:
							# if ob.name == " ".join(args):
							client.send_cc("^c[In %s]: %s^~\n" %(resultsList[int(args[1]) - 1].name, ob.description))
			except ValueError:
				client.send("Object index must be an integer! I mean, it only makes sense.  Duh.\n")

		else:
			#print resultsList
			for obj in objectList:
				if obj.name == "_".join(args):
					client.send_cc("^c%s^~\n" %obj.description)
					looked = True
					

					if isinstance(obj.kind, World.container):
						for ob in resultsList[obj].kind.inventory:
							if ob.name == " ".join(args):
								client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))

	elif len(resultsList) == 1:
		#print resultsList
		for obj in resultsList:
			# if obj.name == "_".join(args):
			client.send_cc("^c%s^~\n" %obj.description)
			looked = True
			

			if isinstance(obj.kind, World.container):
				for ob in obj.kind.inventory:
					if ob.name == "_".join(args):
						client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.description))


	# handle looking at a player

	# handle looking at a mob



	if looked == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I like to 'look harder' to help me with the names of things!\n" %(" ".join(args)))
		else:
			client.send("You didn't say what you want to look at.\n")


def examine(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	More detailed info than look.  Without arguments, it shows the long description of the current room.  With arguments, it shows the long description of the item that is named by the arguments
	"""
	clientDataID = str(client.addrport())
	objectList = []
	examined = False
	inventory = False

	if args == []:
		# examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		client.send("What did I want to examine again?\n")
		examined = True


	elif args[0] == 'inventory' or args[0] == 'i':
		#print args[0]
		args = args[1:]
		inventory = True

	elif args[0] == 'lh':
		examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		args.pop(0)
		examined = True

	# handle examining at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory


	resultsList = []

	for obj in objectList:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)
			#print resultsList
		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
					if len(args) > 0:
						if args[-1] == ob.name: 
							resultsList.append(ob)
					elif len(args) > 1:
						if args[-2] == ob.name:
							resultsList.append(ob)
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	if len(resultsList) > 1:
		# print "args " + str(args)
		# print "arglen " + str(len(args))

		if len(args) >= 2:

			# numlist = []
			# for x in range(99):
			# 	numlist.append(x)
			# if args[1] in numlist:
			try:
				if len(resultsList) >= int(args[-1]):
					client.send_cc("^c%s^~\n" %resultsList[int(args[-1]) - 1].longDescription)
					examined = True

					if isinstance(resultsList[int(args[-1]) - 1].kind, World.container):
						#print"has inv"
						#print "isLocked: " + str(resultsList[int(args[-1]) - 1].kind.isLocked)
						if resultsList[int(args[-1]) - 1].kind.isLocked == False:
							for ob in resultsList[int(args[-1]) - 1].kind.inventory:
								# if ob.name == "_".join(args):
								client.send_cc("^c[In %s]: %s^~\n" %(resultsList[int(args[1]) - 1].name, ob.name))
							if resultsList[int(args[-1]) - 1].kind.inventory == []:
								client.send_cc("^c[In %s]:^~\n" %resultsList[int(args[1]) - 1].name)
						else:
							client.send_cc("^cThe %s is locked.^~\n" %resultsList[int(args[1]) - 1].name)
			except ValueError:
				client.send("Object index must be an integer! My mother always said!\n")

			# for obj in resultsList:
			# 	if args[-1] == obj.name or args[-2] == obj.name:
			# 		examine(client, [obj.name], CLIENT_LIST, CLIENT_DATA)
					


		else:
			#print resultsList
			for obj in resultsList:
				# if obj.name == "_".join(args):
				client.send_cc("^c%s^~\n" %obj.longDescription)
				examined = True

				if isinstance(obj.kind, World.container):
					#print "*******"
					if obj.kind.isLocked == False:
						for ob in obj.kind.inventory:
							#print ob.name,
							client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.name))
						if obj.kind.inventory == []:
							client.send_cc("^c[In %s]:^~\n" %obj.name)
					else:
						client.send_cc("^cThe %s is locked.^~\n" %obj.name)	



	elif len(resultsList) == 1:
		#print resultsList
		for obj in resultsList:
			#print "result: " + str(obj)
			client.send_cc("^c%s^~\n" %obj.longDescription)
			examined = True

			#print obj.kind
			#print 'ob.inv: ' + str(obj.kind.inventory)

			if hasattr(obj.kind, 'inventory'):
				#print"&&&&&&&&&&&&&&"
				if obj.kind.isLocked == False:
					for ob in obj.kind.inventory:
						client.send_cc("^c[In %s]: A %s^~\n" %(obj.name, ob.name))
					if obj.kind.inventory == []:
						client.send_cc("^c[In %s]:^~\n" %obj.name)
				else:
					client.send_cc("^cThe %s is locked.^~\n" %obj.name)					





	# for obj in objectList:
	# 	if obj.name == "_".join(args):
	# 		client.send_cc("^c%s^~\n" %obj.longDescription)
	# 		examined = True

	# 		if isinstance(obj.kind, World.container):	# is a container, display the inventory
	# 			client.send_cc("^c^UContents^u: ")
	# 			for ob in obj.kind.inventory:
	# 				if len(obj.kind.inventory) == 1:
	# 					client.send_cc( "%s " %ob.name)
	# 				else:
	# 					client.send_cc( "%s, " %ob.name)
	# 			client.send_cc("^~\n")

	# 	elif isinstance(obj.kind, World.container):		# check container inventory for argument
	# 		for ob in obj.kind.inventory:
	# 			if ob.name == " ".join(args):
	# 				client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.longDescription))
	# 				examined = True

	# handle examining a player

	# handle examining a mob



	if examined == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I seem to recall the names of things better when I 'look harder'!\n" %(" ".join(args)))
		else:
			client.send("I am not sure what I wanted to examine.\n")


def battleExamine(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	More detailed info than look.  Without arguments, it shows the long description of the current room.  With arguments, it shows the long description of the item that is named by the arguments
	"""
	clientDataID = str(client.addrport())
	objectList = []
	examined = False
	inventory = False

	if args == []:
		# examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		client.send("What did I want to examine again?\n")
		examined = True


	elif args[0] == 'inventory' or args[0] == 'i':
		#print args[0]
		args = args[1:]
		inventory = True

	elif args[0] == 'lh':
		battle_examine_room(client, CLIENT_DATA[clientDataID].avatar, CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA )
		args.pop(0)
		examined = True

	# handle examining at an object
	if inventory == False:
		objectList = CLIENT_DATA[clientDataID].avatar.currentRoom.objects
	else:
		objectList = CLIENT_DATA[clientDataID].avatar.kind.inventory


	resultsList = []

	for obj in objectList:
		if obj.name == "_".join(args) or obj.name == "_".join(args[:-1]) or obj.name == "_".join(args[:-2]):
			resultsList.append(obj)
			#print resultsList
		elif isinstance(obj.kind, World.container):
			if obj.kind.isLocked == False:
				for ob in obj.kind.inventory:
					if len(args) > 0:
						if args[-1] == ob.name: 
							resultsList.append(ob)
					elif len(args) > 1:
						if args[-2] == ob.name:
							resultsList.append(ob)
			# else:
			# 	client.send("The %s is locked!\n" %obj.name)
			# 	return

	if len(resultsList) > 1:
		# print "args " + str(args)
		# print "arglen " + str(len(args))

		if len(args) >= 2:

			# numlist = []
			# for x in range(99):
			# 	numlist.append(x)
			# if args[1] in numlist:
			try:
				if len(resultsList) >= int(args[-1]):
					client.send_cc("^c%s^~\n" %resultsList[int(args[-1]) - 1].longDescription)
					examined = True

					if isinstance(resultsList[int(args[-1]) - 1].kind, World.container):
						#print"has inv"
						#print "isLocked: " + str(resultsList[int(args[-1]) - 1].kind.isLocked)
						if resultsList[int(args[-1]) - 1].kind.isLocked == False:
							for ob in resultsList[int(args[-1]) - 1].kind.inventory:
								# if ob.name == "_".join(args):
								client.send_cc("^c[In %s]: %s^~\n" %(resultsList[int(args[1]) - 1].name, ob.name))
							if resultsList[int(args[-1]) - 1].kind.inventory == []:
								client.send_cc("^c[In %s]:^~\n" %resultsList[int(args[1]) - 1].name)
						else:
							client.send_cc("^cThe %s is locked.^~\n" %resultsList[int(args[1]) - 1].name)
			except ValueError:
				client.send("Object index must be an integer! My mother always said!\n")

			# for obj in resultsList:
			# 	if args[-1] == obj.name or args[-2] == obj.name:
			# 		examine(client, [obj.name], CLIENT_LIST, CLIENT_DATA)
					


		else:
			#print resultsList
			for obj in resultsList:
				# if obj.name == "_".join(args):
				client.send_cc("^c%s^~\n" %obj.longDescription)
				examined = True

				if isinstance(obj.kind, World.container):
					#print "*******"
					if obj.kind.isLocked == False:
						for ob in obj.kind.inventory:
							#print ob.name,
							client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.name))
						if obj.kind.inventory == []:
							client.send_cc("^c[In %s]:^~\n" %obj.name)
					else:
						client.send_cc("^cThe %s is locked.^~\n" %obj.name)	



	elif len(resultsList) == 1:
		#print resultsList
		for obj in resultsList:
			#print "result: " + str(obj)
			client.send_cc("^c%s^~\n" %obj.longDescription)
			examined = True

			#print obj.kind
			#print 'ob.inv: ' + str(obj.kind.inventory)

			if hasattr(obj.kind, 'inventory'):
				#print"&&&&&&&&&&&&&&"
				if obj.kind.isLocked == False:
					for ob in obj.kind.inventory:
						client.send_cc("^c[In %s]: A %s^~\n" %(obj.name, ob.name))
					if obj.kind.inventory == []:
						client.send_cc("^c[In %s]:^~\n" %obj.name)
				else:
					client.send_cc("^cThe %s is locked.^~\n" %obj.name)					





	# for obj in objectList:
	# 	if obj.name == "_".join(args):
	# 		client.send_cc("^c%s^~\n" %obj.longDescription)
	# 		examined = True

	# 		if isinstance(obj.kind, World.container):	# is a container, display the inventory
	# 			client.send_cc("^c^UContents^u: ")
	# 			for ob in obj.kind.inventory:
	# 				if len(obj.kind.inventory) == 1:
	# 					client.send_cc( "%s " %ob.name)
	# 				else:
	# 					client.send_cc( "%s, " %ob.name)
	# 			client.send_cc("^~\n")

	# 	elif isinstance(obj.kind, World.container):		# check container inventory for argument
	# 		for ob in obj.kind.inventory:
	# 			if ob.name == " ".join(args):
	# 				client.send_cc("^c[In %s]: %s^~\n" %(obj.name, ob.longDescription))
	# 				examined = True

	# handle examining a player

	# handle examining a mob



	if examined == False:
		if len(args) > 0:
			client.send("I don't see a '%s'. I seem to recall the names of things better when I 'look harder'!\n" %(" ".join(args)))
		else:
			client.send("I am not sure what I wanted to examine.\n")


def inventory(client, args, CLIENT_LIST, CLIENT_DATA):
	"""
	Display the contents of the player avatar's inventory
	"""
	clientDataID = str(client.addrport())

	longestItemName = 0
	longestItemDescription = 0

	for obj in CLIENT_DATA[clientDataID].avatar.kind.inventory:
		if len(obj.name) > longestItemName:
			longestItemName = len(obj.name)
		if len(obj.name) > longestItemDescription:
			longestItemDescription = len(obj.name)

	client.send_cc("\n^I[" + ((longestItemName + 9)* " ") + "    Inventory" + ((longestItemDescription + 16)* " ") +"]^~\n")
	client.send_cc("\nSpace: " + str(len(CLIENT_DATA[clientDataID].avatar.kind.inventory)) + "/" + str(CLIENT_DATA[clientDataID].avatar.kind.inventorySize)+ " used. \n\n")

	client.send_cc("^U^!Item Name" + (longestItemName* " ") + "    Item Description"+ (longestItemDescription * " ") + "^~\n")

	for obj in CLIENT_DATA[clientDataID].avatar.kind.inventory:
		client.send_cc(str(obj.name) + (((9 + longestItemName) - len(obj.name)) * " ") + "    " + str(obj.description) + "\n")
	client.send("\n")


def status(client, args, CLIENT_LIST, CLIENT_DATA):
	'''displays stats about the player'''
	clientDataID = str(client.addrport())
	avatar = CLIENT_DATA[clientDataID].avatar
	divspc1=0
	divspc2=0
	divspc3=0
	divspc4=0
	divspc5=0
	divspc6=0

	if avatar.kind.offense<10:
		divspc1=2
	elif avatar.kind.offense<100:
		divspc1=1

	if avatar.kind.vitality<10:
		divscp2=2
	elif avatar.kind.vitality<100:
		divspc2=1

	if avatar.kind.speed<10:
		divspc3=2
	elif avatar.kind.speed<100:
		divspc3=1

	if avatar.kind.IQ<10:
		divscp4=2
	elif avatar.kind.IQ<100:
		divspc4=1

	if avatar.kind.exp<10:
		divspc5=7
	elif avatar.kind.exp<100:
		divspc5=6
	elif avatar.kind.exp<1000:
		divspc5=5
	elif avatar.kind.exp<10000:
		divspc5=4
	elif avatar.kind.exp<100000:
		divspc5=3
	elif avatar.kind.exp<1000000:
		divspc5=2
	elif avatar.kind.exp<10000000:
		divspc5=1

	if avatar.kind.money<10:
		divspc6=0
	elif avatar.kind.money<100:
		divspc6=1
	elif avatar.kind.money<1000:
		divspc6=2
	elif avatar.kind.money<10000:
		divspc6=3
	elif avatar.kind.money<100000:
		divspc6=4
	elif avatar.kind.money<1000000:
		divspc6=5
	elif avatar.kind.money<10000000:
		divspc6=6
	elif avatar.kind.money<100000000:
		divspc6=7

	hpratio = (1.000*avatar.kind.hp)/(1.000*avatar.kind.maxHp)
	ppratio = (1.000*avatar.kind.pp)/(1.000*avatar.kind.maxPp)
	#print hpratio

	hpcolor = ""
	ppcolor = ""

	if hpratio <= 0.1:
		hpcolor = "^r"
	elif hpratio <= 0.33:
		hpcolor = "^R"
	elif hpratio <= 0.66:
		hpcolor = "^y"
	elif hpratio <= 0.85:
		hpcolor = "^g"
	elif hpratio < 1.0:
		hpcolor = "^G"

	if ppratio <= 0.1:
		ppcolor = "^K"
	elif ppratio <= 0.33:
		ppcolor = "^b"
	elif ppratio <= 0.66:
		ppcolor = "^B"
	elif ppratio <= 0.85:
		ppcolor = "^c"
	elif ppratio < 1.0:
		ppcolor = "^C"

	client.send_cc("    _____________________^I[ Status ]^~____________________\n")
	client.send_cc("    |"+ (" "*49) + "|\n")
	client.send_cc("  ^I  ^~| ^!" + str(avatar.name) + "^~, " + str(avatar.title) +(" "*(48-len(str(avatar.name))-2-len(str(avatar.title))))+ "|\n")
	client.send_cc("  ^I  ^~|"+ (" "*49) + "|\n")
	client.send_cc("  ^I  ^~| Level: " + str(avatar.kind.level)+ "     " +(" "*divspc5) +"Exp: " + str(avatar.kind.exp) + (" "*(48-7-5-5-divspc5-len(str(avatar.kind.level))-len(str(avatar.kind.exp)))) + "|\n")
	client.send_cc("  ^I  ^~|        " + " "*len(str(avatar.kind.level))+ "     " +(" "*divspc5) +"TNL: " + str(avatar.expToLevel) + (" "*(48-7-5-5-divspc5-len(str(avatar.kind.level))-len(str(avatar.expToLevel)))) + "|\n")
	client.send_cc("  ^I  ^~|"+ (" "*49) + "|\n")
	client.send_cc("  ^I  ^~| ^GHP:^~ " + hpcolor + str(avatar.kind.hp) + "^~" + "/" + str(avatar.kind.maxHp) +(" "*(48-4-len(str(avatar.kind.hp))-1-len(str(avatar.kind.maxHp))))+"|\n")
	client.send_cc("  ^I  ^~| ^CPP:^~ " + ppcolor + str(avatar.kind.pp) + "^~" + "/" + str(avatar.kind.maxPp) +(" "*(48-4-len(str(avatar.kind.pp))-1-len(str(avatar.kind.maxPp))))+ "|\n")
	client.send_cc("  ^I  ^~|"+ (" "*49) + "|\n")
	client.send_cc("  ^I  ^~| Offense: " + str(avatar.kind.offense) + "       " +(" "*divspc1)+ "Defense: " + str(avatar.kind.defense) +(" "*(47-9-7-divspc1-9-len(str(avatar.kind.defense))))+"|\n")
	client.send_cc("  ^I  ^~| Vitality: " + str(avatar.kind.vitality) + "        " +(" "*divspc2)+ "Guts: " + str(avatar.kind.guts) +(" "*(47-10-8-divspc2-6-len(str(avatar.kind.guts))))+ "|\n")
	client.send_cc("  ^I  ^~| Speed: " + str(avatar.kind.speed) + "         " + (" "*divspc3) + "Luck: "+ str(avatar.kind.luck) +(" "*(47-7-9-divspc3-6-len(str(avatar.kind.luck))))+ "|\n")
	client.send_cc("  ^I  ^~| IQ: " + str(avatar.kind.IQ) + "           " + (" "*divspc4) +(" "*(47-4-11-divspc4-0+1-len(str(avatar.kind.IQ))))+ "|\n")
	client.send_cc("  ^I  ^~|"+ (" "*49) + "|\n") 
	client.send_cc("  ^I  ^~| Money: $" + str(avatar.kind.money) + (" "*(47-8-0-divspc6-0+1-len(str(avatar.kind.money))))+ "|\n")
	client.send_cc("  ^I  ^~|_________________________________________________|\n")
	client.send_cc("  ^I                                                  ^~\n")
	client.send_cc("\n")


#-------------------------------------------------------------------


def render_room(client, player, room, CLIENT_DATA):
	"""
	Displays the details of whatever room the client is in to the client on room entry
	"""
	#print room
	#print room.region
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	# roomDescription = Rooms.master[regionRoom].description
	#print Rooms.master
	#print regionRoom
	roomName = Rooms.master[regionRoom].name
	# roomMobs = Rooms.master[regionRoom].mobs
	roomObjects = Rooms.master[regionRoom].objects
	# roomPlayers = Rooms.master[regionRoom].players
	# roomExits = Rooms.master[regionRoom].exits.keys()

	client.send_cc("\n^I[ " + roomName + " ]^~\n")
	display_description(client, room, CLIENT_DATA)
	display_objects(client, room, CLIENT_DATA)
	display_mobs(client, room, CLIENT_DATA)
	display_other_players(client, room, CLIENT_DATA)
	display_exits(client, room)


def examine_room(client, player, region, room, CLIENT_DATA):
	"""
	Displays more information than render_room
	"""
	regionRoom = str(region)+room.name.capitalize()
	roomDescription = Rooms.master[regionRoom].longDescription
	roomName = Rooms.master[regionRoom].name
	# roomMobs = Rooms.master[regionRoom].mobs
	# roomContainers = Rooms.master[regionRoom].containers
	# roomPlayers = Rooms.master[regionRoom].players
	# roomExits = Rooms.master[regionRoom].exits.keys()

	client.send_cc("\n^I[ Region: " + region +" ]\n")
	client.send_cc("[ Room Name: " + roomName + " ]\n^~\n")
	client.send(roomDescription + "\n\n")
	#display_description(client, room, CLIENT_DATA)
	display_object_names(client, room, CLIENT_DATA)
	display_mob_names(client, room, CLIENT_DATA)
	display_other_players(client, room, CLIENT_DATA, examine=True)
	display_exits(client, room)


def battle_examine_room(client, player, region, room, CLIENT_DATA):
	"""
	Displays more information than render_room
	"""
	regionRoom = str(region)+room.name.capitalize()
	roomDescription = Rooms.master[regionRoom].longDescription
	roomName = Rooms.master[regionRoom].name
	# roomMobs = Rooms.master[regionRoom].mobs
	# roomContainers = Rooms.master[regionRoom].containers
	# roomPlayers = Rooms.master[regionRoom].players
	# roomExits = Rooms.master[regionRoom].exits.keys()

	# client.send_cc("\n^I[ Region: " + region +" ]\n")
	client.send_cc("^I\n[ Room Name: " + roomName + " ]\n^~\n")
	client.send(roomDescription + "\n\n")
	#display_description(client, room, CLIENT_DATA)
	display_mob_names(client, room, CLIENT_DATA, isBattle=True)
	client.send("\n")
	display_other_players(client, room, CLIENT_DATA, examine=True)
	client.send("\n")

	display_player_status(client, room, CLIENT_DATA)
	display_battle_commands(client, CLIENT_DATA)

#-------------------------------------------------------------------------------

def display_description(client, room, CLIENT_DATA):
	#print display_description
	region =  room.region
	regionRoom = str(region)+room.name.capitalize()
	roomDescription = Rooms.master[regionRoom].description
	client.send_cc("\n" + str(roomDescription) + "\n\n")


def display_exits(client, room):
	region =  room.region
	regionRoom = str(region)+room.name.capitalize()
	roomExits = Rooms.master[regionRoom].exits.keys()
	client.send_cc("\n^UExits^u: " + str(roomExits) + "\n\n")


def display_other_players(client, room, CLIENT_DATA, examine=False):
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	roomPlayers = Rooms.master[regionRoom].players
	for player in roomPlayers:
		if player != CLIENT_DATA[str(client.addrport())].avatar and player.currentRoom == CLIENT_DATA[str(client.addrport())].avatar.currentRoom:
			if examine == True:
				client.send_cc("^gA player named ^~")
			client.send_cc("^g%s is here.^~\n" %player.name)


def display_objects(client, room, CLIENT_DATA):
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	roomObjects = Rooms.master[regionRoom].objects
	for obj in roomObjects:
		if obj.isVisible == True:
			client.send_cc("^c%s^~\n" %obj.description)


def display_object_names(client, room, CLIENT_DATA):
	region = room.region
	regionRoom = str(region)+room.name.capitalize()
	roomObjects = Rooms.master[regionRoom].objects
	for obj in roomObjects:
		if obj.isVisible == True:
			if obj.kind == None:
				client.send_cc("^cAn object named '%s'^~\n" %obj.name)
			elif isinstance(obj.kind, World.item):
				client.send_cc("^cAn item named '%s'^~\n" %obj.name)		
			elif isinstance(obj.kind, World.container):
				client.send_cc("^cA container named '%s'^~\n" %obj.name)


def display_mobs(client, room, CLIENT_DATA, isBattle=False):
	region = room.region
	regionRoom = str(region) + room.name.capitalize()
	roomMobs = Rooms.master[regionRoom].mobs
	#print 'mobs:' + str(roomMobs)
	for mob in roomMobs:

		if isBattle:
			mobhealthratio = (float(mob.kind.hp)/float(mob.kind.maxHp))
			if mobhealthratio == 1.0:
				healthmessage = '(healthy)'
			elif mobhealthratio >= 0.75:
				healthmessage = '(a few scratches)'
			elif mobhealthratio >= 0.50:
				healthmessage = '(bruised and battered)'
			elif mobhealthratio >= 0.25:
				healthmessage = '(injured and bleeding)'
			else:
				healthmessage = '(barely alive)'

		if not isBattle:
			client.send_cc("^y%s^~\n" %mob.description)
		else:
			client.send_cc("^y" + mob.description + " " + healthmessage + "^~\n")


def display_mob_names(client, room, CLIENT_DATA, isBattle=False):
	region = room.region
	regionRoom = str(region) + room.name.capitalize()
	roomMobs = Rooms.master[regionRoom].mobs
	#print 'mobs:' + str(roomMobs)
	for mob in roomMobs:

		if isBattle:
			mobhealthratio = (float(mob.kind.hp)/float(mob.kind.maxHp))
			if mobhealthratio == 1.0:
				healthmessage = '(healthy)'
			elif mobhealthratio >= 0.63:
				healthmessage = '(a few scratches)'
			elif mobhealthratio >= 0.33:
				healthmessage = '(bruised and battered)'
			elif mobhealthratio >= 0.1:
				healthmessage = '(pretty beat up and bleeding)'
			else:
				healthmessage = '(barely living)'

		if not isBattle:		
			client.send_cc("^yA mob named '%s'.^~\n" %mob.name)	
		else:
			client.send_cc("^yA mob named '" + mob.name + "'. " + healthmessage + "^~\n")


def display_player_status(client, room, CLIENT_DATA):
	clientDataID = str(client.addrport())
	avatar = CLIENT_DATA[clientDataID].avatar
	hpcolor='^G'
	ppcolor='^C'

	hpratio = float(avatar.kind.hp)/float(avatar.kind.maxHp)
	if avatar.kind.hp != avatar.kind.maxHp:
		hpcolor='^g'
	if hpratio <= 0.66:
		hpcolor='^y'
	if hpratio < 0.33:
		hpcolor='^r'

	ppratio = float(avatar.kind.pp)/float(avatar.kind.maxPp)
	if avatar.kind.pp != avatar.kind.maxPp:
		ppcolor='^c'
	if ppratio <= 0.66:
		ppcolor='^B'
	if ppratio < 0.33:
		ppcolor='^b'


	hpstring="^I" + hpcolor + "[          " + str(avatar.kind.hp) + "/" + str(avatar.kind.maxHp) + " ]^~\n"

	hpstringlength = len(hpstring)
	# print hpstringlength
	if hpstringlength <= 40:
		hpstringfiller = 40-hpstringlength
	else:
		hpstringfiller = 0
	# print hpstringfiller
	hpstring = hpstring[:-5] + (" "*hpstringfiller)+ hpstring[-5:]

	hpremratio = int((1.0-hpratio)*40)
	if hpremratio > 0:
		lowHealthMod = ''
		separator = '^~'
		cutoff = -(hpremratio) - 2
		if cutoff <= -36:
			cutoff = -36
		if hpratio < 0.1:
			lowHealthMod = '^r'
			separator = ''
			hpstring = hpstring[4:]
		hpstring = lowHealthMod + hpstring[:cutoff] + separator + hpstring[cutoff:]
		#print hpstring

	hpstring = "\n ^GHP: ^~" + hpstring



	ppstring="^I"+ ppcolor +"[          " + str(avatar.kind.pp) + "/"+ str(avatar.kind.maxPp) + " ]^~\n"

	ppstringlength = len(ppstring)
	# print ppstringlength
	if ppstringlength <= 40:
		ppstringfiller = 40-ppstringlength
	else:
		ppstringfiller = 0
	# print ppstringfiller
	ppstring = ppstring[:-5] + (" "*ppstringfiller)+ ppstring[-5:]

	ppremratio = int((1.0-ppratio)*40)
	if ppremratio > 0:
		lowPPMod = ''
		separator = '^~'
		cutoff = -(ppremratio) - 2
		if cutoff <= -36:
			cutoff = -36
		if ppratio < 0.1:
			lowPPMod = '^b'
			separator = ''
			ppstring = ppstring[4:]
		ppstring = lowPPMod + ppstring[:cutoff] + separator + ppstring[cutoff:]
		#print ppstring

	ppstring = " ^CPP: ^~" + ppstring


	client.send_cc("\n^!^I^w               " + avatar.name + (" "*(11+len(avatar.name)))+ "^~")
	client.send_cc(hpstring + ppstring+"\n")


def display_battle_commands(client, CLIENT_DATA):
	clientDataID = str(client.addrport())
	client.send_cc('^UCommands^~: ' + str(CLIENT_DATA[clientDataID].avatar.battleCommands) + "\n")
	client.send_cc("______________________________________\n\n")