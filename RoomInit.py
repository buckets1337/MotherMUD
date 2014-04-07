# RoomInit.py
# handles loading in all the rooms in all the regions in the world.

import Globals, Engine, Rooms, World
import os


masterRooms = Globals.masterRooms
regionListDict = Globals.regionListDict
fileData = []


def loadRoom(file):
	'''
	loads the contents of one room definition file into the world, and initializes the room with all required items and exits
	'''

	if str(file).endswith('~'):
		return

	print file

	path = 'world/' + file
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

	item = ''
	destRegion = ''
	destRoom = ''
	destContainer = ''
	hasSpawnContainers = False

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
				exitDetails = (exit).split(':')
				#print exitDetails
				exitsDict[exitDetails[1]] = Globals.regionListDict[exitDetails[0]][exitDetails[1]]
			newRoom.exits = exitsDict

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
						if ob.kind:
							if ob.kind.objectSpawner:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=True, whereFrom='file')
								spawnList.append(newObject)
							else:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
								spawnList.append(newObject)
						else:
							newObject = Engine.cmdSpawnObject(ob.name, newRoom, active=False)
							spawnList.append(newObject)

			newRoom.objects = spawnList
			Rooms.setCurrentRoom(newRoom.objects, newRoom)

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
			containersList = containersList.split(", ")
			for container in containersList:
				containerDetails = container.split(":")
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
				stuffDesc = entry.split(':')
				item = stuffDesc[0]
				container = stuffDesc[1]
				for obj in newRoom.objects:
					if obj.name == item:
						for ob in newRoom.objects:
							if ob.name == container and ob.kind is not None and ob.kind.inventory is not None:
								newRoom.objects.remove(obj)
								ob.kind.inventory.append(obj)
								print ob.kind.inventory





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
		directoryFiles = os.listdir('world/'+str(region)+'/')
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