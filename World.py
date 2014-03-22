# World.py
"""
describes the classes for objects that will be in the world
"""

class World():
	"""
	This class represents the world map.  It should contain a list of regions, along with any other globally-applicable information
	"""
	def __init__(self, regions=[]):
		self.regions = regions


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
	def __init__(self, region='', name='', description='', exits={}, longDescription = '', players=[], containers=[], mobs=[]):
		self.containers = containers
		self.exits = exits
		self.mobs = mobs
		self.players = players
		self.description = description
		self.region = region
		self.name = name
		self.longDescription = longDescription


class Entity():
	"""
	A superclass for all moveable entities in the world.  Mob and Player both subclass this, so only functionality that they share should be here
	"""
	def __init__(self, description, currentRoom):
		self.description = description
		self.currentRoom = currentRoom



class Item():
	"""
	A superclass for items in the world.  Items are interactable, and often are able to be picked up and carried
	"""
	def __init__(self, description, currentRoom):
		self.description = description
		self.currentRoom = currentRoom


class Container(Item):
	"""
	This class represents some kind of container.  A container is an object that is visible and interactable in the world, that is able to hold other objects inside of it.
	"""
	def __init__(self, description, currentRoom, isCarryable = False):
		Item.__init__(description, currentRoom)
		self.isCarryable = isCarryable


class Mob(Entity):
	"""
	This class describes a generic badguy, and holds his information.  Methods will be added in mostly through constructors
	"""
	def __init__(self, description, currentRoom):
		Entity.__init__(self, description, currentRoom)


class Player(Entity):
	"""
	This is a representation of the clients' avatar.  Methods should mostly be added using the same general contstructors that the Mob class uses
	"""
	def __init__(self, description, currentRoom, name, client, clientDataID):
		Entity.__init__(self, description, currentRoom)
		self.name = name
		self.client = client
		self.clientDataID = clientDataID
