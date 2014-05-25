# Engine.py
"""
checks for input from connected clients, and sends them to the appropriate handlers
"""
import time, random, os

from passlib.hash import sha256_crypt

import cChat, cMove, cInfo, cInteractions, cPersonal, battleCommands
import Rooms
import World
import Objects
import Globals
import SysInit
# import clientInfo









def process_clients(SERVER_RUN, OPList, CLIENT_LIST, CLIENT_DATA):
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """




    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            msg = client.get_command()      # the string recieved from the client
            if msg.startswith("'"):
                msg = msg[:1] + " " + msg[1:]
            lmsg = msg.lower()              # an all-lowercase version of the string recieved from the client
            if msg == '':
                cmd = ''                    # cmd is the first word of the string from the client. It represents the command sent by the client, to be processed below
            else:
                cmd = lmsg.split()[0]

            args = msg.split()[1:]         # args is everything following the first word, not including the first word(cmd)
            #print "args: " + str(args)

            clientDataID = str(client.addrport())       # location of client's data in CLIENT_DATA
            prompt = CLIENT_DATA[clientDataID].prompt 

            

            commandSuccess = False
            #---------------------
            # Command Definitions
            #---------------------

            if CLIENT_DATA[clientDataID].name == "none" or CLIENT_DATA[clientDataID].name == '':     # client just logged in and doesn't have a name assigned.  Accept the first input and assign it to the client as it's name.
                CLIENT_DATA[clientDataID].name = str(msg)

                path = "data/client/" + CLIENT_DATA[clientDataID].name
                if os.path.isfile(path):
                    client.send("\nWelcome back, %s!\n" %CLIENT_DATA[clientDataID].name)
                    client.send("Please enter your password.\n")
                    return

                else:
                    client.send("\nHello, %s!\n" % CLIENT_DATA[clientDataID].name)
                    client.send("Choose a password.  It can be anything, just be sure to remember it.  If you lose your password, your character is gone forever!\n")
                    return

            while CLIENT_DATA[clientDataID].authSuccess == False:
                path = "data/client/" + CLIENT_DATA[clientDataID].name
                if os.path.isfile(path):
                    with open(path, 'r') as f:
                        CLIENT_DATA[clientDataID].password = f.readline()
                        CLIENT_DATA[clientDataID].password = CLIENT_DATA[clientDataID].password[:-1]
                else:
                    CLIENT_DATA[clientDataID].password = ' '

                if CLIENT_DATA[clientDataID].password == ' ':
                    CLIENT_DATA[clientDataID].password = sha256_crypt.encrypt(str(msg))
                    # print CLIENT_DATA[clientDataID].password
                    # print "pwl:" + str(len(CLIENT_DATA[clientDataID].password))

                    CLIENT_DATA[clientDataID].authSuccess = True

                else:
                    # path = "data/client/" + CLIENT_DATA[clientDataID].name
                    try:
                        with open(path, 'r') as f:
                            password = f.readline()
                            password = password[:-1]
                        # print password
                        # print "pwl:" + str(len(CLIENT_DATA[clientDataID].password))
                        CLIENT_DATA[clientDataID].authSuccess = sha256_crypt.verify(str(msg), password)
                        # print authSuccess
                        CLIENT_DATA[clientDataID].password = password

                    except:
                        raise

                if CLIENT_DATA[clientDataID].authSuccess == False:
                    if CLIENT_DATA[clientDataID].numTries == 2:
                        client.send("Last attempt is final before kick.\n")
                    elif CLIENT_DATA[clientDataID].numTries > 2:
                        CLIENT_DATA[clientDataID].numTries = 0
                        client.active = False

                    client.send("Incorrect password.  Please try again.\n")
                    CLIENT_DATA[clientDataID].numTries += 1
                    return



            if CLIENT_DATA[clientDataID].authSuccess == True and CLIENT_DATA[clientDataID].loadFinish == False:
                print "** " + str(client.addrport()) + " identified as " + str(CLIENT_DATA[clientDataID].name)

                # client.send(prompt)
                mortalComponent = World.mortal(hp=100,maxHp=100,pp=10,maxPp=10,level=1,exp=0,money=0,offense=1,defense=1,speed=1,guts=1,luck=1,vitality=1,IQ=1,inventory=[])
                
                if os.path.isfile('data/client/'+str(CLIENT_DATA[clientDataID].name)):
                    #print "cl:" + str(CLIENT_LIST)
                    #CLIENT_DATA[clientDataID].avatar = World.Player(description='Just another traveler.', currentRoom = Globals.startingRoom, name=CLIENT_DATA[clientDataID].name, client=client, clientDataID = clientDataID, kind=mortalComponent)          
                    SysInit.clientDataLoad(client, CLIENT_LIST, CLIENT_DATA, Globals.TIMERS, mortalComponent)
                    #Globals.startingRoom.players.remove(CLIENT_DATA[clientDataID].avatar)
                    # print 'sp:' + str(Globals.startingRoom.players) + " sr:" + str(Globals.startingRoom.name) + ' ' + str(Globals.startingRoom)
                    # print 'ava:' + str(CLIENT_DATA[clientDataID].avatar.currentRoom.name)+ ' asrp:'+ str(CLIENT_DATA[clientDataID].avatar.currentRoom.players)
                    # print 'avacr:' + str(CLIENT_DATA[clientDataID].avatar.currentRoom)
                    #print "cl2:" + str(CLIENT_LIST)
                else:
                    CLIENT_DATA[clientDataID].avatar = World.Player(description='Just another traveler.', currentRoom = Globals.startingRoom, name=CLIENT_DATA[clientDataID].name, client=client, clientDataID = clientDataID, kind=mortalComponent)
                    Globals.startingRoom.players.append(CLIENT_DATA[clientDataID].avatar)
                    # print 'starting;' + str(Globals.startingRoom.players)

                    with  open(path, 'w') as f:
                        f.write(str(CLIENT_DATA[clientDataID].password) + '\n')
                        # print CLIENT_DATA[clientDataID].password

                player = CLIENT_DATA[clientDataID].avatar
                for playerName in OPList:
                    #print str(CLIENT_DATA[clientDataID].name)
                    #print str(playerName)
                    if playerName.endswith('\n'):
                        playerName = playerName[:-1]
                    if str(CLIENT_DATA[clientDataID].name) == str(playerName):
                        CLIENT_DATA[clientDataID].op = True
                        #print "op true"
                    #print CLIENT_DATA[clientDataID].op

                cMove.alert(client, CLIENT_DATA, ("\n^g^!%s appeared.^~\n" %player.name))
                #print Rooms.startingRoom.players
                cInfo.render_room(client=client, player=CLIENT_DATA[clientDataID].avatar, room=CLIENT_DATA[clientDataID].avatar.currentRoom, CLIENT_DATA=CLIENT_DATA)
                CLIENT_DATA[clientDataID].loadFinish = True
                commandSuccess = True


            elif cmd == 'say':
                ## If the client sends a 'say' command echo it to the room
                cChat.say(client, args, CLIENT_LIST, CLIENT_DATA)
                commandSuccess = True


            elif cmd == 'shout':
                ## If the client sends a 'shout' command echo it to the region
                cChat.shout(client, args, CLIENT_LIST, CLIENT_DATA)
                commandSuccess = True


            elif cmd == 'tell' or cmd == 't':
                cChat.tell(client, args, CLIENT_LIST, CLIENT_DATA)
                commandSuccess = True


            elif cmd == 'chat' or cmd == 'c':
                ## If the client sends a 'chat' command echo it to the chat channel
                cChat.chat(client, args, CLIENT_LIST, CLIENT_DATA)
                CLIENT_DATA[str(client.addrport())].replyTo = None
                commandSuccess = True

            elif cmd == "'":
                if CLIENT_DATA[client.addrport()].replyTo is None:
                    cChat.chat(client, args, CLIENT_LIST, CLIENT_DATA)
                else:
                    args.insert(0, CLIENT_DATA[(CLIENT_DATA[client.addrport()].replyTo).addrport()].name)
                    isOnline = cChat.tell(client, args, CLIENT_LIST, CLIENT_DATA)
                    if isOnline == False:
                        CLIENT_DATA[str(client.addrport())].replyTo = None
                    #print CLIENT_DATA[client.addrport()].replyTo
                commandSuccess = True


            elif cmd == 'channel':
                ## if the client sends a 'channel' command, create a new chat channel
                cChat.Channel()
                commandSuccess = True


            elif cmd == 'who':
                ## display who is online
                cInfo.who(client, args, CLIENT_LIST, CLIENT_DATA)
                commandSuccess = True


            elif cmd == 'title':
                ## set player title to args
                cPersonal.title(client,args,CLIENT_LIST,CLIENT_DATA)
                commandSuccess = True


            elif cmd == 'inventory' or cmd == 'i':
                ## If the client sends an 'inventory' command, display the contents of the client avatar's inventory
                cInfo.inventory(client, args, CLIENT_LIST, CLIENT_DATA)
                commandSuccess = True

            elif cmd == 'status' or cmd == 'st':
                cInfo.status(client, args, CLIENT_LIST, CLIENT_DATA)
                commandSuccess = True


            elif CLIENT_DATA[clientDataID].op == True:        # OP-only commands.

                if cmd == 'spawn':     # don't spawn anything but top level items for testing, otherwise it breaks things
                    item = args[0]
                    if len(args)>1:
                        active = args[1]
                        #print active
                        if active == 'on':
                            active = True
                        elif active == 'off':
                            active = False
                        # elif active == '':
                        #     active = False
                        else:
                            client.send("Second argument should be 'on' to turn on object spawning, else 'off' or nothing.\n")
                            return
                        if len(args)>2:
                            container = args[2]

                    else:
                        active = False
                        container = None

                    newObject = cmdSpawnObject(item, CLIENT_DATA[clientDataID].avatar.currentRoom, active)

                    if container is not None:
                        for item in CLIENT_DATA[clientDataID].avatar.currentRoom.objects:
                            if item.name == str(container):
                                if hasattr(newObject, 'kind'):
                                    if hasattr(newObject.kind, 'objectSpawner'):
                                        if newObject.kind.objectSpawner is not None:
                                            newObject.kind.objectSpawner.container = item.kind
                                    if newObject.kind is not None:
                                        newObject.kind.spawnContainer = item
                                item.kind.inventory.append(newObject)
                                CLIENT_DATA[clientDataID].avatar.currentRoom.objects.remove(newObject)


                            # elif item.inventory != []:
                            #     for item in item.inventory:
                            #         if item.name == str(container):
                            #             if newObject.kind.objectSpawner:
                            #                 newObject.kind.objectSpawner.container = item
                            #             item.kind.inventory.append(newObject)
                            #             CLIENT_DATA[clientDataID].avatar.currentRoom.objects.inventory.remove(newObject)
                    commandSuccess = True

                elif cmd == 'shutdown':
                    ## shutdown the server (needs to be protected or removed)
                    print "** Shutdown request received from %s." % CLIENT_DATA[clientDataID].name
                    return 'shutdown'
                    commandSuccess = True


            # State-dependant commands

            if CLIENT_DATA[clientDataID].gameState == 'normal':
                if cmd in CLIENT_DATA[clientDataID].avatar.currentRoom.exits: 
                    ## player used a room exit name as a command, move to room associated with the exit
                    cMove.move(client, cmd, args, CLIENT_LIST, CLIENT_DATA, CLIENT_DATA[clientDataID].avatar.currentRoom.exits)

                elif cmd == 'get':
                    ## pick up an item in the room
                    cInteractions.get(client, args, clientDataID, CLIENT_DATA, (CLIENT_DATA[clientDataID].avatar.currentRoom))

                elif cmd == 'check':
                    cInteractions.check(client, args, clientDataID, CLIENT_DATA, CLIENT_DATA[clientDataID].avatar.currentRoom)

                elif cmd == 'drop':
                    ## drop an item in the room
                    cInteractions.drop(client, args, clientDataID, CLIENT_DATA, (CLIENT_DATA[clientDataID].avatar.currentRoom))

                elif cmd == 'fight' or cmd == 'f':
                    ## start a battle with a mob
                    cInteractions.startBattle(client, args, clientDataID, CLIENT_DATA, (CLIENT_DATA[clientDataID].avatar.currentRoom))
                    CLIENT_DATA[clientDataID].gameState = 'battle'

                elif cmd == 'look' or cmd == 'l':
                    ## If the client sends a 'look' command, send back the description
                    cInfo.look(client, args, CLIENT_LIST, CLIENT_DATA)

                elif cmd == 'lh':
                    ## alias for 'look harder'
                    cInfo.look(client, ['harder'], CLIENT_LIST, CLIENT_DATA)

                elif cmd == 'examine' or cmd == 'ex':
                    ## If the client sends an 'examine' command, send back the long description
                    cInfo.examine(client, args, CLIENT_LIST, CLIENT_DATA)

                elif cmd == 'quit':
                    ## client is disconnecting
                    client.send("Disconnected.")
                    #CLIENT_LIST.remove(client)
                    client.active = False


                elif cmd == '':
                    ## client just send a return ony, with no information at all
                    client.send("\nDid you mean to tell me something?\n\n")


                elif commandSuccess == False:
                    ## command does not exist or is badly formed
                    client.send("\nHuh?  I don't know what '%s' means.\n\n" % msg)




            elif CLIENT_DATA[clientDataID].gameState == 'battle':
                if cmd == 'look' or cmd == 'l':
                    cInfo.battleLook(client, args, CLIENT_LIST, CLIENT_DATA)

                elif cmd == 'examine' or cmd == 'ex':
                    cInfo.battleExamine(client, args, CLIENT_LIST, CLIENT_DATA)

                elif cmd == 'lh':
                    cInfo.battleExamine(client, ['lh'], CLIENT_LIST, CLIENT_DATA)

                elif cmd == 'flee':
                    cMove.fleeBattle(client, args, CLIENT_LIST, CLIENT_DATA)

                elif cmd in CLIENT_DATA[clientDataID].avatar.battleCommands:
                    if cmd == 'bash':
                        commandFunction = battleCommands.bash
                    commandFunction(client, args, CLIENT_LIST, CLIENT_DATA)


                elif cmd == '':
                    ## client just send a return ony, with no information at all
                    client.send("\nDid you mean to tell me something?\n\n")


                elif commandSuccess == False:
                    ## command does not exist or is badly formed
                    client.send("\nI can't '%s' in a battle.\n\n" % msg)




            elif cmd == '':
                ## client just send a return ony, with no information at all
                client.send("\nDid you mean to tell me something?\n\n")


            elif commandSuccess == False:
                ## command does not exist or is badly formed
                client.send("\nHuh?  I don't know what '%s' means.\n\n" % msg)




def selector(oddsList):     # pick a random selection from an odds list and return it.
                            # an odds list is a list containing any number of smaller lists, each with the format of [<choice>,<odds value>]
    totalOdds = 0

    for sel in oddsList:
        totalOdds += sel[1]
    #print "total odds" + str(totalOdds)

    oddSum = 0
    selection = random.randint(0, totalOdds)
    for sel in oddsList:
        oddSum += sel[1]
        if oddSum >= selection:
            break
    #print sel, selection
    #print Globals.TIMERS
    #for timer in Globals.TIMERS:
        #print timer.attachedTo.owner.owner.name
    return sel





def cmdSpawnObject(refobj, spawnLocation, active=False, alert=True, whereFrom='cmd', spawnContainer=None):
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

    newObject = World.Object(obj.name, obj.description)

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
    if obj.mobSpawner is not None:
        mobSpawner = obj.mobSpawner
    else:
        mobSpawner = None
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

    if mobSpawner is not None:
        newObject.mobSpawner = World.mobSpawner(newObject)
        newObject.mobSpawner.TIMERS = mobSpawner.TIMERS
        newObject.mobSpawner.time = mobSpawner.time
        newObject.mobSpawner.mob = mobSpawner.mob
        newObject.mobSpawner.oddsList = mobSpawner.oddsList
        newObject.mobSpawner.mode = mobSpawner.mode
        newObject.mobSpawner.cycles = mobSpawner.cycles
        newObject.mobSpawner.active = mobSpawner.active

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

