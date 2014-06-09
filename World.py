# World.py
"""
describes the classes for objects that will be in the world
"""

import Engine, aiMove, cMove
import Globals
import random



class World():
	"""
	This class represents the world map.  It should contain a list of regions, along with any other globally-applicable information
	"""
	def __init__(self, regions=[]):
		self.regions = regions	 # an easy way to add the regions on world initialization is by using Regions.list, as it should already contain every region


class Region():
	"""
	This class represents a region on the map.  A region is a collection of rooms sharing a common theme or idea.  Examples: a forest, a dungeon, a town, etc
	"""
	def __init__(self, regionName, description, rooms=[]):
		self.rooms = rooms
		self.regionName = regionName
		self.description = description


class Room():
	"""
	This class holds data and methods for a single room.  Most of the information about the world will be stored in instances of this class
	"""
	# containers is a list of all containers in a room
	# exits is a dictionary of exits, with the key being the command and the value being the room it connects to
	# mobs is a list of all badguys in a room
	# players is a list of all clients in a room
	# description is a string containing a prose description of the room
	# longDescription is a string containing a more detailed prose description of the room
	# items is a list of all items in a room
	# region is the world region that the room belongs to
	# name is the name of the room

	def __init__(self, region='', name='', description='', exits={}, longDescription = '', players=[], objects=[], items=[], containers=[], mobs=[]):
		self.region = region
		self.name = name
		self.description = description
		self.exits = exits
		self.longDescription = longDescription
		self.players = players
		self.objects = objects
		self.items = items
		self.containers = containers
		self.mobs = mobs


#----------------------------------------------------------------------------------------------------------------------------------------------------------------



class Timer:
    """
    A timer is an object that, when spawned, will count down until zero, and then perform and action and possibly respawn itself
    """
    def __init__(self, TIMERS, time, actionFunction, actionArgs = [], attachedTo = None, respawns = False):
        self.TIMERS = TIMERS
        self.time = time
        self.actionFunction = actionFunction
        self.actionArgs = actionArgs
        self.attachedTo = attachedTo
        self.respawns = respawns

        self.currentTime = float(time)

        self.count = 0

        self.TIMERS.append(self)

        # self.initialTime = time.clock()
        # self.lastTime = 0

    def tick(self, deltaTime):     
        """tick should be called once each game loop"""
        #timePassed = (time.clock() - self.initialTime) - self.lastTime

        self.currentTime -= deltaTime
        #print self.currentTime
        #print "tick"
        self.count += 1
        #print str(self.count) + self.attachedTo.owner.owner.name

        if self.currentTime <= 0:

			#print "time out. " + str(self.attachedTo.owner.owner.name) + " " + str(self)
			if self in Globals.TIMERS:
				Globals.TIMERS.remove(self)
			elif self in Globals.MoveTIMERS:
				Globals.MoveTIMERS.remove(self)

			#print "removed " + str(self)

			if self.actionArgs != []:
				self.actionFunction(self.actionArgs)
			else:
			    self.actionFunction()


			#print "timers:" + str(Globals.TIMERS)


			# if self.respawns == True:
			#     self.currentTime = self.time
			#     Globals.TIMERS.append(self)




#------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Object():
	"""
	A class representing objects in the world.  Objects contain a description and location, but may or may not be visible.
	An object that contains no other components is essentially a prop, or scenery.  Adding components allows items to be built that do more interesting things.
	"""
	def __init__(self, name, description, currentRoom = None, isVisible = False, spawnContainer = None, longDescription = None, kind = None, TIMERS = None):
		self.name = name
		self.description = description
		self.currentRoom = currentRoom
		self.isVisible = isVisible
		self.spawnContainer = spawnContainer
		self.longDescription = longDescription
		if self.longDescription == None:
			self.longDescription = self.description
		self.kind = kind								# The 'kind' attribute is a placeholder for a high-level composition class, like 'item' or 'container'.
		if self.kind:									# Adding a 'kind' to an object makes the object interactable, and gives it other features.
			self.kind.owner = self
		self.TIMERS = TIMERS
		if self.TIMERS:
			self.TIMERS.owner = self



class item:		# 'kind' attribute
	"""
	This component represents an item, that is able to be picked up and used by players in some manner
	"""
	def __init__(self, isCarryable = True, respawns = False, itemGrabHandler = None, objectSpawner = None):
		self.isCarryable = isCarryable		# if true, item can be picked up into an inventory
		self.respawns = respawns 			# if true, item will eventually respawn at original location after it has been picked up
		self.itemGrabHandler = itemGrabHandler
		if self.itemGrabHandler:
			self.itemGrabHandler.owner = self
		self.objectSpawner = objectSpawner
		if self.objectSpawner:
			self.objectSpawner.owner = self


class container:		# 'kind' attribute
	"""
	This component represents some kind of container.  A container is an object that has an inventory and may hold other items.
	"""
	def __init__(self, inventory = [], isLocked = False, isCarryable = False, respawns = False, respawnContents = False, itemGrabHandler = None, objectSpawner = None):
		self.inventory = inventory
		self.isLocked = isLocked
		self.isCarryable = isCarryable		# if true, container can be picked up into an inventory. Must have 'itemGrabHandler' component to do this.
		self.respawns = respawns 			# if true, container will eventually respawn at original location after it has been picked up
		self.respawnContents = respawnContents 	# if true, container will eventually respawn it's contents (possibly running a random check on a loot table again)
		self.itemGrabHandler = itemGrabHandler
		if self.itemGrabHandler:
			self.itemGrabHandler.owner = self
		self.objectSpawner = objectSpawner
		if self.objectSpawner:
			self.objectSpawner.owner = self


class itemGrabHandler:		# for 'kind' components, adds the ability for item to be picked up or dropped
	"""
	This component adds the ability to pick up and drop an item
	"""
	def __init__(self, notDroppable = False):
		self.notDroppable = notDroppable

	def get(self, client, player):
		# check if 'item' is in room...if so, remove it from room, and add it to avatar's inventory 
		if self.owner.isCarryable:
			player.kind.inventory.append(self.owner.owner)		# add the top level of the item to the avatar's inventory

			gotten = False
			# print 'sc:' + str(self.owner.owner.spawnContainer)
			# print 'owner:'+str(self.owner.owner.name)
			# print 'sooco:'+str(self.owner.owner.currentRoom.objects)
			# for obj in self.owner.owner.currentRoom.objects:
			# 	print obj.name
			# print 'cr:'+str(self.owner.owner.currentRoom.name)
			if self.owner.owner.spawnContainer is None:
				for obj in self.owner.owner.currentRoom.objects:
					# print 'objname:'+obj.name
					# print 'ownname:'+self.owner.owner.name
					if obj == self.owner.owner and gotten == False:
						# print 'cro:' + str(self.owner.owner.currentRoom.objects)
						self.owner.owner.currentRoom.objects.remove(self.owner.owner)		# remove from the top level currentRoom's objects list the top level of the item
						#print '!self.owner.owner removed!'
						gotten = True
					elif obj.name == self.owner.owner.name and gotten == False:
						#print 'curroomobj:'+ str(self.owner.owner.currentRoom.objects)
						self.owner.owner.currentRoom.objects.remove(obj)
						#print self.owner.owner.currentRoom.objects
						#print'!'+ obj.name + ' removed!'
						gotten = True

					elif hasattr(obj, 'kind'):
						if hasattr(obj.kind, 'inventory'):
							#print obj.kind.inventory
							if obj.kind.inventory != []:
								#print obj.kind.inventory
								inv = obj.kind.inventory
								for ob in inv:
									#print "ob:"+ str(ob)
									if ob == self.owner.owner and gotten == False:
										#print obj.kind.inventory
										obj.kind.inventory.remove(ob)		# remove from the top level currentRoom's objects list the top level of the item
										gotten = True
									# elif ob.name == self.owner.owner.name and gotten == False:
									# 	#print obj.kind.inventory
									# 	print ob.name
									# 	obj.kind.inventory.remove(ob)
									# 	gotten = True
			else:
				# if self.owner.owner in self.owner.owner.spawnContainer.kind.inventory:
				# 	self.owner.owner.spawnContainer.kind.inventory.remove(self.owner.owner)

				for obj in self.owner.owner.spawnContainer.kind.inventory:
					if obj.name == self.owner.owner.name and gotten == False:
						self.owner.owner.spawnContainer.kind.inventory.remove(obj)
						gotten = True
				if self.owner.owner in self.owner.owner.currentRoom.objects:
					self.owner.owner.currentRoom.objects.remove(self.owner.owner)
					gotten = True
				if gotten == False:
					print str(self.owner.owner.name) +'not found.'

			client.send("You picked up a %s.\n" %self.owner.owner.name)


		else:
			client.send("You are not able to carry %s.\n" %item.name)
		

class objectSpawner:		# for 'kind' components, a component that, when placed in a room or container, will attempt to randomly spawn objects at specified intervals
	def __init__(self, owner, TIMERS = None, time = 0, obj = None, oddsList = None, container = None, cycles=1, repeat = False, active = False):
		self.owner = owner
		self.TIMERS = TIMERS
		self.owner.owner.TIMERS = self.TIMERS
		self.time = time
		self.obj = obj
		self.oddsList = oddsList
		self.container = container
		self.cycles = cycles
		self.repeat = repeat
		self.active = active
		if self.active:
			timer = Timer(TIMERS, time, self.spawn, [], self, False)
		else:
			timer = None
		self.timer = timer
		#print "obj in:" + str(self.owner.owner.currentRoom)
		self.startingLocation = self.owner.owner.currentRoom,


	def stuff(self, obj, isNew):
			#moves newly spawned objects to containers
		#print self.owner.owner.spawnContainer
		#print obj.name
		if obj.spawnContainer != None:
			#print obj.spawnContainer.name
			#print obj.spawnContainer
			#if obj.spawnContainer in obj.kind.objectSpawner.startingLocation[0].objects:
				#print "object sc and sl ="
			#print obj.spawnContainer.kind
			# if obj.owner.owner.spawnContainer.currentRoom == self.startingLocation[0]:
				#print self.startingLocation[0].name
			if isNew:
				obj.kind.objectSpawner.startingLocation[0].objects.remove(obj)
			#print "sc:" + str(obj.spawnContainer) + " " + str(obj.spawnContainer.name)
			#print "sro:" + str(obj.kind.objectSpawner.startingLocation[0].objects)
			for ob in obj.kind.objectSpawner.startingLocation[0].objects:
				#print ob.name
				if ob == obj.spawnContainer:
					ob.kind.inventory.append(obj)
					#print ob.kind.inventory
			#print obj.spawnContainer.kind.inventory
			return True
		#print "stuff of " + obj.name + " failed"
		return False


	def spawn(self):
		if self.active:
		 	#if self.startingLocation[0] is not None:
			#print self.active

			if self.repeat:
				self.timer.currentTime = self.time
				#print "repeatTime: " + str(self.timer.currentTime)
				self.TIMERS.append(self.timer)
				#print str(self.timer) + " repeated. " + str(Globals.TIMERS)

			elif self.cycles > 1:
				self.cycles -= 1
				#Globals.TIMERS.remove(self.timer)
				self.timer.currentTime = self.time
				#print "cycleTime: " + str(self.timer.currentTime)
				Globals.TIMERS.append(self.timer)
				#print "cycles -1 " + str(Globals.TIMERS)

			winner = Engine.selector(self.oddsList)
			if winner[0]:
				#print self.active
				#print self.owner.owner.currentRoom
				#print self.startingLocation
				#self.obj.currentRoom = self.startingLocation[0]	# tell the object what room it is in

				for obj in Globals.fromFileList:
					if obj.name == self.obj.name:
						refobj = obj.name
						ob = obj

				#print self.active
				newObject = Engine.cmdSpawnObject(refobj, self.startingLocation[0], whereFrom='objSpawner', spawnContainer=self.owner.owner.spawnContainer)
				#print self.active
				#print str(newObject.name) + " added timer " + str(newObject.kind.objectSpawner.timer)
				#print "ob " +str(ob.kind.objectSpawner.active)
				#print self.active
				#print newObject.spawnContainer
				#print self.owner.owner
				# if self.startingLocation[0] is not None:
				#self.startingLocation[0].objects.append(self.obj)
				# else:
				# 	pass	# add the new object to the room

				stuffed = self.stuff(newObject, True)		# try shoving items in containers if they should be there instead of in the room

				# for client in Globals.CLIENT_LIST:
				# 	if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
				# 		if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == self.startingLocation[0]:		# if a client is in the room object just appeared in, let it know
				# 			if not stuffed:
				# 				client.send_cc("^BA %s appeared.^~\n" %self.owner.owner.name)
				# print "repeat:" + str(self.repeat)
				# print "cycles:" + str(self.cycles)
				# print "timer:" + str(self.timer)
				#print "currentTime:" + str(self.obj.kind.objectSpawner.timer.currentTime)
				# print "time:" + str(self.timer.time)
				# print "name:" + str(self.owner.owner.name)


					#print "$o  "+ str(self.owner.owner)+ " "+ str(self.owner.owner.name) + " @ [" + str(self.startingLocation[0].region) + ":" + str(self.startingLocation[0].name) +"]"

			# else:
			# 	self.obj.kind.objectSpawner.timer.currentTime = self.time
			# 	#print self.timer.time
			# 	Globals.TIMERS.append(self.obj.kind.objectSpawner.timer)
			# 	print "noWin " + str(Globals.TIMERS)
	
		else:
			if self.owner.owner.spawnContainer is not None:
				if not(self.owner.owner in self.owner.owner.spawnContainer.kind.inventory):
					stuffed = self.stuff(self.owner.owner, False)	

		#print "timers:",
		#for timer in Globals.TIMERS:
		# 	print str(timer)
		 	#print str(timer.attachedTo.owner.owner.name),
		# 	print str(timer.currentTime
		#print "\n"


class mobSpawner:		# for Objects, a component that, when placed on an object in a room, randomly spawns mobs at a given interval into that room
	def __init__(self, owner, TIMERS = None, time = 0, mob = None, oddsList = None, cycles=1, mode = None, active = True):
		self.owner = owner
		self.TIMERS = TIMERS
		self.owner.TIMERS = self.TIMERS
		self.time = time
		self.mob = mob
		self.oddsList = oddsList
		self.cycles = cycles
		self.mode = mode
		self.active = active
		if self.active:
			timer = Timer(Globals.TIMERS, time, self.spawn, [], self, False)
		else:
			timer = None
		self.timer = timer
		#print "obj in:" + str(self.owner.owner.currentRoom)
		self.startingLocation = self.owner.currentRoom,




	def spawn(self):

		winner = Engine.selector(self.oddsList)

		if winner[0]:

			#print "winner"

			for mob in Globals.mobsFromFile:
				if mob.name == self.mob:
					refmob = mob.name
					ob = mob
				elif hasattr(self.mob, 'name') and mob.name == self.mob.name:
					refmob = mob.name
					ob = mob

			if self.mode == 'pack':		# spawns a group of mobs, the maximum size of which is determined by self.cycles. Always spawns at least one mob.
				iters = 0
				maxNum = random.randint(1, self.cycles)
				#print str(iters) + ":" + str(maxNum)
				while iters < maxNum:
					#print str(iters) + ":" + str(maxNum)
					newMortal = mortal(hp=int(ob.kind.hp), maxHp=int(ob.kind.maxHp), pp=int(ob.kind.pp), maxPp=int(ob.kind.maxPp), level=int(ob.kind.level), exp=int(ob.kind.exp), money=int(ob.kind.money), offense=int(ob.kind.offense), defense=int(ob.kind.defense), speed=int(ob.kind.speed), guts=int(ob.kind.guts), luck=int(ob.kind.luck), vitality=int(ob.kind.vitality), IQ=int(ob.kind.IQ), inventory=[], inventorySize=int(ob.kind.inventorySize), equipment={})
					newMob = Mob(ob.description, ob.currentRoom, ob.name, ob.region, ob.longDescription, ob.speech, newMortal, ob.species, None)
					if hasattr(ob, 'aiMove'):
						newAIComponent = aiMove.movementAI(newMob, ob.aiMove.time)
						if ob.aiMove.Timer.actionFunction == ob.aiMove.basicRandom:
							newAIComponent.Timer.actionFunction = newAIComponent.basicRandom
						if ob.aiMove.Timer.actionFunction == ob.aiMove.introvertRandom:
							newAIComponent.Timer.actionFunction = newAIComponent.introvertRandom
						if ob.aiMove.Timer.actionFunction == ob.aiMove.extrovertRandom:
							newAIComponent.Timer.actionFunction = newAIComponent.extrovertRandom
						if ob.aiMove.Timer.actionFunction == ob.aiMove.doNotMove:
							newAIComponent.Timer.actionFunction = newAIComponent.doNotMove
					newMob.aiMove = newAIComponent

					if hasattr(ob, 'aiBattle'):
						newMob.aiBattle = ob.aiBattle

					if hasattr(ob, 'expirator') and ob.expirator != None:
						newExpirator = expirator(newMob, ob.expirator.startingTime)
						newMob.expirator = newExpirator
					self.owner.currentRoom.mobs.append(newMob)
					newMob.currentRoom = self.owner.currentRoom
					print "$m " +str(newMob) + " " + newMob.name + " @ " + "[" +newMob.currentRoom.region + ":" + newMob.currentRoom.name + "] (pack)"
					for client in Globals.CLIENT_LIST:
						if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
							if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == newMob.currentRoom:      # if a client is in the room object just appeared in, let it know
								client.send_cc("^yA %s appeared.^~\n" %newMob.name)
					iters += 1

			elif self.mode == 'cont':	 	# always spawns exactly one mob
				newMortal = newMortal = mortal(hp=int(ob.kind.hp), maxHp=int(ob.kind.maxHp), pp=int(ob.kind.pp), maxPp=int(ob.kind.maxPp), level=int(ob.kind.level), exp=int(ob.kind.exp), money=int(ob.kind.money), offense=int(ob.kind.offense), defense=int(ob.kind.defense), speed=int(ob.kind.speed), guts=int(ob.kind.guts), luck=int(ob.kind.luck), vitality=int(ob.kind.vitality), IQ=int(ob.kind.IQ), inventory=[], inventorySize=int(ob.kind.inventorySize), equipment={})
				newMob = Mob(ob.description, ob.currentRoom, ob.name, ob.region, ob.longDescription, ob.speech, newMortal, ob.species, None)
				if hasattr(ob, 'aiMove'):
					newAIComponent = aiMove.movementAI(newMob, ob.aiMove.time)
					if ob.aiMove.Timer.actionFunction == ob.aiMove.basicRandom:
						newAIComponent.Timer.actionFunction = newAIComponent.basicRandom
					if ob.aiMove.Timer.actionFunction == ob.aiMove.introvertRandom:
						newAIComponent.Timer.actionFunction = newAIComponent.introvertRandom
					if ob.aiMove.Timer.actionFunction == ob.aiMove.extrovertRandom:
						newAIComponent.Timer.actionFunction = newAIComponent.extrovertRandom
					if ob.aiMove.Timer.actionFunction == ob.aiMove.doNotMove:
						newAIComponent.Timer.actionFunction = newAIComponent.doNotMove
				newMob.aiMove = newAIComponent

				if hasattr(ob, 'aiBattle'):
					newMob.aiBattle = ob.aiBattle

				if hasattr(ob, 'expirator') and ob.expirator != None:
					newExpirator = expirator(newMob, ob.expirator.startingTime)
					newMob.expirator = newExpirator
				self.owner.currentRoom.mobs.append(newMob)
				newMob.currentRoom = self.owner.currentRoom
				print "$m " +str(newMob) + " " + newMob.name + " @ " + "[" + newMob.currentRoom.region + ":" + newMob.currentRoom.name + "] (cont)"
				for client in Globals.CLIENT_LIST:
					if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
						if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == newMob.currentRoom:      # if a client is in the room object just appeared in, let it know
							client.send_cc("^yA %s appeared.^~\n" %newMob.name)

			elif self.mode == 'thresh':		# spawns mobs until the number of mobs in the room equals self.cycles
				resultsList = []
				for mob in self.owner.currentRoom.mobs:
					if mob.name == self.mob:
						resultsList.append(mob)
				numPresent = len(resultsList)
				#print numPresent
				if numPresent < self.cycles:
					newMortal = newMortal = mortal(hp=int(ob.kind.hp), maxHp=int(ob.kind.maxHp), pp=int(ob.kind.pp), maxPp=int(ob.kind.maxPp), level=int(ob.kind.level), exp=int(ob.kind.exp), money=int(ob.kind.money), offense=int(ob.kind.offense), defense=int(ob.kind.defense), speed=int(ob.kind.speed), guts=int(ob.kind.guts), luck=int(ob.kind.luck), vitality=int(ob.kind.vitality), IQ=int(ob.kind.IQ), inventory=[], inventorySize=int(ob.kind.inventorySize), equipment={})
					newMob = Mob(ob.description, ob.currentRoom, ob.name, ob.region, ob.longDescription, ob.speech, newMortal, ob.species, None)
					if hasattr(ob, 'aiMove'):
						newAIComponent = aiMove.movementAI(newMob, ob.aiMove.time)
						if ob.aiMove.Timer.actionFunction == ob.aiMove.basicRandom:
							newAIComponent.Timer.actionFunction = newAIComponent.basicRandom
						if ob.aiMove.Timer.actionFunction == ob.aiMove.introvertRandom:
							newAIComponent.Timer.actionFunction = newAIComponent.introvertRandom
						if ob.aiMove.Timer.actionFunction == ob.aiMove.extrovertRandom:
							newAIComponent.Timer.actionFunction = newAIComponent.extrovertRandom
						if ob.aiMove.Timer.actionFunction == ob.aiMove.doNotMove:
							newAIComponent.Timer.actionFunction = newAIComponent.doNotMove
					newMob.aiMove = newAIComponent

					if hasattr(ob, 'aiBattle'):
						newMob.aiBattle = ob.aiBattle

					if hasattr(ob, 'expirator') and ob.expirator != None:
						newExpirator = expirator(newMob, ob.expirator.startingTime)
						newMob.expirator = newExpirator
					self.owner.currentRoom.mobs.append(newMob)
					newMob.currentRoom = self.owner.currentRoom
					print "$m " +str(newMob) + " " + newMob.name + " @ " + "[" + newMob.currentRoom.region + ":" + newMob.currentRoom.name + "] (thresh)"
					for client in Globals.CLIENT_LIST:
						if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
							if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == newMob.currentRoom:      # if a client is in the room object just appeared in, let it know
								client.send_cc("^yA %s appeared.^~\n" %newMob.name)
				#else:
					#print "limit reached"

		self.timer.currentTime = self.time
		self.TIMERS.append(self.timer)
		#print "spawned"
		#print self.TIMERS


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Entity():
	"""
	A superclass for all moveable entities in the world.  Mob and Player both subclass this, so only functionality that they share should be here
	"""
	def __init__(self, description, currentRoom, name):
		self.description = description
		self.currentRoom = currentRoom
		self.name = name


class Mob(Entity):
	"""
	This class describes a generic badguy, and holds his information.  Methods will be added in mostly through components
	"""
	def __init__(self, description, currentRoom, name, region=None, longDescription = None, speech = None, kind = None, species = None, expirator = None, aiMove = None, aiBattle = None):
		Entity.__init__(self, description, currentRoom, name)
		self.region = region
		self.longDescription = longDescription
		self.speech = speech
		self.kind = kind
		self.species = species
		self.expirator = expirator
		self.aiMove = aiMove
		self.aiBattle = aiBattle

		# let components know what mob they belong to
		if self.kind:
			self.kind.owner = self
		# if self.species:
		# 	self.species.owner = self
		if self.expirator:
			self.expirator.owner = self
			if self.expirator.Timer != None:
				self.expirator.Timer.attachedTo = self

	def battleDeath(self, attackingPlayer):
		'''
		run when a mob dies.  Adds the mob's xp and money to the totals for the battle that the player will be awarded
		'''
		attackingPlayer.rewardExp += self.kind.exp
		attackingPlayer.rewardMoney += self.kind.money
		Globals.CLIENT_DATA[attackingPlayer.clientDataID].battleRoom.mobs.remove(self)
		attackingPlayer.client.send_cc("^!You killed " + self.name + "!^~\n")


class Player(Entity):
	"""
	This is a representation of the clients' avatar.  Methods should mostly be added using the same general components as mobs
	"""
	def __init__(self, description, currentRoom, name, client, clientDataID, title = 'just another soul on the bus.', kind = None, battleCommands = None, spawnRoom = None, rewardExp=0, rewardMoney=0, expToLevel=100):
		Entity.__init__(self, description, currentRoom, name)
		self.name = name
		self.title = title
		self.client = client
		self.clientDataID = clientDataID
		self.kind = kind
		if self.kind:
			self.kind.owner = self
		self.battleCommands = battleCommands
		if self.battleCommands == None:
			self.battleCommands = ('bash','flee')
		self.spawnRoom = spawnRoom

		self.spawnRoom = Globals.regionListDict['test']['bullpen']

		self.rewardExp = rewardExp
		self.rewardMoney = rewardMoney

		self.expToLevel = expToLevel
		self.lvlchoiceslist = []


	def battleDeath(self, killingMob):
		'''
		run when the player dies in battle.  Moves the player from the battleRoom to their spawnRoom and resets player hp to 1
		'''

		self.client.send_cc("\n^!You were killed by " + killingMob.name + "!\n")
		self.client.send_cc("You lose all sense of balance and direction.\n")
		self.client.send_cc("Reality seems less important by the second.\n")
		self.client.send_cc("Suddenly, you hear an impossibly deep gong and see a bright flash of white light.\n")
		self.client.send_cc("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

		self.rewardExp = 0

		Globals.CLIENT_DATA[self.clientDataID].battleRoom.players.remove(self)		
		self.kind.hp = 1
		for player in Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo.players:
			if player != self:
				player.client.send_cc("^R" +self.name.capitalize() + " was killed by " + killingMob.name + "!^~\n")

		#print Globals.CLIENT_DATA[self.clientDataID].battleRoom.players
		#Globals.CLIENT_DATA[self.clientDataID].battleRoom.players.remove(self)

		self.currentRoom = self.spawnRoom

		self.currentRoom.players.append(self)

		for player in self.currentRoom.players:
			if player != self:
				player.client.send_cc("^c" + self.name.capitalize() + " fell in battle.^~\n")

		print "-B " + str(self) + " " + self.name + " (player death)"


	def battleWin(self):
		'''
		run when the player wins a battle.  Moves the player from the battleRoom back to the currentRoom
		'''
		#print Globals.CLIENT_DATA[self.clientDataID].battleRoom.name
		#print Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo.name
		Globals.CLIENT_DATA[self.clientDataID].battleRoom.players.remove(self)
		#Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo.players.append(self)
		self.currentRoom = Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo
		
		for obj in self.currentRoom.objects:
			if obj.name.startswith("^r" + self.name):
				self.currentRoom.objects.remove(obj)

		self.client.send_cc("\n^!^U^I            ***YOU WIN!***            ^~\n\n")

		self.kind.exp += self.rewardExp
		self.expToLevel -= self.rewardExp
		leveled = self.levelUp()
		if not leveled:
			self.client.send_cc("You gained ^Y^!" + str(self.rewardExp) + " experience.^~\n")
			self.client.send_cc("______________________________________\n\n")		
		self.rewardExp = 0

		#print self.currentRoom.name
		cMove.move(client=self.client, cmd=Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo.name, args=[], CLIENT_LIST=Globals.CLIENT_LIST, CLIENT_DATA=Globals.CLIENT_DATA, exits={Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo.name:Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo}, fromBattle=True, leveledUp=leveled)

		Globals.battleRooms.remove(Globals.CLIENT_DATA[self.clientDataID].battleRoom)
		
		label = str(Globals.CLIENT_DATA[self.clientDataID].battleRoom.region)+str(Globals.CLIENT_DATA[self.clientDataID].battleRoom.name)
		if label in Globals.masterRooms:
			del Globals.masterRooms[label]

		Globals.CLIENT_DATA[self.clientDataID].battleRoom.attachedTo = None
		Globals.CLIENT_DATA[self.clientDataID].battleRoom = None
		if not leveled:
			Globals.CLIENT_DATA[self.clientDataID].gameState = 'normal'

		print "-B " + str(self) + " " + self.name + " (victory)"
		if leveled:
			print "lvl " + str(self) + " " + self.name + " (now " + str(self.kind.level) + ")"


	def levelUp(self):
		'''checks for and handles leveling up a player'''

		if self.expToLevel <= 0:
			Globals.CLIENT_DATA[self.clientDataID].gameState = 'levelup'
			self.kind.level += 1

			if self.expToLevel < 0:
				expMod = 0 + self.expToLevel
			else:
				expMod = 0

			expToLevelMod = (random.randint(80,120)+self.kind.level)/100.00
			newBaseExpToLevel = (((self.kind.exp + expMod) * self.kind.level)/(self.kind.level-1))*expToLevelMod
			self.expToLevel = int(newBaseExpToLevel)

			choicesList = []
			maxChoices = (abs(self.kind.IQ/3)-self.kind.level)
			if maxChoices < 1:
				maxChoices = 1
			numberOfChoices = random.randint(0, maxChoices)
			if numberOfChoices < 2:
				numberOfChoices = 2
			if numberOfChoices > 6:
				numberOfChoices = 6


			i = 0
			while i < numberOfChoices:
				spread = [0,0,0,0,0,0,0]
				boosts = 5
				if random.randint(0,20) == 0:
					boosts += random.randint(0, (self.kind.level/random.randint(1,5)))
					self.client.send_cc("^W^U****!!!SMASH!!!****^~\n")

				for x in range(boosts):	
					pointer = random.randint(0,6)
					spread[pointer] += 1
				choicesList.append(spread)
				i += 1


			self.client.send_cc("^W^UYOU GAINED A LEVEL!^~\n")
			self.client.send_cc("Which way would you like to develop?\n")
			self.client.send_cc("\n")
			self.client.send_cc("^W^IChoice  Off  Def  Vit  Gut  Spd  Lck  I.Q. ^~\n")
			self.client.send_cc("  A      " + str(choicesList[0][0]) + "    " + str(choicesList[0][1]) + "    " + str(choicesList[0][2]) + "    " + str(choicesList[0][3]) + "    " + str(choicesList[0][4]) + "    " + str(choicesList[0][5]) + "    " + str(choicesList[0][6]) + "\n")
			self.client.send_cc("  B      " + str(choicesList[1][0]) + "    " + str(choicesList[1][1]) + "    " + str(choicesList[1][2]) + "    " + str(choicesList[1][3]) + "    " + str(choicesList[1][4]) + "    " + str(choicesList[1][5]) + "    " + str(choicesList[1][6]) + "\n")
			if numberOfChoices > 2:
				self.client.send_cc("  C      " + str(choicesList[2][0]) + "    " + str(choicesList[2][1]) + "    " + str(choicesList[2][2]) + "    " + str(choicesList[2][3]) + "    " + str(choicesList[2][4]) + "    " + str(choicesList[2][5]) + "    " + str(choicesList[2][6]) + "\n")
			if numberOfChoices > 3:
				self.client.send_cc("  D      " + str(choicesList[3][0]) + "    " + str(choicesList[3][1]) + "    " + str(choicesList[3][2]) + "    " + str(choicesList[3][3]) + "    " + str(choicesList[3][4]) + "    " + str(choicesList[3][5]) + "    " + str(choicesList[3][6]) + "\n")
			if numberOfChoices > 4:
				self.client.send_cc("  E      " + str(choicesList[4][0]) + "    " + str(choicesList[4][1]) + "    " + str(choicesList[4][2]) + "    " + str(choicesList[4][3]) + "    " + str(choicesList[4][4]) + "    " + str(choicesList[4][5]) + "    " + str(choicesList[4][6]) + "\n")
			if numberOfChoices > 5:
				self.client.send_cc("  F      " + str(choicesList[5][0]) + "    " + str(choicesList[5][1]) + "    " + str(choicesList[5][2]) + "    " + str(choicesList[5][3]) + "    " + str(choicesList[5][4]) + "    " + str(choicesList[5][5]) + "    " + str(choicesList[5][6]) + "\n")

			self.lvlchoiceslist = choicesList
			return True
		else:
			return False


class mortal:		# 'kind' attribute 
	'''
	A component class for all attributes of mortals (living creatures)
	'''
	def __init__(self, hp, maxHp, pp, maxPp, level, exp, money, offense, defense, speed, guts, luck, vitality, IQ, inventory, inventorySize=16, equipment={}):
		self.hp = hp
		self.maxHp = maxHp
		self.pp = pp
		self.maxPp = maxPp
		self.level = level
		self.exp = exp
		self.money = money
		self.offense = offense
		self.defense = defense
		self.speed = speed
		self.guts = guts
		self.luck = luck
		self.vitality = vitality
		self.IQ = IQ
		self.inventory = inventory
		self.inventorySize = inventorySize
		self.equipment = equipment



class expirator:		# component added to mobs.  Causes the mob to expire and delete after a set period of time, so the world does not fill with mobs

	def __init__(self, owner, time):
		self.owner = owner
		self.time = time
		self.startingTime = time
		self.Timer = Timer(Globals.TIMERS, self.time, self.selfExpire, [], None, False)

	# def checkTimer(self):		#checks to see how long it has been since there was contact, and if it has been longer than the time, delete the mob.
	# 	if self.Timer.time <= 0:
	# 		self.selfExpire()

	def selfExpire(self):		#removes self from the game, and then deletes self to free up memory
		for player in Globals.regionListDict[self.owner.currentRoom.region][self.owner.currentRoom.name].players:
			player.client.send_cc("^y%s disappeared.^~\n" %self.owner.name.capitalize())

		print("-m " + str(self.owner)+ " " + str(self.owner.name) + " @ [" + str(self.owner.currentRoom.region) + ":" + str(self.owner.currentRoom.name)+ "] (expired)")

		if self.owner in Globals.regionListDict[self.owner.currentRoom.region][self.owner.currentRoom.name].mobs:
			Globals.regionListDict[self.owner.currentRoom.region][self.owner.currentRoom.name].mobs.remove(self.owner)

		#Globals.TIMERS.remove(self.Timer)
		if self.owner.aiMove != None and (self.owner.aiMove.Timer in Globals.MoveTIMERS):
			Globals.MoveTIMERS.remove(self.owner.aiMove.Timer)


	def resetTimer(self):		#if a player enters the same room as the mob, reset the timer continuously until the player leaves
		self.time = self.startingTime
		found = False
		if self.Timer != None:
			self.Timer.time = self.startingTime
			self.Timer.currentTime = self.startingTime
		for timer in Globals.TIMERS:
			if timer == self.Timer:
				timer.time = self.startingTime
				timer.currentTime = self.startingTime
				timerID = timer
				print ('#m ' + str(self.owner)+ " " + str(self.owner.name) + " @ [" + str(self.owner.currentRoom.region) + ":" + str(self.owner.currentRoom.name)+ "] (" + str(timerID.time) +")")

