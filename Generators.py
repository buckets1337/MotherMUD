# generators.py
# handles functions that create things in the world

import os
import Objects, Globals
import World

def syscmdSpawnObject(refobj, spawnLocation, worldObject, alert=True, active=False, whereFrom='cmd', spawnContainer=None):
    # creates a new object based on the attributes of the object fed to the function

    obj = None
    # if whereFrom == 'cmd':
    #     active = True
    #print Objects.fromFileList[0].name
    #print str(refobj)
    for thing in Globals.fromFileList:
        if thing.name == str(refobj):
            obj = thing
            #print obj
    if obj == None:
        print ("%s not found." %refobj)
        return

    newObject = worldObject

    newObject.currentRoom = spawnLocation
    newObject.isVisible = obj.isVisible
    if obj.spawnContainer:
        newObject.spawnContainer = obj.spawnContainer
    else:
        newObject.spawnContainer = spawnContainer
    newObject.longDescription = obj.longDescription
    newObject.kind = obj.kind
    if newObject.kind:
        newObject.kind.owner = newObject
    newObject.TIMERS = obj.TIMERS
    # if newObject.TIMERS:
    #     newObject.TIMERS.owner = newObject

    if newObject.kind is not None:
        if isinstance(newObject.kind, World.item):
            newObject.kind = World.item()
            newObject.kind.owner = newObject
            newObject.kind.isCarryable = obj.kind.isCarryable
            newObject.kind.respawns = obj.kind.respawns
            newObject.kind.itemGrabHandler = obj.kind.itemGrabHandler
            if newObject.kind.itemGrabHandler:
                newObject.kind.itemGrabHandler.owner = newObject.kind
            newObject.kind.objectSpawner = obj.kind.objectSpawner
            if newObject.kind.objectSpawner:
                newObject.kind.objectSpawner.owner = newObject.kind

        if isinstance(newObject.kind, World.container):
            newObject.kind = World.container()
            newObject.kind.owner = newObject
            newObject.kind.inventory = []
            newObject.kind.isLocked = obj.kind.isLocked
            newObject.kind.isCarryable = obj.kind.isCarryable
            newObject.kind.respawns = obj.kind.respawns
            newObject.kind.respawnContents = obj.kind.respawnContents
            newObject.kind.itemGrabHandler = obj.kind.itemGrabHandler
            if newObject.kind.itemGrabHandler:
                newObject.kind.itemGrabHandler.owner = newObject.kind
            newObject.kind.objectSpawner = obj.kind.objectSpawner
            if newObject.kind.objectSpawner:
                newObject.kind.objectSpawner.owner = newObject.kind

        if newObject.kind.itemGrabHandler:
            newObject.kind.itemGrabHandler.notDroppable = obj.kind.itemGrabHandler.notDroppable

        if newObject.kind.objectSpawner:
            newObject.kind.objectSpawner = World.objectSpawner(newObject.kind)
            newObject.kind.objectSpawner.TIMERS = obj.kind.objectSpawner.TIMERS
            newObject.kind.objectSpawner.time = obj.kind.objectSpawner.time
            newObject.kind.objectSpawner.obj = obj.kind.objectSpawner.obj
            newObject.kind.objectSpawner.oddsList = obj.kind.objectSpawner.oddsList
            newObject.kind.objectSpawner.container = obj.kind.objectSpawner.container
            newObject.kind.objectSpawner.cycles = obj.kind.objectSpawner.cycles
            newObject.kind.objectSpawner.repeat = obj.kind.objectSpawner.repeat
            newObject.kind.objectSpawner.timer = World.Timer(newObject.kind.objectSpawner.TIMERS, newObject.kind.objectSpawner.time, newObject.kind.objectSpawner.spawn, [], newObject.kind.objectSpawner, newObject.kind.respawns)
            newObject.kind.objectSpawner.startingLocation = spawnLocation,

    if newObject.kind:
        if newObject.kind.objectSpawner:
            # print "has object spawner"
            newObject.kind.objectSpawner.active = active      # set the spawned object to active
            #print "active:" + str(newObject.kind.objectSpawner.active)

    spawnLocation.objects.append(newObject)
    symbol = '+'
    if whereFrom == 'cmd':
        symbol = 's'
    elif whereFrom == 'objSpawner':
        symbol = '$'
    elif whereFrom == 'inv':
    	symbol = 'i'
    if newObject.kind:
        if newObject.kind.objectSpawner:
            print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "] (active=" + str(newObject.kind.objectSpawner.active) +")"
        else:
            print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "]"
    else:
        print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "]"


    for client in Globals.CLIENT_LIST:
        if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
            if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == newObject.currentRoom:      # if a client is in the room object just appeared in, let it know
                if alert==True:
                	client.send_cc("^BA %s appeared.^~\n" %newObject.name)

    return newObject


# makes sure required directories exist, and if not, it creates them
path = [str("data/server/"), "data/client/", "data/log/auth/"]
for pathname in path:
	try:
		os.makedirs(pathname)
	except OSError:
		if not os.path.isdir(pathname):
			raise



def cmdSpawnObject(refobj, spawnLocation, worldObject, active=False, alert=True, whereFrom='cmd', spawnContainer=None):
    # creates a new object based on the attributes of the object fed to the function

    obj = None
    # if whereFrom == 'cmd':
    #     active = True
    #print Objects.fromFileList[0].name
    #print str(refobj)
    for thing in Objects.fromFileList:
        if thing.name == str(refobj):
            obj = thing
            #print obj
    if obj == None:
        print ("Unable to spawn, %s not found." %refobj)
        return

    newObject = World.Object('none', 'none')

    newObject.currentRoom = spawnLocation
    newObject.isVisible = obj.isVisible
    if obj.spawnContainer:
        newObject.spawnContainer = obj.spawnContainer
    else:
        newObject.spawnContainer = spawnContainer
    newObject.longDescription = obj.longDescription
    newObject.kind = obj.kind
    if newObject.kind is not None and hasattr(newObject, 'kind'):
        newObject.kind.owner = newObject
    newObject.TIMERS = obj.TIMERS
    # if newObject.TIMERS:
    #     newObject.TIMERS.owner = newObject

    if newObject.kind is not None:
        if isinstance(newObject.kind, World.item):
            newObject.kind = World.item()
            newObject.kind.owner = newObject
            newObject.kind.isCarryable = obj.kind.isCarryable
            newObject.kind.respawns = obj.kind.respawns
            if hasattr(obj.kind, 'itemGrabHandler') and obj.kind.itemGrabHandler is not None:
                newObject.kind.itemGrabHandler = World.itemGrabHandler()
            else:
                newObject.kind.itemGrabHandler = None
            if newObject.kind.itemGrabHandler is not None:
                newObject.kind.itemGrabHandler.owner = newObject.kind
            newObject.kind.objectSpawner = obj.kind.objectSpawner
            if newObject.kind.objectSpawner:
                newObject.kind.objectSpawner.owner = newObject.kind



        if isinstance(newObject.kind, World.container):
            newObject.kind = World.container()
            newObject.kind.owner = newObject
            newObject.kind.inventory = []
            newObject.kind.isLocked = obj.kind.isLocked
            newObject.kind.isCarryable = obj.kind.isCarryable
            newObject.kind.respawns = obj.kind.respawns
            newObject.kind.respawnContents = obj.kind.respawnContents
            if hasattr(obj.kind, 'itemGrabHandler') and obj.kind.itemGrabHandler is not None:
                newObject.kind.itemGrabHandler = World.itemGrabHandler()
            else:
                newObject.kind.itemGrabHandler = None
            #print newObject.kind.itemGrabHandler
            # newObject.kind.itemGrabHandler.owner = newObject.kind
            if newObject.kind.itemGrabHandler is not None:
                newObject.kind.itemGrabHandler.owner = newObject.kind
            newObject.kind.objectSpawner = obj.kind.objectSpawner
            if newObject.kind.objectSpawner:
                newObject.kind.objectSpawner.owner = newObject.kind

        if newObject.kind.itemGrabHandler is not None:
            if obj.kind.itemGrabHandler.notDroppable is not None:
                newObject.kind.itemGrabHandler.notDroppable = obj.kind.itemGrabHandler.notDroppable
            else:
                newObject.kind.itemGrabHandler.notDroppable = False

        if newObject.kind.objectSpawner:
            newObject.kind.objectSpawner = World.objectSpawner(newObject.kind)
            newObject.kind.objectSpawner.TIMERS = obj.kind.objectSpawner.TIMERS
            newObject.kind.objectSpawner.time = obj.kind.objectSpawner.time
            newObject.kind.objectSpawner.obj = obj.kind.objectSpawner.obj
            newObject.kind.objectSpawner.oddsList = obj.kind.objectSpawner.oddsList
            newObject.kind.objectSpawner.container = obj.kind.objectSpawner.container
            newObject.kind.objectSpawner.cycles = obj.kind.objectSpawner.cycles
            newObject.kind.objectSpawner.repeat = obj.kind.objectSpawner.repeat
            newObject.kind.objectSpawner.timer = World.Timer(newObject.kind.objectSpawner.TIMERS, newObject.kind.objectSpawner.time, newObject.kind.objectSpawner.spawn, [], newObject.kind.objectSpawner, newObject.kind.respawns)
            newObject.kind.objectSpawner.startingLocation = spawnLocation,


    if newObject.kind:
        if newObject.kind.objectSpawner:
            # print "has object spawner"
            newObject.kind.objectSpawner.active = active      # set the spawned object to active
            #print "active:" + str(newObject.kind.objectSpawner.active)
    if spawnLocation is not None:
        spawnLocation.objects.append(newObject)
    symbol = '+'
    if whereFrom == 'cmd':
        symbol = 's'
    elif whereFrom == 'objSpawner':
        symbol = '$'
    if newObject.kind:
        if newObject.kind.objectSpawner:
            if newObject.currentRoom is not None:
                print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "] (active=" + str(newObject.kind.objectSpawner.active) +")"
            else:
                print symbol +"o " + str(newObject) +": " + newObject.name + " @ [None] (active=" + str(newObject.kind.objectSpawner.active) +")"
        else:
            print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "]"
    else:
        print symbol +"o " + str(newObject) +": " + newObject.name + " @ [" + str(newObject.currentRoom.region) + ":" + str(newObject.currentRoom.name) + "]"


    for client in Globals.CLIENT_LIST:
        if Globals.CLIENT_DATA[str(client.addrport())].avatar is not None:
            if Globals.CLIENT_DATA[str(client.addrport())].avatar.currentRoom == newObject.currentRoom:      # if a client is in the room object just appeared in, let it know
                if newObject.spawnContainer is None and alert:
                # if not stuffed:
                    client.send_cc("^BA %s appeared.^~\n" %newObject.name)

    return newObject