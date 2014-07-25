#!/usr/bin/env python
#------------------------------------------------------------------------------
#   MUDserver.py
#   
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------

"""
Simple MUD server using miniboa
"""
import time

from miniboa import TelnetServer

from clientInfo import ClientInfo

import Engine, World, SysInit, RoomInit, MobInit, Rooms
import Objects
from cMove import alert

import Globals




IDLE_TIMEOUT = Globals.IDLE_TIMEOUT
CLIENT_LIST = Globals.CLIENT_LIST
SERVER_RUN = Globals.SERVER_RUN
CLIENT_DATA = Globals.CLIENT_DATA
TIMERS = Globals.TIMERS

OPList = Globals.OPList

def on_connect(client):
    """
    on_connect function.
    Handles new connections.
    """
    clientDataID = str(client.addrport())
    print "++ Opened connection to %s" % client.addrport()  
    #broadcast('%s connected.\n' % client.addrport() )
    CLIENT_LIST.append(client)
    #print "&&&&&&&&&&&&" + str(Globals.CLIENT_LIST)
    clientID = len(CLIENT_LIST) - 1

    clientInfo = ClientInfo(name='none', prompt='>>', client=client, clientID=clientID, clientDataID=clientDataID)
    CLIENT_DATA[clientDataID] = clientInfo

    CLIENT_DATA[clientDataID].loadFinish = False
    CLIENT_DATA[clientDataID].authSuccess = False
    CLIENT_DATA[clientDataID].numTries = 0

    client.send("\nWelcome to the MUD!\nPlease tell us your name.\n%s" % str(CLIENT_DATA[clientDataID].prompt))


def on_disconnect(client):
    """
    on_disconnect function.
    Handles lost connections.
    """
    clientDataID = str(client.addrport())
    player = CLIENT_DATA[clientDataID].avatar
    #print player
    print "-- Lost connection to %s" % client.addrport()

    Globals.CLIENT_LIST.remove(client)
    #print "clE:" + str(Globals.CLIENT_LIST)
    #Globals.CLIENT_LIST.remove(client)
    if player is not None:
        SysInit.clientDataSave(client, CLIENT_LIST, CLIENT_DATA, TIMERS)
        player.currentRoom.players.remove(player)
        alert(client, CLIENT_DATA, ("\n^g%s disappeared.^~\n" %player.name))

    #broadcast('%s leaves the conversation.\n' % client.addrport() )


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    ## Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT and CLIENT_DATA[str(client.addrport())].gameState != 'battle':
            print('>> Kicking idle lobby client from %s' % client.addrport())
            SysInit.clientDataSave(client, CLIENT_LIST, CLIENT_DATA, TIMERS)
            client.send("You have been kicked for inactivity.\n")
            client.active = False


def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)




 


#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':



    startupTime = time.time()
    lastTime = 0



    ## Create a telnet server with a port, address,
    ## a function to call with new connections
    ## and one to call with lost connections.

    '''address should be a blank string for deployment across a network, as blank allows the server to use any network interface it finds.
    localhost is for testing where server and clients both exist on one computer, without going across the network'''
    telnet_server = TelnetServer(
        port=7777,
        address='localhost',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout = .05
        )

    world = World.World(regions = ['test', 'testb', 'Onette'])     # create the world and load the regions into it



    # testCounter = 0

    # def testTimerFunction(args):
    #     print "Timer Alert" + str(args[0])
    #     args[0] += 1

    # testTimer = World.Timer(TIMERS, 1, testTimerFunction, [testCounter], respawns = True)
    #print TIMERS

    MobInit.loadMobs()
    RoomInit.setup()
    MobInit.loadSavedMobs()

    Globals.startingRoom = Globals.regionListDict['test']['bullpen']
    print 'startingRoom:' + str(Globals.startingRoom) + Globals.startingRoom.region + Globals.startingRoom.name.capitalize()+'\n'

    print(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)
    #print TIMERS

    with open('data/OPList', 'r') as f:
        OPList = f.readlines()

    #print str(Globals.TIMERS)

    ## Server Loop
    while SERVER_RUN:
        telnet_server.poll()        ## Send, Recv, and look for new connections

        kick_idle()     ## Check for idle clients
     
        currentTime = time.time()
        deltaTime = (currentTime - startupTime) - lastTime
        # print "last " + str(lastTime)
        # print "cur+start " + str((currentTime-startupTime))
        # print "del " + str(deltaTime)
        for timer in Globals.TIMERS:
            timer.tick(deltaTime)
        for timer in Globals.MoveTIMERS:
            timer.tick(deltaTime)
        lastTime = (currentTime - startupTime)

        engineState = Engine.process_clients(SERVER_RUN, OPList, CLIENT_LIST, CLIENT_DATA)           ## Check for client input, saving any state changes generated by the engine to 'engineState'
        if engineState == 'shutdown':
            #print engineState
            SysInit.dataSave(CLIENT_LIST, CLIENT_DATA, TIMERS)
            RoomInit.saveAllRooms()
            MobInit.saveMobs()
            Objects.saveEq()
            SERVER_RUN = False

    print("<< Server shutdown.")
