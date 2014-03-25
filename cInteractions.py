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
	for obj in CLIENT_DATA[clientDataID].avatar.currentRoom.objects:
		# print obj.name
		# print 'argstr = ' + (" ".join(args))
		# print args

		if obj.name == " ".join(args):
			objectFound = True

			if obj.kind is not None and obj.kind.itemGrabHandler is not None:
				obj.kind.itemGrabHandler.get(client, CLIENT_DATA[clientDataID].avatar)
			else:
				client.send("*sigh* Why would you want to take the '%s'?\n" %obj.name)

		elif isinstance(obj.kind, World.container):
			for obj in obj.kind.inventory:
		# print obj.name
		# print 'argstr = ' + (" ".join(args))
		# print args
				for x in range(len(args[1:])):
					if obj.name == " ".join(args[-x:]):
						objectFound = True

						if obj.kind is not None and obj.kind.itemGrabHandler is not None:
							obj.kind.itemGrabHandler.get(client, CLIENT_DATA[clientDataID].avatar)
						else:
							client.send("The '%s' appears to be stuck in the '%s'.\n" %(obj.name, obj.owner.name))

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