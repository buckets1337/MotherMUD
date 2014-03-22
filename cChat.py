# cChat.py
"""
defines the 'say' command, the 'tell' command, the 'shout' command, the 'chat' command, and all individual chat channel commands
"""

def say(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'say' to everyone in the room.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataID = str(client.addrport())
    prompt = CLIENT_DATA[clientDataID].prompt

    print '   <%s:%s>%s: %s' % (CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom.name.capitalize(), CLIENT_DATA[clientDataID].name, message)

    for guest in CLIENT_LIST:
        if guest != client:
            if CLIENT_DATA[str(guest.addrport())].avatar.currentRoom == CLIENT_DATA[clientDataID].avatar.currentRoom:
                guest.send_cc('\n^!%s says "%s"^..\n' % (CLIENT_DATA[clientDataID].name, message))
                # guest.send(prompt)
        else:
            guest.send('You say "%s".\n' % message)
            # guest.send(prompt)


def shout(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'shout' to everyone in the region.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataID = str(client.addrport())
    prompt = CLIENT_DATA[clientDataID].prompt

    print '   <%s>%s: %s' % (CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].name, message)

    for guest in CLIENT_LIST:
        if guest != client:
            if CLIENT_DATA[str(guest.addrport())].avatar.currentRoom.region == CLIENT_DATA[clientDataID].avatar.currentRoom.region:
                guest.send_cc('\n^!%s shouts "%s" from somewhere nearby.^.\n' % (CLIENT_DATA[clientDataID].name, message))
                # guest.send(prompt)
        else:
            guest.send('You shout "%s" for all to hear.\n' % message)
            # guest.send(prompt)

def chat(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'say' to everyone in the room.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataID = str(client.addrport())
    prompt = CLIENT_DATA[clientDataID].prompt

    print '   <chat> %s: %s' % (CLIENT_DATA[clientDataID].name, message)

    for guest in CLIENT_LIST:
        if guest != client:
            guest.send_cc('^Y<chat> %s: "%s"^~\n' % (CLIENT_DATA[clientDataID].name, message))
                # guest.send(prompt)
        else:
            guest.send_cc('^y<chat> %s: %s^~\n' % (CLIENT_DATA[clientDataID].name, message))
            # guest.send(prompt)