# Engine.py
# checks for input from connected clients, and sends them to the appropriate handlers

import cChat

def process_clients(SERVER_RUN, CLIENT_LIST, CLIENT_DATA):
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:

            msg = client.get_command()
            lmsg = msg.lower()

            cmd = lmsg.split()[0]
            args = lmsg.split()[1:]

            clientDataID = str(client.addrport())
            prompt = CLIENT_DATA[clientDataID]['prompt']

            if CLIENT_DATA[clientDataID]['name'] == "none":     # client just logged in and doesn't have a name assigned.  Accept the first input and assign it to the client as it's name.
                CLIENT_DATA[clientDataID]['name'] = msg
                print ">> " + str(client.addrport()) + " identified as " + str(CLIENT_DATA[clientDataID]['name'])
                client.send("Hello, %s!\n" % CLIENT_DATA[clientDataID]['name'])
                # client.send(prompt)

            elif cmd == 'say':
                ## If the client sends a chat command echo it to the chat room via cChat.py
                cChat.say(client, args, CLIENT_LIST, CLIENT_DATA)


            elif cmd == 'quit':
                client.active = False


            elif cmd == 'shutdown':
                return 'shutdown'

            else:
                client.send("Huh?  I don't know that command.\n")