# RoomInit.py
# handles loading in all the rooms in all the regions in the world.

import Globals, Engine, Rooms, World
import os


masterRooms = Globals.masterRooms
regionListDict = Globals.regionListDict
fileData = []

def saveAllRooms():
	'''
	saves each room in the server's memory to a room definition text file
	'''
	for region in Globals.regionListDict:
		# pathRoot= 'data/world/'
		# if not os.path.exists(pathRoot):
		# 	os.makedirs(pathRoom)
		path= 'data/world/'+ region + '/'
		if not os.path.exists(path):
			os.makedirs(path)
		#print 'region:' + str(region)
		for room in Globals.regionListDict[region]:
			#print 'room:' + str(Globals.regionListDict[region][room])
			saveRoom(Globals.regionListDict[region][room])


def saveRoom(room):
	'''
	saves the room and it's contents to a room definition file
	'''
	#print room
	region = room.region
	path = 'data/world/'+region+'/'+room.name


	with open(path, 'w') as f:
		f.write('name=%s\n' %room.name)
		f.write('region=%s' %room.region)
		f.write('\n\n')
		f.write("description='%s'" %room.description)
		f.write('\n\n')
		f.write("longDescription='%s'" %room.longDescription)
		f.write('\n\n')
		f.write('exits=',)
		fileString = ''
		for exit in room.exits:
			exitRegion = room.exits[exit].region
			exitRoom = room.exits[exit].name
			fileString = fileString + (exitRegion+':'+exitRoom+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')
		f.write('actives=',)
		fileString = ''
		for obj in room.objects:
			if hasattr(obj.kind,'objectSpawner'):
				if hasattr(obj.kind.objectSpawner, 'active'):
					if obj.kind.objectSpawner.active:
						fileString = fileString + (obj.name+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')				
		f.write('objects=',)
		fileString = ''
		for obj in room.objects:
			#print obj
			info = dir(obj)
			#print info
			fileString = fileString + (obj.name+', ')
			if hasattr(obj.kind,'inventory'):
				#print 'inv:' + str(obj.kind.inventory)
				for ob in obj.kind.inventory:
					fileString = fileString + (ob.name+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')
		f.write('spawnPoints=',)
		for obj in room.objects:
			fileString = ''
			if hasattr(obj, 'kind') and hasattr(obj.kind, 'objectSpawner') and obj.kind is not None and obj.kind.objectSpawner is not None:
				if obj.kind.objectSpawner.startingLocation[0].name != room.name:
					fileString = fileString + (obj.name +':'+obj.currentRoom.region+'-'+obj.kind.objectSpawner.startingLocation[0].name + ', ')
				if fileString.endswith(', '):
					fileString = fileString[:-2]
				f.write(fileString)
		f.write('\n\n')
		f.write('spawnContainers=',)
		for obj in room.objects:
			fileString = ''

			if obj.spawnContainer != None:
				fileString = fileString + (obj.name +':'+obj.currentRoom.region+'-'+obj.kind.objectSpawner.startingLocation[0].name + '-'+ str(obj.spawnContainer.name)+', ')
			if fileString.endswith(', '):
				fileString = fileString[:-2]
			f.write(fileString)
		f.write('\n\n')
		f.write('stuffList=',)
		fileString = ''
		for obj in room.objects:
			if hasattr(obj, 'kind'):
				#print "^^^stuffkind"
				if hasattr(obj.kind, 'inventory'):
					#print "^^^stuffinv"
					if obj.kind.inventory != []:
						#print "^^^stuffobjinv" + str(obj.kind.inventory)
						for ob in obj.kind.inventory:
							fileString = fileString + (ob.name+':'+obj.name+', ')
		if fileString.endswith(', '):
			fileString = fileString[:-2]
		f.write(fileString)
		f.write('\n\n')






def loadRoom(file):
	'''
	loads the contents of one room definition file into the world, and initializes the room with all required items and exits
	'''

	if str(file).endswith('~'):
		return

	print file

	path = 'blueprints/world/' + file
	if os.path.exists('data/world/' + file):
		path = 'data/world/' + file
	with open(path, 'r') as f:
		fileData = f.readlines()

	print fileData



	# name = None
	# region = None
	# description = None
	# longDescription = None
	# exits = {}
	# objects = []
	fileDetails = file.split("/")
	newRoom = regionListDict[fileDetails[0]][fileDetails[1]]

	newRoom.players = []

	item = ''
	destRegion = ''
	destRoom = ''
	destContainer = ''
	hasSpawnContainers = False
	activesList = []

	for Data in fileData:


		if Data.startswith('name='):
			newRoom.name = Data[5:-1]
			#print "name-" + newRoom.name

		if Data.startswith('region='):
			newRoom.region = Data[7:-1]

		if Data.startswith('description='):
			newRoom.description = Data[13:-2]

		if Data.startswith('longDescription='):
			newRoom.longDescription = Data[17:-2]

		if Data.startswith('exits='):
			#print Data
			exitsDict = {}
			exitsList = (Data[6:-1]).split(', ')
			#print exitsList
			regionRooms = Globals.regionListDict[newRoom.region]
			for exit in exitsList:
				if exit != '':
					exitDetails = (exit).split(':')
					#print exitDetails
					exitsDict[exitDetails[1]] = Globals.regionListDict[exitDetails[0]][exitDetails[1]]
			newRoom.exits = exitsDict

		if Data.startswith('actives='):
			activesList = Data[8:-1]
			activesList = activesList.split(", ")
			print 'actives:' + str(activesList)

		if Data.startswith('objects='):
			#print Data
			objectList = Data[8:-1]
			objectList = objectList.split(", ")
			#print objectList
			spawnList = []
			#print "ffl:"+str(Globals.fromFileList)
			for obj in objectList:
				#print obj
				for ob in Globals.fromFileList:
					if ob.name == obj:
						#print '!!!name'
						if hasattr(ob, 'kind'):
							#print '!!!kind'
							if hasattr(ob.kind, 'objectSpawner'):
								#print '!!!objSpwn'
								act = False
								#print '###actives:' + str(activesList)
								for spawner in activesList:
									# print 'spn:' + spawner
									# print 'ob:' + ob.name
									if str(ob.name) == str(spawner):
										act = True
										activesList.remove(spawner)
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=act, whereFrom='file')
								if act == False and hasattr(newObject, 'kind') and hasattr(newObject.kind,'objectSpawner') and hasattr(newObject.kind.objectSpawner,'timer'):
									Globals.TIMERS.remove(newObject.kind.objectSpawner.timer)
								spawnList.append(newObject)
							else:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
								spawnList.append(newObject)
						else:
							newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
							spawnList.append(newObject)

			newRoom.objects = spawnList
			Rooms.setCurrentRoom(newRoom.objects, newRoom)
			#print newRoom.name
			for obj in newRoom.objects:
				print str((obj.name, obj.currentRoom.name))

		if Data.startswith('spawnPoints='):
			pointsList = Data[12:-1]
			pointsList = pointsList.split(", ")
			for point in pointsList:
				pointDetails = point.split(":")
				for obj in newRoom.objects:
					if obj.name == pointDetails[0]:
						coord = pointDetails[1].split('-')
						obj.kind.objectSpawner.startingLocation = regionListDict[coord[0]][coord[1]],

		if Data.startswith('spawnContainers='):
			hasSpawnContainers = True
			containersList = Data[16:-1]
			if containersList != '':
				containersList = containersList.split(", ")
				#print '***' + str(containersList)
				for container in containersList:
					containerDetails = container.split(":")
					#print '***' + str(containerDetails)
					containerSpecs = containerDetails[1].split("-")

					item = containerDetails[0]
					destRegion = containerSpecs[0]
					destRoom = containerSpecs[1]
					destContainer = containerSpecs[2]

					for obj in newRoom.objects:
						if obj.name == item:
							obj.spawnContainer = [item, destRegion, destRoom, destContainer]

		if Data.startswith('stuffList='):
			stuffList = Data[10:-1]
			stuffList = stuffList.split(', ')

			for entry in stuffList:
				if entry != '':
					stuffDesc = entry.split(':')
					item = stuffDesc[0]
					container = stuffDesc[1]
					#print "container:" + container
					resultsList = []
					ID = False
					objObject = None
					for obj in newRoom.objects:
						if obj.name == item:
							objObject = obj
						# if hasattr(obj, 'kind'):
						# 	#print "$$$$$$stuff2kind"
						# 	if hasattr(obj.kind, 'inventory'):
						# 		#print "$$$$$stuff2inv"
						if obj.name == container:
							#print "$$$$$stuff2cont " + ob.name
							# print newRoom.objects
							# if obj in newRoom.objects:
							# 	newRoom.objects.remove(obj)	
							# ob.kind.inventory.append(obj)
							resultsList.append(obj)
							#print ob.kind.inventory
						elif obj.name == container[:-1]:
							resultsList.append(obj)
							ID = True

					if resultsList != []:
						# for obj in resultsList:
						# 	print obj.name
						# print 'res:' + str(resultsList)
						# print 'con:' + str(container)
						# print 'conID:' + str(container[-1:])
						if ID == True:
							selected = resultsList[int(container[-1:]) - 1]
							#print 'id'
						else:
							selected = resultsList[0]
						#print selected
						if objObject in newRoom.objects:
							newRoom.objects.remove(objObject)
						selected.kind.inventory.append(objObject)
						#print 'inv:' +str(selected.kind.inventory)






	labelString = newRoom.region + newRoom.name.capitalize()
	#print 'ls:' + labelString
	Globals.masterRooms[labelString] = newRoom
	Globals.regionListDict[newRoom.region][newRoom.name] = newRoom





	# if hasSpawnContainers:
	# 	found = False
	# 	for region in Globals.regionListDict:
	# 		for room in Globals.regionListDict[region]:
	# 			roomObj = Globals.regionListDict[region][room]
	# 			#print '****regionRooms:' + str(Globals.regionListDict[region][room])
	# 	#print Globals.regionListDict
	# 			# print 'roomName:' + roomObj.name
	# 			# print 'destRoom:' + destRoom
	# 			if roomObj == Globals.regionListDict[destRegion][destRoom]:
	# 				for obj in roomObj.objects:
	# 					if obj.name == destContainer:
	# 						for thing in roomObj.objects:
	# 							if thing.name == item and found == False:
	# 								roomObj.objects.remove(thing)
	# 								obj.inventory.append(thing)
	# 								found = True



	print "name=" + newRoom.name
	print "region=" + newRoom.region
	print "description=" + newRoom.description
	print "longDescription" + newRoom.longDescription
	print "exits=" + str(newRoom.exits)
	print "objects=" + str(newRoom.objects)
	print "\n"


	#print newRoom
	return newRoom


def setSpawnContainers(newRoom):
	for obj in newRoom.objects:
		#print obj.name
		if obj.spawnContainer is not None:
			destination = Globals.regionListDict[obj.spawnContainer[1]][obj.spawnContainer[2]]
			#print "destination:" + str(destination) + obj.spawnContainer[1] + ":" + obj.spawnContainer[2]
			#print destination.objects
			for item in destination.objects:
				#print item.name
				#print "destCont:" + obj.spawnContainer[3]
				if item.name == obj.spawnContainer[3]:
					obj.spawnContainer = item
					# for ob in Globals.fromFileList:
					# 	if ob.name == obj.name
					#print "spawnCont:" + str(obj.spawnContainer) + str(obj.spawnContainer.name)




def setup():
	fileList=[]
	for region in Globals.RegionsList:
		directoryFiles = os.listdir('blueprints/world/'+str(region)+'/')
		for roomFile in directoryFiles:
			path = str(region)+'/'+ roomFile
			fileList.append(path)
	newRooms = []
	for room in fileList:
		if room is not None:
			newRooms.append(loadRoom(room))
		#print newRooms
	for room in newRooms:
		if room is not None:
			setSpawnContainers(room)

	# for room in Globals.masterRooms:
	# 	print room
	# 	for obj in Globals.masterRooms[room].objects:
	# 		print obj
	# 		if obj.kind:
	# 			if obj.kind.objectSpawner:
	# 				stuffed = obj.kind.objectSpawner.stuff(obj.kind.objectSpawner)
	# 				if stuffed:
	# 					print obj.name + " stuffed"