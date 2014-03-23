# World.py
"""
describes the classes for objects that will be in the world
"""





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
	def __init__(self, region='', name='', description='', exits={}, longDescription = '', players=[], items=[], containers=[], mobs=[]):
		self.containers = containers
		self.exits = exits
		self.mobs = mobs
		self.players = players
		self.description = description
		self.region = region
		self.name = name
		self.longDescription = longDescription
		self.items = items





#------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Object():
	"""
	A class representing objects in the world.  Objects contain a description and location, but may or may not be visible.
	An object that contains no other components is essentially a prop, or scenery.  Adding components allows items to be built that do more interesting things.
	"""
	def __init__(self, description, currentRoom, isVisible = False, longDescription = None, kind = None):
		self.description = description
		self.currentRoom = currentRoom
		self.isVisible = isVisible
		self.longDescription = longDescription
		if self.longDescription == None:
			self.longDescription = self.description
		self.kind = kind
		if self.kind:
			self.kind.owner = self



class item:		# 'kind' attribute
	"""
	This component represents an item, that is able to be picked up and used by players in some manner
	"""
	def __init__(self, isCarryable = True):
		self.isCarryable = isCarryable


class container:		# 'kind' attribute
	"""
	This component represents some kind of container.  A container is an object that has an inventory and may hold other items.
	"""
	def __init__(self, inventory = [], isCarryable = False):
		self.isCarryable = isCarryable





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