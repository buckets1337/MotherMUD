# Engine.py
"""
checks for input from connected clients, and sends them to the appropriate handlers
"""

import cChat, cMove, cInfo
import Rooms
import World
# import clientInfo

def process_clients(SERVER_RUN, CLIENT_LIST, CLIENT_DATA):
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:

            msg = client.get_command()
            lmsg = msg.lower()
            if msg == '':
                cmd = ''
            else:
                cmd = lmsg.split()[0]

            args = lmsg.split()[1:]

            clientDataID = str(client.addrport())
            prompt = CLIENT_DATA[clientDataID].prompt



            if CLIENT_DATA[clientDataID].name == "none":     # client just logged in and doesn't have a name assigned.  Accept the first input and assign it to the client as it's name.
                CLIENT_DATA[clientDataID].name = msg
                print "** " + str(client.addrport()) + " identified as " + str(CLIENT_DATA[clientDataID].name)
                client.send("\nHello, %s!\n" % CLIENT_DATA[clientDataID].name)
                # client.send(prompt)
                CLIENT_DATA[clientDataID].avatar = World.Player(description='Just another traveler.', currentRoom = Rooms.startingRoom, name=CLIENT_DATA[clientDataID].name, client=client, clientDataID = clientDataID)
                Rooms.startingRoom.players.append(CLIENT_DATA[clientDataID].avatar)
                player = CLIENT_DATA[clientDataID].avatar
                cMove.alert(client, CLIENT_DATA, ("\n^g%s appeared.^~\n" %player.name))
                #print Rooms.startingRoom.players
                cInfo.render_room(client=client, player=CLIENT_DATA[clientDataID].avatar, room=Rooms.startingRoom, CLIENT_DATA=CLIENT_DATA)


            elif cmd == 'say':
                ## If the client sends a chat command echo it to the chat room via cChat.py
                cChat.say(client, args, CLIENT_LIST, CLIENT_DATA)


            elif cmd == 'shout':
                cChat.shout(client, args, CLIENT_LIST, CLIENT_DATA)


            elif cmd == 'look':
                cInfo.look(client, args, CLIENT_LIST, CLIENT_DATA)


            elif cmd == 'examine':
                cInfo.examine(client, args, CLIENT_LIST, CLIENT_DATA)


            elif cmd in CLIENT_DATA[clientDataID].avatar.currentRoom.exits:         # player used an exit name as a command
                cMove.move(client, cmd, args, CLIENT_LIST, CLIENT_DATA, CLIENT_DATA[clientDataID].avatar.currentRoom.exits)


            elif cmd == 'quit':
                client.send("Disconnected.")
                client.active = False


            elif cmd == 'shutdown':
                print "** Shutdown request recieved from %s." % CLIENT_DATA[clientDataID].name
                return 'shutdown'


            elif cmd == '':
                client.send("\nDid you mean to tell me something?\n\n")


            else:
                client.send("\nHuh?  I don't know what %s means.\n\n" % cmd)





