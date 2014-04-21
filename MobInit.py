# mobInit.py
# initializes the mobs in the world, and handles saving and loading the mobs in the world to and from file

import os

import Globals
import Engine, World


mobsFromFile = Globals.mobsFromFile
fileList = []

for region in Globals.RegionsList:
	directoryFiles = os.listdir('blueprints/mob/'+str(region)+'/')
	for obj in directoryFiles:
		path = str(region)+'/'+ obj
		fileList.append(path)


def loadMobs():
	'''
	handles loading all the mob prototypes into the world from files.
	'''
	for file in fileList:
		loadMobFromFile(file)


def loadMobFromFile(file):
	'''
	handles loading a single mob from a given mob definition file into the world
	'''
	print file

	if str(file).endswith('~'):
		print '\n'
		return

	path = 'blueprints/mob/' + file
	with open(path, 'r') as f:
		fileData = f.readlines()



	newMob = World.Mob('none', 'none', 'none')

	print fileData

	splitFile = file.split("/")
	mobID = None
	name = 'none'
	species = None
	currentRoom = None
	region = None
	description = ''
	longDescription = ''
	hp = 0
	exp = 0
	inventory = []
	inventorySize = 0
	equipment = {}
	kind = None
	expirator = None
	inventoryItems = []
	currentRoomString = ''

	newMob.kind = World.mortal(0,0)
	newMob.region = splitFile[0]

	for Data in fileData:

		if Data.startswith('mobID='):
			IDstring = Data[6:-1]
			if IDstring != '':
				newMob.mobID = int(IDstring)
		if Data.startswith('name='):
			newMob.name = Data[5:-1]
		if Data.startswith('species='):
			newMob.species = Data[8:-1]
		if Data.startswith('currentRoom='):
			currentRoomString = Data[12:-1]
		if Data.startswith('description='):
			newMob.description = Data[12:-1]
		if Data.startswith('longDescription='):
			newMob.longDescription = Data[16:-1]
		if Data.startswith('speech='):
			newMob.speech = Data[7:-1]

		if Data.startswith('kind.hp='):
			newMob.kind.hp = int(Data[8:-1])
		if Data.startswith('kind.exp='):
			newMob.kind.exp = int(Data[9:-1])
		if Data.startswith('kind.inventory='):
			invString = Data[15:-1]
			if invString != '':
				#print "invString:" + invString
				invList = invString.split(', ')
				#print 'invList:' + str(invList)
				for item in invList:
					for ob in Globals.fromFileList:
						if item == ob.name:
							inventoryItems.append(item)
		if Data.startswith('kind.inventorySize='):
			newMob.kind.inventorySize = int(Data[19:-1])


	if currentRoomString != '':
		currentRoomCoords = currentRoomString.split(":")
		newMob.currentRoom = Globals.regionListDict[currentRoomCoords[0]][currentRoomCoords[1]]
	else:
		newMob.currentRoom = Globals.regionListDict[newMob.region]['bullpen']

	for item in inventoryItems:
		#print item
		removed = False
		newItem = Engine.cmdSpawnObject(item, newMob.currentRoom, alert=False, whereFrom='mobinv')
		newMob.kind.inventory.append(newItem)
		for obj in newMob.currentRoom.objects:
			if obj.name == item:
				newMob.currentRoom.objects.remove(obj)

	newMob.currentRoom.mobs.append(newMob)
	Globals.mobsFromFile.append(newMob)


	print 'region:' + str(newMob.region)







def saveMobs():
	'''
	handles saving all mobs in the world into unique mob definition files when the server is shutdown
	'''
	pass


def saveMobToFile():
	'''
	handles saving a single mob to a unique mob definition file when the server is shutdown
	'''
	pass

