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
			exitsList = (Data[6:-1]).split(',')
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
			objectList = objectList.split(",")
			#print objectList
			spawnList = []
			#print "ffl:"+str(Globals.fromFileList)
			for obj in objectList:
				#print obj
				for ob in Globals.fromFileList:
					if ob.name == obj:
						if ob.kind:
							if ob.kind.objectSpawner:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, ob.kind.objectSpawner.active)
								spawnList.append(newObject)
							else:
								newObject = Engine.cmdSpawnObject(ob.name, newRoom, False)
								spawnList.append(newObject)
						else:
							newObject = Engine.cmdSpawnObject(ob.name, newRoom, False)
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



	labelString = newRoom.region + newRoom.name.capitalize()
	#print 'ls:' + labelString
	Globals.masterRooms[labelString] = newRoom
	Globals.regionListDict[newRoom.region][newRoom.name] = newRoom

	print "name=" + newRoom.name
	print "region=" + newRoom.region
	print "description=" + newRoom.description
	print "longDescription" + newRoom.longDescription
	print "exits=" + str(newRoom.exits)
	print "objects=" + str(newRoom.objects)
	print "\n"






def setup():
	fileList=[]
	for region in Globals.RegionsList:
		directoryFiles = os.listdir('world/'+str(region)+'/')
		for roomFile in directoryFiles:
			path = str(region)+'/'+ roomFile
			fileList.append(path)
	for room in fileList:
		loadRoom(room)