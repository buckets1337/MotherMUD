# World.py
"""
describes the classes for objects that will be in the world
"""

import Engine
import Globals



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

        self.currentTime = time

        self.TIMERS.append(self)

        # self.initialTime = time.clock()
        # self.lastTime = 0

    def tick(self, deltaTime):     
        """tick should be called once each game loop"""
        #timePassed = (time.clock() - self.initialTime) - self.lastTime

        self.currentTime -= deltaTime
        #print self.time

        if self.currentTime <= 0:
            self.TIMERS.remove(self)
            if self.actionArgs != []:
                self.actionFunction(self.actionArgs)
            else:
                self.actionFunction()


            if self.respawns == True:
                newTimer = Timer(self.TIMERS, self.time, self.actionFunction, self.actionArgs, self.attachedTo, self.respawns)




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
	def __init__(self, isCarryable = True, respawns = False, itemGrabHandler = None):
		self.isCarryable = isCarryable		# if true, item can be picked up into an inventory
		self.respawns = respawns 			# if true, item will eventually respawn at original location after it has been picked up
		self.itemGrabHandler = itemGrabHandler
		if self.itemGrabHandler:
			self.itemGrabHandler.owner = self


class container:		# 'kind' attribute
	"""
	This component represents some kind of container.  A container is an object that has an inventory and may hold other items.
	"""
	def __init__(self, inventory = [], isCarryable = False, respawns = False, respawnContents = False, itemGrabHandler = None, objectSpawner = None):
		self.inventory = inventory
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
	def get(self, client, player):
		# check if 'item' is in room...if so, remove it from room, and add it to avatar's inventory 
		if self.owner.isCarryable:
			player.kind.inventory.append(self.owner.owner)		# add the top level of the item to the avatar's inventory

			if self.owner.owner.spawnContainer is None:
				self.owner.owner.currentRoom.objects.remove(self.owner.owner)		# remove from the top level currentRoom's objects list the top level of the item
			else:
				self.owner.owner.spawnContainer.kind.inventory.remove(self.owner.owner)

			client.send("You picked up %s.\n" %self.owner.owner.name)


		else:
			client.send("You are not able to carry %s.\n" %item.name)
		

class objectSpawner:		# for 'kind' components, a component that, when placed in a room or container, will attempt to randomly spawn objects at specified intervals
	def __init__(self, owner, TIMERS, time, obj, oddsList, container = None, cycles=1, repeat = False):
		self.owner = owner
		self.TIMERS = TIMERS
		self.time = time
		self.obj = obj
		self.oddsList = oddsList
		self.container = container
		self.cycles = cycles
		self.repeat = repeat
		timer = Timer(TIMERS, time, self.spawn, [], self, False)
		self.timer = timer

	def spawn(self):
		# first, make a random determination of if item will be respawning this time
		if self.owner.respawns == True:
			winner = Engine.selector(self.oddsList)
			if winner[0]:
				# if yes, spawn the item and reset the spawner
				self.obj.currentRoom = self.owner.owner.currentRoom		# tell the object what room it is in

				#print self.owner.owner

				self.owner.owner.currentRoom.objects.append(self.obj)	# add the new object to the room

				for client in Globals.CLIENT_LIST:
					if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
						if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == self.owner.owner.currentRoom:		# if a client is in the room object just appeared in, let it know
							client.send_cc("^BA %s appeared.^~\n" %self.owner.owner.name)

				if self.repeat:
					self.timer.currentTime = self.time
					self.TIMERS.append(self.timer)

				elif self.cycles > 1:
					self.cycles -= 1
					self.timer.currentTime = self.time
					self.TIMERS.append(self.timer)

			else:
				self.timer.currentTime = self.time
				#print self.timer.time
				self.TIMERS.append(self.timer)




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Entity():
	"""
	A superclass for all moveable entities in the world.  Mob and Player both subclass this, so only functionality that they share should be here
	"""
	def __init__(self, description, currentRoom):
		self.description = description
		self.currentRoom = currentRoom


class Mob(Entity):
	"""
	This class describes a generic badguy, and holds his information.  Methods will be added in mostly through components
	"""
	def __init__(self, description, currentRoom, kind = None, species = None):
		Entity.__init__(self, description, currentRoom)
		self.kind = kind
		self.species = species

		# let components know what mob they belong to
		if self.kind:
			self.kind.owner = self
		if self.species:
			self.species.owner = self


class Player(Entity):
	"""
	This is a representation of the clients' avatar.  Methods should mostly be added using the same general components as mobs
	"""
	def __init__(self, description, currentRoom, name, client, clientDataID, kind = None):
		Entity.__init__(self, description, currentRoom)
		self.name = name
		self.client = client
		self.clientDataID = clientDataID
		self.kind = kind
		if self.kind:
			self.kind.owner = self


class mortal:		# 'kind' attribute 
	'''
	A component class for all attributes of mortals (living creatures)
	'''
	def __init__(self, hp, exp, inventory=[], equipment={}):
		self.hp = hp
		self.exp = exp
		self.inventory = inventory
		self.equipment = equipment