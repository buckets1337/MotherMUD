# cInteractions
# handles various commands that modify the world in some manner

import World

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
		client.send("You have no more space in your inventory. Drop something first.\n")
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
					if len(args) > 0:
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


	if len(resultsList) == 1:
		if resultsList[0].kind is not None and resultsList[0].kind.itemGrabHandler is not None:
			resultsList[0].kind.itemGrabHandler.get(client, CLIENT_DATA[clientDataID].avatar)
			objectFound = True
		else:
			client.send("*sigh* Why would you want to take the '%s'?\n" %resultsList[0].name)
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
					client.send("*sigh* Why would you want to take the '%s'?\n" %resultsList[int(index) - 1].name)
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
	client.send("Dropping...\n")